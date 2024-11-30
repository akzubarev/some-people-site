"""Group serializers module."""
from rest_framework import serializers

from apps.games.models import Group
from .character import CharacterSerializer


class GroupSerializer(serializers.ModelSerializer):
    """Group serializer."""

    characters = CharacterSerializer(many=True)
    members = CharacterSerializer(many=True)
    subgroups = serializers.SerializerMethodField()

    class Meta:
        """Serializer meta."""

        model = Group
        fields = [
            'id',
            'order',
            'name',
            'alias',
            'hidden',
            'family',
            'description',
            'game',
            'parent',
            'characters',
            'members',
            'subgroups',
            'image',
        ]

    def get_subgroups(self, group: Group) -> list[dict]:
        return GroupSerializer(group.subgroups, many=True).data
