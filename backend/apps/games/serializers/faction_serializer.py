"""Faction serializers module."""
from django.db.models import Count, Case, When, BooleanField
from rest_framework import serializers

from apps.games.models import Faction
from .character_serializer import CharacterSerializer


class FactionSerializer(serializers.ModelSerializer):
    """Faction serializer."""

    characters = serializers.SerializerMethodField()

    class Meta:
        """Serializer meta."""

        model = Faction
        fields = [
            'id',
            'name',
            'alias',
            'hidden',
            'description',
            'game',
            'parent',
            'characters',
            'image',
        ]

    def get_characters(self, obj):
        return CharacterSerializer(
            obj.characters.annotate(
                leader=Count(
                    Case(When(tags__name="Лидер", then=1),
                         default=0, output_field=BooleanField())
                )
            ).order_by("-leader"), many=True
        ).data


class MainFactionSerializer(FactionSerializer):
    """Main faction serializer."""

    subfactions = FactionSerializer(many=True)

    class Meta:
        """Serializer meta."""

        model = Faction
        fields = [
            'id',
            'name',
            'alias',
            'hidden',
            'description',
            'game',
            'parent',
            'characters',
            'image',
            'subfactions'
        ]
