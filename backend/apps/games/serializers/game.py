"""Game serializers module."""
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.games.models import Game, Character
from .character import CharacterSerializer
from .group import MainGroupSerializer


class GameSerializer(serializers.ModelSerializer):
    """Game serializer."""
    groups = SerializerMethodField()
    characters = SerializerMethodField()
    non_grouped = SerializerMethodField()
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
            'groups',
            'characters',
            'non_grouped',
            'open_applications',
            'open_character_list',
            'player_count',
        ]

    def get_groups(self, obj: Game):
        return MainGroupSerializer(
            obj.groups.filter(parent__isnull=True, hidden=False), many=True
        ).data

    def get_characters(self, obj: Game):
        return CharacterSerializer(
            Character.objects.filter(group__game=obj),
            many=True
        ).data

    def get_player_count(self, obj: Game):
        return Character.objects.filter(group__game=obj).count()

    def get_non_grouped(self, obj: Game):
        return CharacterSerializer(
            Character.objects.filter(
                group__game=obj, group__hidden=True
            ), many=True
        ).data
