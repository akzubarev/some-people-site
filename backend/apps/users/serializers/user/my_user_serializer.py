from base64 import b64decode

from django.core.files.base import ContentFile

from .user_serializer import UserSerializer


class MyUserSerializer(UserSerializer):
    class Meta:
        model = UserSerializer.Meta.model
        read_only_fields = UserSerializer.Meta.read_only_fields
        fields = UserSerializer.Meta.fields

    def __init__(self, instance=None, *args, **kwargs):
        logo = kwargs.get('data', {}).get('avatar')

        if logo and isinstance(logo, str) and ';base64,' in logo:
            format, imgstr = logo.split(';base64,')
            ext = format.split('/')[-1]
            kwargs['data']['avatar'] = ContentFile(b64decode(imgstr),
                                                   'avatar.{}'.format(ext))
        return super().__init__(instance, *args, **kwargs)
