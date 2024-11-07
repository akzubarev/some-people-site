"""Question serializers module."""
from rest_framework import serializers

from apps.games.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """Question serializer."""

    class Meta:
        """Serializer meta."""

        model = Question
        fields = [
            'id',
            'title',
            'description',
            'type',
            'choices',
            'order',
        ]
