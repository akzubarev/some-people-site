"""Character serializers module."""
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.helpers import lazy_serializer

from apps.games.models import Application, Character
from apps.users.models import User
# from .application import ApplicationPublicSerializer
from .tag import TagSerializer


class CharacterSerializer(serializers.ModelSerializer):
    """Character serializer."""
    # application = ApplicationPublicSerializer()
    tags = TagSerializer(many=True, read_only=True)
    player = serializers.SerializerMethodField()

    class Meta:
        """Serializer meta."""

        model = Character
        fields = [
            'id',
            'name',
            'name_eng',
            'alias',
            'description',
            'image',
            'player',
            'tags',
        ]
        read_only_fields = fields

    @extend_schema_field(lazy_serializer('apps.users.serializers.UserPublicSerializer')(allow_null=True))
    def get_player(self, character: Character) -> dict | None:
        """Gets characters player info."""
        player = User.objects.filter(
            applications__character=character,
            applications__status=Application.Status.CONFIRMED
        ).first()
        if player is not None:
            from apps.users.serializers import UserPublicSerializer
            return UserPublicSerializer(player).data
        else:
            return None
