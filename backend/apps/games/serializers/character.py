"""Character serializers module."""
from rest_framework import serializers

from apps.games.models import Application, Character
from apps.users.models import User
from .application import ApplicationSerializer
from .tag import TagSerializer


class CharacterSerializer(serializers.ModelSerializer):
    """Character serializer."""
    application = ApplicationSerializer()
    tags = TagSerializer(many=True)
    player = serializers.SerializerMethodField()

    class Meta:
        """Serializer meta."""

        model = Character
        fields = [
            'id',
            'name',
            'alias',
            'description',
            'master',
            'image',
            'application',
            'player',
            'tags',
        ]

    def get_player(self, character: Character) -> dict | None:
        """Gets characters player info."""
        player = User.objects.filter(
            applications__character=character,
            applications__status=Application.Status.CONFIRMED
        ).first()
        if player is not None:
            from apps.users.serializers import UserSerializer
            return UserSerializer(player).data
        else:
            return None
