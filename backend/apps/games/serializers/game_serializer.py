from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.games.models import Game, Character
from .character_serializer import CharacterSerializer
from .faction_serializer import MainFactionSerializer


class GameSerializer(serializers.ModelSerializer):
    factions = SerializerMethodField()
    characters = SerializerMethodField()
    non_factioned = SerializerMethodField()

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
            'factions',
            'characters',
            'non_factioned',
            "open_applications",
            "open_character_list",
        ]

    def get_factions(self, obj: Game):
        return MainFactionSerializer(
            obj.factions.filter(parent__isnull=True, hidden=False), many=True
        ).data

    def get_characters(self, obj: Game):
        return CharacterSerializer(
            Character.objects.filter(faction__game=obj),
            many=True
        ).data

    def get_non_factioned(self, obj: Game):
        return CharacterSerializer(
            Character.objects.filter(
                faction__game=obj, faction__hidden=True
            ), many=True
        ).data
