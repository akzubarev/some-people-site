"""Script for uploading characters from google sheet."""
import json
import os
import sys
from logging import getLogger
from typing import Collection

import django
import gspread
from gspread import Client, Worksheet, service_account_from_dict
from gspread.utils import ValueInputOption

if __name__ == '__main__':
    sys.path[0] = '/app/'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

from apps.games.models import Answer, Application, Question

logger = getLogger(__name__)
games_data = {
    'spreadsheet_id': '1obEoiPrtLyIpVdWVODDfNz1gBeQ6EiDFRel82j_e584',
    'whales': {'applications_worksheet_id': '418879773', 'unfinished_worksheet_id': '1018078207'},
}


def _get_google_credentials() -> Client:
    """Получаем аккаунт для взаимодействия с гугл-таблицами."""
    return service_account_from_dict(info=json.loads(os.getenv('GOOGLE_CREDS')))


def _get_worksheet(spreadsheet_id: str, worksheet_id: str) -> gspread.Worksheet:
    """Get a worksheet from Google Spreadsheet."""
    google_creds = _get_google_credentials()
    return google_creds.open_by_key(key=spreadsheet_id).get_worksheet_by_id(id=worksheet_id)


def _get_answer_value(answer: Answer | None, question: Question) -> list[str]:
    if not answer or not answer.value:
        return ['' for _ in get_titles(question)]
    value = answer.value
    if isinstance(value, list):
        if len(value) > 0 and isinstance(value[0], list):
            return [','.join(v) for v in value]
        return [','.join(value)]
    return [value]


def get_titles(question: Question) -> list:
    if isinstance(question.choices, list) and len(question.choices) == 2 and isinstance(question.choices[1], list):
        return [f'{question.title} [{choice}]' for choice in question.choices[1]]
    return [question.title]


def _make_title(questions: Collection[Question]):
    title = ['Кто']
    for question in questions:
        title.extend(get_titles(question=question))
    return title


def upload_applications(worksheet: Worksheet, game_alias: str) -> None:
    questions = Question.objects.filter(games__alias=game_alias).order_by('order')
    applications = Application.objects.filter(game__alias=game_alias).exclude(
        status=Application.Status.DELETED,
    ).order_by('id')
    title = _make_title(questions=questions)
    rows = []
    for application in applications:
        answers = {answer.question_id: answer for answer in application.answers.all()}
        answers_values = []
        for question in questions:
            answers_values.extend(_get_answer_value(answer=answers.get(question.id), question=question))
        rows.append([str(application.user)] + answers_values)
    if rows:
        worksheet.clear()
        worksheet.append_rows(
            values=[title, *rows], value_input_option=ValueInputOption.user_entered,
        )
        logger.info(f'Выгружено {len(applications)} заявок.')


def upload_unfinished(worksheet: Worksheet, game_alias: str) -> None:
    title = ['Игрок', 'Неотвеченные вопросы']
    rows = []
    questions = Question.objects.filter(games__alias=game_alias).order_by('order')
    applications = Application.objects.filter(game__alias=game_alias).exclude(
        status=Application.Status.DELETED,
    ).order_by('id')
    for application in applications:
        unfilled_ids = application.unfilled(only_questionnaire=True)
        if unfilled_ids:
            unfilled_questions = questions.filter(id__in=unfilled_ids).values_list('title', flat=True)
            rows.append([str(application.user), ', '.join(unfilled_questions)])
    if rows:
        worksheet.clear()
        worksheet.append_rows(
            values=[title, *rows], value_input_option=ValueInputOption.user_entered,
        )


def export_finished():
    """Entrypoint for loading games characters."""
    for game_alias in [
        # 'frostpunk',
        'whales'
    ]:
        upload_applications(
            game_alias=game_alias, worksheet=_get_worksheet(
                spreadsheet_id=games_data['spreadsheet_id'],
                worksheet_id=games_data[game_alias]['applications_worksheet_id'],
            ),
        )


def export_unfinished():
    """Entrypoint for loading games characters."""
    for game_alias in [
        # 'frostpunk',
        'whales'
    ]:
        upload_unfinished(
            game_alias=game_alias, worksheet=_get_worksheet(
                spreadsheet_id=games_data['spreadsheet_id'],
                worksheet_id=games_data[game_alias]['unfinished_worksheet_id'],
            ),
        )


def export_apps():
    export_finished()
    # export_unfinished()


if __name__ == '__main__':
    export_apps()
