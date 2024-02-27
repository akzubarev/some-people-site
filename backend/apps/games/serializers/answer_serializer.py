from rest_framework import serializers

from apps.games.models import Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'question',
            'application',
            'value',
        ]
