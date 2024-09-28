"""Me serializer."""
from base64 import b64decode

from django.core.files.base import ContentFile

from .user_serializer import UserSerializer


class MyUserSerializer(UserSerializer):
    """Serializes for the /me route."""

    class Meta:
        """Model meta."""

        model = UserSerializer.Meta.model
        read_only_fields = UserSerializer.Meta.read_only_fields
        fields = UserSerializer.Meta.fields

    def __init__(self, instance=None, *args, **kwargs) -> None:
        """Initializes the serializer."""
        avatar = kwargs.get('data', {}).get('avatar')

        if avatar and isinstance(avatar, str) and ';base64,' in avatar:
            avatar_format, image_str = avatar.split(';base64,')
            ext = avatar_format.split('/')[-1]
            kwargs['data']['avatar'] = ContentFile(b64decode(image_str), f'avatar.{ext}')
        super().__init__(instance, *args, **kwargs)
