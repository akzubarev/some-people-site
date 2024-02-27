from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import serializers

from apps.users.conf import settings
from .uid_token_serializer import UidAndTokenSerializer


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        user = getattr(self, "user", None) or self.context["request"].user
        # why assert? There are ValidationError / fail everywhere
        assert user is not None

        try:
            validate_password(attrs["new_password"], user)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)})
        return super().validate(attrs)


class CurrentPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {
        "invalid_password": settings.CONSTANTS.messages.INVALID_PASSWORD_ERROR
    }

    def validate_current_password(self, value):
        is_password_valid = self.context["request"].user.check_password(value)
        if is_password_valid:
            return value
        else:
            self.fail("invalid_password")


class PasswordRetypeSerializer(PasswordSerializer):
    re_new_password = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {
        "password_mismatch": settings.CONSTANTS.messages.PASSWORD_MISMATCH_ERROR
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["new_password"] == attrs["re_new_password"]:
            return attrs
        else:
            self.fail("password_mismatch")


class SetPasswordSerializer(PasswordSerializer, CurrentPasswordSerializer):
    pass


class SetPasswordRetypeSerializer(PasswordRetypeSerializer,
                                  CurrentPasswordSerializer):
    pass


class PasswordResetConfirmRetypeSerializer(
    UidAndTokenSerializer, PasswordRetypeSerializer
):
    pass


class PasswordResetConfirmSerializer(UidAndTokenSerializer,
                                     PasswordSerializer):
    pass
