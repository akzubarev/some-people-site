from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions as rest_exceptions, serializers

from apps.users import utils
from apps.users.conf import settings
from apps.users.models import User


class ReActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']
        read_only_fields = fields


class ActivationSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    default_error_messages = {
        "invalid_token": settings.CONSTANTS.messages.INVALID_TOKEN_ERROR,
        "invalid_uid": settings.CONSTANTS.messages.INVALID_UID_ERROR,
    }

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        # uid validation have to be here, because validate_<field_name>
        # doesn't work with modelserializer
        try:
            uid = utils.decode_uid(self.initial_data.get("uid", ""))
            self.user = User.objects.get(pk=uid)
            self.user.last_login = None
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise rest_exceptions.ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )

        if self.user.email_active:
            raise rest_exceptions.PermissionDenied(
                _("The given email already verified."))

        is_token_valid = self.context["view"].token_generator.check_token(
            self.user, self.initial_data.get("token", "")
        )
        if is_token_valid:
            return validated_data
        else:
            key_error = "invalid_token"
            raise rest_exceptions.ValidationError(
                {"token": [self.error_messages[key_error]]}, code=key_error
            )
