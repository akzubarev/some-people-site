"""Group serializers module."""
from django.db.models import Count, Case, When, BooleanField
from rest_framework import serializers

from apps.games.models import Group
from .character_serializer import CharacterSerializer


class GroupSerializer(serializers.ModelSerializer):
    """Group serializer."""

    characters = serializers.SerializerMethodField()

    class Meta:
        """Serializer meta."""

        model = Group
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


class MainGroupSerializer(GroupSerializer):
    """Main group serializer."""

    subgroups = GroupSerializer(many=True)

    class Meta:
        """Serializer meta."""

        model = Group
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
            'subgroups'
        ]
