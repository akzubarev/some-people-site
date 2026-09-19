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
        required=True, write_only=True, trim_whitespace=False, style={"input_type": "password"}
    )
    login_field = serializers.CharField(
        required=True
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
        candidate = User.objects.filter(Q(username=login_field) | Q(email=login_field)).first()
        self.user = authenticate(request=self.context.get('request'),
                                 username=candidate.username if candidate else login_field,
                                 password=password)
        if self.user:
            return attrs
        self.fail("invalid_credentials")
