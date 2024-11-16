"""Group serializers module."""
from django.db.models import Count, Case, When, BooleanField
from rest_framework import serializers

from apps.games.models import Group
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

    def get_characters(self, group: Group) -> list[dict]:
        return CharacterSerializer(
            group.characters.annotate(
                leader=Count(
                    Case(When(tags__name="Лидер", then=1),
                         default=0, output_field=BooleanField())
                )
            ).order_by("-leader"), many=True
        ).data
    def get_members(self, group: Group) -> list[dict]:
        return CharacterSerializer(
            group.members.annotate(
                leader=Count(
                    Case(When(tags__name="Лидер", then=1),
                         default=0, output_field=BooleanField())
                )
            ).order_by("-leader"), many=True
        ).data

    def get_subgroups(self, group: Group) -> list[dict]:
        return GroupSerializer(group.subgroups, many=True).data
