"""Group serializers module."""
from rest_framework import serializers

from apps.games.models import Group
from apps.games.visibility import public_characters, visible_group_ids
from .character import CharacterSerializer


class GroupSerializer(serializers.ModelSerializer):
    """Group serializer."""

    characters = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
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
        ]

    def get_subgroups(self, group: Group) -> list[dict]:
        visible = self.visible_ids(group)
        return GroupSerializer(group.subgroups.filter(pk__in=visible), many=True,
                               context={'visible_group_ids': visible}).data

    def visible_ids(self, group):
        if 'visible_group_ids' not in self.context:
            self.context['visible_group_ids'] = visible_group_ids(group.game_id)
        return self.context['visible_group_ids']

    def get_characters(self, group):
        return CharacterSerializer(public_characters(group.game_id, self.visible_ids(group)).filter(group=group), many=True).data

    def get_members(self, group):
        return CharacterSerializer(public_characters(group.game_id, self.visible_ids(group)).filter(family=group), many=True).data
