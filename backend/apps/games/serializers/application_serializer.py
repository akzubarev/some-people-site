from rest_framework import serializers

from apps.games.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
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

    def get_answers(self, obj):
        answers = obj.answers.all()
        return {
            answer.question.id: answer.value
            for answer in answers
        }
