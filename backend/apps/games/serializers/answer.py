"""Answers serializers module."""
import json

from rest_framework import serializers

from apps.games.models import Answer, Question


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
            'filled',
        ]
