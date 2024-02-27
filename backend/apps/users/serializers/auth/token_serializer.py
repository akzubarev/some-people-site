from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users import utils
from apps.users.conf import settings
from apps.users.models import User


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")

    class Meta:
        model = Token
        fields = ("auth_token",)


class TokenCreateSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=False, style={"input_type": "password"}
    )
    login_field = serializers.CharField(
        required=False
    )

    default_error_messages = {
        "invalid_credentials": settings.CONSTANTS.messages.INVALID_CREDENTIALS_ERROR,
        "inactive_account": settings.CONSTANTS.messages.INACTIVE_ACCOUNT_ERROR,
        "email_not_active": settings.CONSTANTS.messages.INACTIVE_EMAIL_ERROR
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        password = attrs.get("password")
        login_field = attrs.get("login_field")
        self.user = authenticate(
            request=self.context.get("request"),
            login_field=login_field, password=password
        )
        if not self.user:
            self.user = User.objects.filter(
                # Q(**{"username": login_field}) |
                Q(**{"email": login_field})
            ).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user and self.user.is_active:
            if utils.is_email_verify_enabled(
                    self.user) and not self.user.email_active:
                self.fail("email_not_active")
            return attrs
        self.fail("invalid_credentials")
