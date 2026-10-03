"""CSRF-protected Google sign-in and explicit password-proven account linking."""
from datetime import timedelta
import hashlib
import secrets
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import login
from django.db import IntegrityError, transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle

from apps.users.google_auth import verify_identity
from apps.users.models import GoogleChallenge, GoogleIdentity, User
from .session import BrowserSession, SessionSerializer


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


class GoogleThrottle(SimpleRateThrottle):
    scope = 'google_auth'
    rate = '10/minute'

    def get_cache_key(self, request, view):
        return self.cache_format % {'scope': self.scope, 'ident': self.get_ident(request)}


class ChallengeInput(serializers.Serializer):
    purpose = serializers.ChoiceField(choices=['signin', 'link'])
    password = serializers.CharField(required=False, write_only=True, trim_whitespace=False, max_length=4096)


class ChallengeOutput(serializers.Serializer):
    nonce = serializers.CharField()
    client_id = serializers.CharField()
    expires_in = serializers.IntegerField()


class CredentialInput(serializers.Serializer):
    nonce = serializers.CharField(min_length=43, max_length=43)
    credential = serializers.CharField(max_length=16384, trim_whitespace=False)


class CancelInput(serializers.Serializer):
    nonce = serializers.CharField(min_length=43, max_length=43)


class PasswordInput(serializers.Serializer):
    password = serializers.CharField(write_only=True, trim_whitespace=False, max_length=4096)


class GoogleStatus(serializers.Serializer):
    enabled = serializers.BooleanField()
    linked = serializers.BooleanField()
    can_unlink = serializers.BooleanField()


def password_proof(request, password):
    if not request.user.is_authenticated or not request.user.is_active:
        raise PermissionDenied('Sign in to the existing account first.')
    if not request.user.has_usable_password() or not request.user.check_password(password or ''):
        raise PermissionDenied('Confirm your current password to change Google linking.')


class GoogleBase(BrowserSession):
    throttle_classes = [GoogleThrottle]

    def enabled(self):
        if not settings.GOOGLE_OAUTH_CLIENT_ID:
            raise ValidationError({'detail': 'Google sign-in is not configured.'})

    def consume(self, request, nonce):
        # Atomic conditional UPDATE: only one request may use the nonce, even
        # across workers. Consume before verification, including failed attempts.
        now = timezone.now()
        query = GoogleChallenge.objects.filter(
            digest=digest(nonce), browser_digest=digest(request.session.get('google_browser', '')),
            user_id=request.user.pk if request.user.is_authenticated else None,
            expires_at__gt=now, consumed_at__isnull=True)
        if query.update(consumed_at=now) != 1:
            raise ValidationError({'detail': 'Google attempt expired or was already used. Start again.'})
        return query.model.objects.get(digest=digest(nonce))


class GoogleChallengeView(GoogleBase):
    http_method_names = ['post', 'delete', 'options']

    @extend_schema(request=ChallengeInput, responses=ChallengeOutput)
    def post(self, request):
        self.enabled()
        serializer = ChallengeInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if data['purpose'] == 'link':
            password_proof(request, data.get('password'))
        elif request.user.is_authenticated:
            raise PermissionDenied('Sign out before Google sign-in.')
        binding = request.session.get('google_browser') or secrets.token_urlsafe(32)
        request.session['google_browser'] = binding
        nonce = secrets.token_urlsafe(32)
        now = timezone.now()
        # Remove old credentials without touching unexpired attempts in other browsers.
        GoogleChallenge.objects.filter(expires_at__lte=now).delete()
        GoogleChallenge.objects.filter(browser_digest=digest(binding), consumed_at__isnull=True).update(consumed_at=now)
        GoogleChallenge.objects.create(digest=digest(nonce), browser_digest=digest(binding),
            user=request.user if request.user.is_authenticated else None,
            purpose=data['purpose'], expires_at=now + timedelta(minutes=5))
        response = Response({'nonce': nonce, 'client_id': settings.GOOGLE_OAUTH_CLIENT_ID, 'expires_in': 300})
        response['Cache-Control'] = 'no-store'
        return response

    @extend_schema(request=CancelInput, responses={204: None})
    def delete(self, request):
        serializer = CancelInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.consume(request, serializer.validated_data['nonce'])
        return Response(status=204, headers={'Cache-Control': 'no-store'})


