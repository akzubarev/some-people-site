"""Validate partial questionnaire saves before writing any answers."""
from rest_framework.exceptions import ValidationError
from apps.games.models import Question


def validated_answers(game, data):
    questions = {question.pk: question for question in game.questions.all()}
    answers = {}
    errors = {}
    for key, value in data.items():
        if key == 'game_alias':
            continue
        try:
            question_id = int(key.removeprefix('question_'))
            question = questions[question_id] if key == f'question_{question_id}' else None
        except (ValueError, KeyError):
            question = None
        if question is None:
            errors[key] = 'Неизвестный вопрос для этой игры.'
            continue
        choices = question.choices or []
        kind = question.type
        # Empty values are saved as drafts; required/unfilled is calculated separately.
        valid = value is None
        if kind in (Question.Type.LINE, Question.Type.PARAGRAPH):
            valid = value is None or isinstance(value, str) and len(value) <= 20000
        elif kind in (Question.Type.SINGLE_CHOICE, Question.Type.SCALE):
            valid = value in (None, '') or isinstance(value, str) and value in choices
        elif kind == Question.Type.MULTIPLE_CHOICE:
            valid = value is None or (isinstance(value, list) and
                all(isinstance(item, str) and item in choices for item in value) and
                len(value) == len(set(value)))
        elif kind in (Question.Type.MATRIX, Question.Type.MATRIX_CHECKBOX):
            columns, rows = choices if len(choices) == 2 else ([], [])
            valid = isinstance(value, list) and len(value) == len(rows)
            if valid:
                valid = all(isinstance(row, list) and
                    all(isinstance(item, str) and item in columns for item in row) and
                    len(row) == len(set(row)) and
                    (kind == Question.Type.MATRIX_CHECKBOX or len(row) <= 1)
                    for row in value)
        if not valid:
            errors[key] = 'Ответ не соответствует типу вопроса или доступным вариантам.'
        else:
            answers[question_id] = value
    if errors:
        raise ValidationError(errors)
    return answers
