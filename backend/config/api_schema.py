"""Shared schema shapes for JSON fields and action responses."""
from typing import TypedDict
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

AnswerValue = str | list[str] | list[list[str]] | None


class ApplicationAnswers(TypedDict):
    values: dict[str, AnswerValue]
    unfilled: list[int]


@extend_schema_field({
    'oneOf': [
        {'type': 'array', 'items': {'type': 'string'}},
        {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'string'}}},
    ], 'nullable': True,
})
class QuestionChoicesField(serializers.JSONField):
    pass


class GameAliasSerializer(serializers.Serializer):
    game_alias = serializers.CharField(max_length=20)


class TelegramLinkSerializer(serializers.Serializer):
    code = serializers.CharField()
    expires_in = serializers.IntegerField()
    url = serializers.URLField()


class StatusSerializer(serializers.Serializer):
    status = serializers.CharField()


APPLICATION_INPUT_SCHEMA = {
    'type': 'object',
    'required': ['game_alias'],
    'properties': {'game_alias': {'type': 'string'}},
    'additionalProperties': {
        'nullable': True,
        'oneOf': [
            {'type': 'string'},
            {'type': 'array', 'items': {'type': 'string'}},
            {'type': 'array', 'items': {'type': 'array', 'items': {'type': 'string'}}},
        ],
    },
    'description': 'Partial draft: game_alias and question_<id> answer keys. '
                   'Only questions belonging to the selected game are accepted.',
}
