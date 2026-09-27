"""Same-origin browser authentication; token endpoints remain for other clients."""
from django.contrib.auth import login, logout
from django.db import transaction
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema

from apps.users.serializers import TokenCreateSerializer, UserCreateSerializer, UserPrivateSerializer


class SessionSerializer(serializers.Serializer):
    user = UserPrivateSerializer(read_only=True, allow_null=True)
    csrfToken = serializers.CharField(read_only=True)


@method_decorator(csrf_protect, name='dispatch')
class BrowserSession(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    def get_throttles(self):
        # Discovering a browser session must not consume the login-attempt quota.
        if self.request.method == 'GET':
            return []
        return super().get_throttles()

    def response(self, request, status=200):
        user = (UserPrivateSerializer(request.user, context={'request': request}).data
                if request.user.is_authenticated else None)
        response = Response({'user': user, 'csrfToken': get_token(request)}, status=status)
        response['Cache-Control'] = 'no-store'
        return response

    @extend_schema(responses=SessionSerializer)
    def get(self, request):
        return self.response(request)

    @extend_schema(request=TokenCreateSerializer, responses=SessionSerializer)
    def post(self, request):
        serializer = TokenCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        login(request, serializer.user)
        return self.response(request)

    @extend_schema(request=None, responses=SessionSerializer)
    def delete(self, request):
        logout(request)
        return self.response(request)


class BrowserRegistration(BrowserSession):
    http_method_names = ['post', 'options']

    @transaction.atomic
    @extend_schema(request=UserCreateSerializer, responses={201: SessionSerializer})
    def post(self, request):
        if request.user.is_authenticated:
            return Response({'detail': 'Sign out before registering.'}, status=400)
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return self.response(request, status=201)
