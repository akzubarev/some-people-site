"""Question serializers module."""
from rest_framework import serializers
from config.api_schema import QuestionChoicesField

from apps.games.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """Question serializer."""
    choices = QuestionChoicesField(read_only=True, allow_null=True)

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
            'required',
        ]
        read_only_fields = fields
