"""User creation serializers module."""
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from django.core import exceptions as django_exceptions
from rest_framework import serializers
from rest_framework.settings import api_settings

from apps.users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """User creation serializer."""
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True, trim_whitespace=False
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

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('An account already uses this email. Sign in to it first.')
        return value

    def create(self, validated_data):
        try:
            with transaction.atomic():
                return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'email': 'An account already exists. Sign in or choose another email or username.'})

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
