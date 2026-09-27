"""Application serializers module."""
from rest_framework import serializers
from config.api_schema import ApplicationAnswers

from apps.games.models import Application
from .character import CharacterSerializer


class ApplicationPublicSerializer(serializers.ModelSerializer):
    """Application serializer."""

    class Meta:
        """Serializer meta."""

        model = Application
        fields = [
            'id',
            # 'user',
            'game',
            'character',
            'status',
        ]
        read_only_fields = fields


class ApplicationPrivateSerializer(ApplicationPublicSerializer):
    """Application serializer."""
    answers = serializers.SerializerMethodField()
    character = CharacterSerializer(read_only=True, allow_null=True)

    class Meta:
        """Serializer meta."""

        model = Application
        fields = [
            'id',
            # 'user',
            'game',
            'character',
            'price',
            'payed',
            'answers',
            'status',
        ]
        read_only_fields = fields

    def get_answers(self, application: Application) -> ApplicationAnswers:
        """Gets application answers."""
        return {
            'values': {answer.question.id: answer.value for answer in application.answers.all()},
            'unfilled': application.unfilled(),
        }
