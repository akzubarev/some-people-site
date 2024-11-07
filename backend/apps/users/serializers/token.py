"""Token serializers module."""
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from apps.users.models import User


class TokenSerializer(serializers.ModelSerializer):
    """Token serializer."""
    auth_token = serializers.CharField(source="key")

    class Meta:
        """Serializer meta."""
        model = Token
        fields = ("auth_token",)


class TokenCreateSerializer(serializers.Serializer):
    """Token create serializer."""
    password = serializers.CharField(
        required=False, style={"input_type": "password"}
    )
    login_field = serializers.CharField(
        required=False
    )

    default_error_messages = {
        "invalid_credentials": "invalid credentials",
        "inactive_account": "inactive account",
    }

    def __init__(self, *args, **kwargs):
        """Initializes serializer."""
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        """Validated model fields."""
        password = attrs.get("password")
        login_field = attrs.get("login_field")
        self.user = authenticate(
            request=self.context.get("request"),
            login_field=login_field, password=password
        )
        if not self.user:
            self.user = User.objects.filter(
                Q(username=login_field) | Q(email=login_field)
            ).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user:
            return attrs
        self.fail("invalid_credentials")
