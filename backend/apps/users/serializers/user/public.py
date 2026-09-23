"""User serializers module."""
from rest_framework import serializers

from apps.users.models import User


class UserPublicSerializer(serializers.ModelSerializer):
    """Explicit public profile; never inherit private profile fields."""
    vk = serializers.SerializerMethodField()
    telegram = serializers.SerializerMethodField()

    class Meta:
        """Serializer meta."""
        model = User
        fields = ('username', 'first_name', 'last_name', 'avatar', 'vk', 'telegram')
        read_only_fields = fields

    def get_vk(self, user: User) -> str | None:
        """Gets users vk username."""
        return user.vk if user.vk_public else None

    def get_telegram(self, user: User) -> str | None:
        return user.telegram_username if user.tg_public else None
