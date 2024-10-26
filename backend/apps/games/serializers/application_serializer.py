"""Application serializers module."""
from rest_framework import serializers

from apps.games.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    """Application serializer."""
    answers = serializers.SerializerMethodField()

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

    def get_answers(self, application: Application) -> dict[int, dict]:
        """Gets application answers."""
        return {answer.question.id: answer.value for answer in application.answers.all()}
