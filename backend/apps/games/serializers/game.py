"""Game serializers module."""
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.games.models import Game, Character
from .character import CharacterSerializer
from .group import GroupSerializer


class GameSerializer(serializers.ModelSerializer):
    """Game serializer."""
    # groups = SerializerMethodField()
    player_count = SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'id',
            'alias',
            'title',
            'location',
            'description',
            'start',
            'end',
            'year',
            'short_description',
            'vk',
            'tg',
            # 'groups',
            'open_applications',
            'open_character_list',
            'player_count',
        ]

    # def get_groups(self, obj: Game):
    #     return GroupSerializer(
    #         obj.groups.filter(parent__isnull=True, hidden=False), many=True
    #     ).data

    def get_player_count(self, obj: Game):
        return Character.objects.filter(group__game=obj).count()
