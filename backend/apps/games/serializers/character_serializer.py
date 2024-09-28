"""Character serializers module."""
from rest_framework import serializers

from apps.games.models import Application, Character
from apps.users.models import User
from .application_serializer import ApplicationSerializer
from .tag_serializer import TagSerializer


class CharacterSerializer(serializers.ModelSerializer):
    """Character serializer."""
    applications = ApplicationSerializer(many=True)
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
            'applications',
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
