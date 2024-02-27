from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import serializers
from rest_framework.settings import api_settings

from apps.users.conf import settings
from apps.users.models import User
from apps.users.serializers.mixins import UserCreateMixin


class UserCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True
    )

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + tuple(settings.LOGIN_FIELDS) + (
            settings.USER_ID_FIELD, "password",
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[
                    api_settings.NON_FIELD_ERRORS_KEY
                ]}
            )

        return attrs

# UserCreateSerializer.Meta.fields += ('first_name', 'last_name', 'phone', 'site')
