"""Me serializer."""
from base64 import b64decode
from binascii import Error as Base64Error
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

    def get_telegram(self, user: User) -> str | None:
        """Gets users telegram username."""
        return user.telegram_username

    def get_likes(self, user: User) -> list[int]:
        return user.likes.all().values_list('id', flat=True)


class ProfileImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and ';base64,' in data:
            header, encoded = data.split(';base64,', 1)
            if header not in ('data:image/png', 'data:image/jpeg', 'data:image/webp') or len(encoded) > 7 * 1024 * 1024:
                raise serializers.ValidationError('Допустимы PNG, JPEG и WebP размером до 5 МБ.')
            try:
                data = ContentFile(b64decode(encoded, validate=True), f'{uuid4()}.{header.split("/")[-1]}')
            except (Base64Error, ValueError):
                raise serializers.ValidationError('Некорректное изображение.')
        if getattr(data, 'size', 0) > 5 * 1024 * 1024:
            raise serializers.ValidationError('Максимальный размер — 5 МБ.')
        image = super().to_internal_value(data)
        if image.image.format not in ('PNG', 'JPEG', 'WEBP'):
            raise serializers.ValidationError('Допустимы PNG, JPEG и WebP.')
        return image


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Only these profile fields may be changed through the SPA."""
    avatar = ProfileImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'avatar',
                  'vk', 'vk_public', 'tg_public')
