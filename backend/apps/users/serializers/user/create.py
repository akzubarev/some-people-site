"""User creation serializers module."""
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import serializers
from rest_framework.settings import api_settings

from apps.users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """User creation serializer."""
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True
    )

    class Meta:
        """Serializer meta."""
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "username",
            "password",
        ]

    def validate(self, attrs):
        """Validates model fields."""
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
