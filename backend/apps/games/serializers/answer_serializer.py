"""Answers serializers module."""
from rest_framework import serializers

from apps.games.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    """Answers serializer."""

    class Meta:
        """Serializer meta."""

        model = Answer
        fields = [
            'id',
            'question',
            'application',
            'value',
        ]
