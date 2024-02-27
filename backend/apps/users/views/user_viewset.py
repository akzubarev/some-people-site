from django.conf import settings as main_settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.utils import timezone
from django.utils.translation import get_language_from_request
from django.utils.translation import gettext as _
from rest_framework import viewsets, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import (
    APIException, NotFound, PermissionDenied, ValidationError
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from apps.notifications.models import Notification
from apps.users import signals, utils
from apps.users.conf import settings
from apps.users.models import User, ActionRequest, \
    NewEmailChangeRequest, OldEmailChangeRequest
from apps.users.serializers import UserSmallSerializer
from apps.users.utils import ActivationEmail
from apps.users.utils.compat import get_user_email
from .utils import get_client_ip


class UserViewSet(LoggingMixin, viewsets.GenericViewSet,
                  mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin):
    serializer_class = settings.SERIALIZERS.user
    queryset = User.objects
    permission_classes = settings.PERMISSIONS.user
    token_generator = default_token_generator
    lookup_field = settings.USER_ID_FIELD

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def permission_denied(self, request, **kwargs):
        if (
                settings.HIDE_USERS
                and request.user.is_authenticated
                and self.action in ["update", "partial_update", "list",
                                    "retrieve"]
        ):
            raise NotFound()
        super().permission_denied(request, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        return queryset

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = settings.PERMISSIONS.user_create
        elif self.action == "activation":
            self.permission_classes = settings.PERMISSIONS.activation
        elif self.action == "resend_activation":
            self.permission_classes = settings.PERMISSIONS.password_reset
        elif self.action == "list":
            self.permission_classes = settings.PERMISSIONS.user_list
        elif self.action == "reset_password":
            self.permission_classes = settings.PERMISSIONS.password_reset
        elif self.action == "reset_password_confirm":
            self.permission_classes = settings.PERMISSIONS.password_reset_confirm
        elif self.action == "set_password":
            self.permission_classes = settings.PERMISSIONS.set_password
        elif self.action == "set_email":
            self.permission_classes = settings.PERMISSIONS.set_username
        elif self.action == "reset_username":
            self.permission_classes = settings.PERMISSIONS.username_reset
        elif self.action == "reset_username_confirm":
            self.permission_classes = settings.PERMISSIONS.username_reset_confirm
        elif self.action == "destroy" or (
                self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            self.permission_classes = settings.PERMISSIONS.user_delete
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.user_create
        elif self.action == "destroy" or (
                self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            return settings.SERIALIZERS.user_delete
        elif self.action == "activation":
            return settings.SERIALIZERS.activation
        elif self.action == "resend_activation":
            return settings.SERIALIZERS.password_reset
        elif self.action == "reset_password":
            return settings.SERIALIZERS.password_reset
        elif self.action == "set_email":
            return settings.SERIALIZERS.set_email
        elif self.action == "reset_password_confirm":
            if settings.PASSWORD_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.password_reset_confirm_retype
            return settings.SERIALIZERS.password_reset_confirm
        elif self.action == "set_password":
            if settings.SET_PASSWORD_RETYPE:
                return settings.SERIALIZERS.set_password_retype
            return settings.SERIALIZERS.set_password
        elif self.action == "set_username":
            if settings.SET_USERNAME_RETYPE:
                return settings.SERIALIZERS.set_username_retype
            return settings.SERIALIZERS.set_username
        elif self.action == "reset_username":
            return settings.SERIALIZERS.username_reset
        elif self.action == "reset_username_confirm":
            if settings.USERNAME_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.username_reset_confirm_retype
            return settings.SERIALIZERS.username_reset_confirm
        elif self.action == "me":
            return settings.SERIALIZERS.current_user

        return self.serializer_class

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = lambda: request.user
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)


    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def by_id(self, request):
        from django.shortcuts import get_object_or_404

        pk = request.GET["id"]
        try:
            user = get_object_or_404(User, pk=pk)
            serializer = UserSmallSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK,
                            headers={})
        except ValueError:
            raise APIException(detail=_('Invalid referral link'))

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def by_ids(self, request):
        pks = request.GET.getlist("id[]")
        users = User.objects.filter(pk__in=pks)
        serializer = UserSmallSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK, headers={})

    @action(
        ["post"], detail=False, url_path="reset_email",
        permission_classes=[AllowAny]
    )
    def reset_username(self, request, *args, **kwargs):
        User.objects.filter(pk=request.user.id).update(
            email=request._data.get("email"), email_active=False
        )
        return super().reset_username(request, *args, **kwargs)


    @action(["post"], detail=False)
    def change_email(self, request, *args, **kwargs):
        success = False
        user = request.user
        new_email = request.data.get('email', None)
        if None not in [user,  new_email]:
            user.email = new_email
            user.email_active = True
            user.save()
            success = True
        return Response(
            status=status.HTTP_204_NO_CONTENT if success is True
            else status.HTTP_406_NOT_ACCEPTABLE
        )

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied(_('You cannot delete this account.'))

    def perform_create(self, serializer):
        user = serializer.save()
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        user.last_login = None
        user.email_active = True
        user.save()
        context = {"user": user}
        to = [user.email]
        if main_settings.DJOSER.get("SEND_ACTIVATION_EMAIL") is True:
            try:
                ActivationEmail(self.request, context).send(to)
            except Exception as e:
                print(e)

    def perform_update(self, serializer):
        viewsets.ModelViewSet.perform_update(self, serializer)

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": self.request.user}
            to = [get_user_email(self.request.user)]
            settings.EMAIL.password_changed_confirmation(
                self.request, context
            ).send(to)

        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            utils.logout_user(self.request)
        elif settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(force_email=True)

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.password_reset(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.user.set_password(serializer.data["new_password"])
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = timezone.now()
        serializer.user.email_active = True
        serializer.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": serializer.user}
            to = [get_user_email(serializer.user)]
            settings.EMAIL.password_changed_confirmation(self.request,
                                                         context).send(to)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def create(self, request):
        if request.user.is_authenticated:
            PermissionDenied()
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)

        user = User.objects.filter(id=serializer.instance.id).first()
        user.save()
        data = dict(serializer.data)
        data["auth_token"] = token.key
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, context={'request': request}
        )
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(
            queryset, context={'request': request}, many=True
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def players(self, request, *args, **kwargs):
        game_alias = request.GET.get("game_alias")
        queryset = User.objects.filter(applications__game__alias=game_alias)
        serializer = self.serializer_class(
            queryset, context={'request': request}, many=True
        )
        return Response(serializer.data)
