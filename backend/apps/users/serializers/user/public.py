"""User serializers module."""
from rest_framework import serializers

from apps.users.models import User
from .base import UserSerializer


class UserPublicSerializer(UserSerializer):
    """User serializer."""
    vk = serializers.SerializerMethodField()

    class Meta:
        """Serializer meta."""
        model = User
        fields = UserSerializer.Meta.fields
        read_only_fields = UserSerializer.Meta.fields

    def get_vk(self, user: User) -> str:
        """Gets users vk username."""
        return user.vk if user.vk_public else None
