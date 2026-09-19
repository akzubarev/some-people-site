"""Me serializer."""
from base64 import b64decode
from uuid import uuid4

from django.core.files.base import ContentFile
from rest_framework import serializers

from apps.users.models import User
from .base import UserSerializer


class UserPrivateSerializer(UserSerializer):
    """Serializes for /me route."""
    likes = serializers.SerializerMethodField()

    class Meta:
        """Model meta."""

        model = User
        fields = UserSerializer.Meta.fields + ('likes', 'vk_public', 'tg_public',)
        read_only_fields = fields

    def __init__(self, instance=None, *args, **kwargs) -> None:
        """Initializes the serializer."""
        avatar = kwargs.get('data', {}).get('avatar')
        if avatar and isinstance(avatar, str) and ';base64,' in avatar:
            avatar_format, image_str = avatar.split(';base64,')
            ext = avatar_format.split('/')[-1]
            kwargs['data']['avatar'] = ContentFile(b64decode(image_str), f'{uuid4()}.{ext}')

        phone = kwargs.get('data', {}).get('phone')
        if phone and phone[0] == '8':
            kwargs['data']['phone'] = phone.replace('8', '+7')

        vk = kwargs.get('vk', {}).get('vk')
        if vk:
            kwargs['data']['vk'] = vk.replace('https://', '').replace('vk.com/', '')

        super().__init__(instance, *args, **kwargs)

    def get_telegram(self, user: User) -> str:
        """Gets users telegram username."""
        return user.telegram_username

    def get_likes(self, user: User) -> str:
        return user.likes.all().values_list('id', flat=True)


class UserProfileUpdateSerializer(UserPrivateSerializer):
    """Only these profile fields may be changed through the SPA."""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'avatar',
                  'vk', 'vk_public', 'tg_public')
