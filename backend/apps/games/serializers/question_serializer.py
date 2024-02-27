from rest_framework import serializers

from apps.games.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id',
            'title',
            'description',
            'type',
            'choices',
            'order',
        ]
