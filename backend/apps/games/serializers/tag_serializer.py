"""Tag serializers mudule."""
from rest_framework import serializers
from apps.games.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer."""

    class Meta:
        """Serializer meta."""

        model = Tag
        fields = [
            'id',
            'name',
            'color',
        ]