class GoogleCredentialView(GoogleBase):
    http_method_names = ['post', 'options']

    @extend_schema(request=CredentialInput, responses=SessionSerializer)
    def post(self, request):
        self.enabled()
        serializer = CredentialInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        nonce = serializer.validated_data['nonce']
        challenge = self.consume(request, nonce)
        claims = verify_identity(serializer.validated_data['credential'], nonce)
        email = serializers.EmailField(max_length=255).run_validation(claims.get('email')).lower()
        try:
            with transaction.atomic():
                identity = GoogleIdentity.objects.filter(subject=claims['sub']).first()
                if challenge.purpose == 'link':
                    user = User.objects.select_for_update().get(pk=challenge.user_id)
                    if not user.is_active:
                        raise PermissionDenied('Account is inactive.')
                    if identity and identity.user_id != user.pk:
                        raise ValidationError({'detail': 'This Google identity is already linked to another account.'})
                    if GoogleIdentity.objects.filter(user=user).exclude(subject=claims['sub']).exists():
                        raise ValidationError({'detail': 'Unlink the current Google identity first.'})
                    # An authenticated account plus password proof authorizes linking;
                    # matching email alone never authorizes it. Different email is fine,
                    # but must not belong to another existing application account.
                    if User.objects.filter(email__iexact=email).exclude(pk=user.pk).exists():
                        raise ValidationError({'detail': 'Sign in to the account using this email to link Google.'})
                    GoogleIdentity.objects.get_or_create(user=user, subject=claims['sub'], defaults={'email': email})
                elif identity:
                    user = User.objects.select_for_update().get(pk=identity.user_id)
                    if not GoogleIdentity.objects.filter(user=user, subject=claims['sub']).exists():
                        raise ValidationError({'detail': 'Google linking changed. Start again.'})
                    if not user.is_active:
                        raise PermissionDenied('Account is inactive.')
                else:
                    if User.objects.filter(email__iexact=email).exists():
                        raise ValidationError({'detail': 'This email already has an account. Sign in with your password, then link Google in profile settings.'})
                    user = User(username='g_' + uuid4().hex[:28], email=email,
                                first_name=str(claims.get('given_name', ''))[:100],
                                last_name=str(claims.get('family_name', ''))[:100])
                    user.set_unusable_password()
                    user.save()
                    GoogleIdentity.objects.create(user=user, subject=claims['sub'], email=email)
        except IntegrityError:
            raise ValidationError({'detail': 'An account or Google identity already exists. Start again or sign in to your existing account.'})
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return self.response(request)


class GoogleIdentityView(GoogleBase):
    http_method_names = ['get', 'delete', 'options']

    @extend_schema(responses=GoogleStatus)
    def get(self, request):
        authenticated = request.user.is_authenticated
        linked = authenticated and GoogleIdentity.objects.filter(user=request.user).exists()
        return Response({'enabled': bool(settings.GOOGLE_OAUTH_CLIENT_ID), 'linked': linked,
                         'can_unlink': linked and request.user.has_usable_password()},
                        headers={'Cache-Control': 'no-store'})

    @extend_schema(request=PasswordInput, responses=SessionSerializer)
    def delete(self, request):
        serializer = PasswordInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        password_proof(request, serializer.validated_data['password'])
        with transaction.atomic():
            user = User.objects.select_for_update().get(pk=request.user.pk)
            if not user.is_active or not user.has_usable_password() or not user.check_password(serializer.validated_data['password']):
                raise PermissionDenied('Confirm your current password.')
            GoogleIdentity.objects.filter(user=user).delete()
            GoogleChallenge.objects.filter(user=user, consumed_at__isnull=True).update(consumed_at=timezone.now())
        return self.response(request)
