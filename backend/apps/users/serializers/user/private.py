"""Me serializer."""
from base64 import b64decode

from django.core.files.base import ContentFile
from rest_framework import serializers

from apps.users.models import User
from utils.auth import encode_uuid
from .public import UserSerializer


class UserPrivateSerializer(UserSerializer):
    """Serializes for /me route."""
    telegram_code = serializers.SerializerMethodField()

    class Meta:
        """Model meta."""

        model = User
        fields = UserSerializer.Meta.fields + ('telegram_code',)
        read_only_fields = UserSerializer.Meta.read_only_fields

    def __init__(self, instance=None, *args, **kwargs) -> None:
        """Initializes the serializer."""
        avatar = kwargs.get('data', {}).get('avatar')
        if avatar and isinstance(avatar, str) and ';base64,' in avatar:
            avatar_format, image_str = avatar.split(';base64,')
            ext = avatar_format.split('/')[-1]
            kwargs['data']['avatar'] = ContentFile(b64decode(image_str), f'avatar.{ext}')
        super().__init__(instance, *args, **kwargs)

    def get_telegram_code(self, user: User) -> str:
        """Returns users telegram code."""
        return encode_uuid(uuid=user.uuid)
