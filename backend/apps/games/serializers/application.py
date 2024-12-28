"""Application serializers module."""
from rest_framework import serializers

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


class ApplicationPrivateSerializer(ApplicationPublicSerializer):
    """Application serializer."""
    answers = serializers.SerializerMethodField()
    character = CharacterSerializer(required=False)

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

    def get_answers(self, application: Application) -> dict[str, dict[int, dict] | list[int]]:
        """Gets application answers."""
        return {
            'values': {answer.question.id: answer.value for answer in application.answers.all()},
            'unfilled': [
                question.id for question in application.game.questions.filter(required=True)
                if not (answer := question.answers.filter(application=application).first()) or
                   (answer and not answer.filled)
            ],
        }
