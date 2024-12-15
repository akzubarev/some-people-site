"""Script for uploading characters from google sheet."""
import os
import sys
from logging import getLogger

import django
import gspread
import requests
from django.core.files.base import ContentFile

if __name__ == '__main__':
    sys.path[0] = '/app/'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

from apps.games.models import Game, Character, Question, Tag, Group
from apps.users.models import User
from utils.text_utils import readable_exception

logger = getLogger(__name__)
google_creds = gspread.api_key(os.getenv('GOOGLE_API_KEY'))
games_data = {
    'spreadsheet_id': '1ucdOv6Hid9toTFUSuTSNRh7z7wpeY2dgCkIOuZtgrz4',
    # 'spreadsheet_id': '1y1k7p41v9C7sSDES4Ojs1AOERYsXrnosQeKNoDgnxNI',
    'frostpunk': {
        'groups_worksheet_id': '1746120384', 'characters_worksheet_id': '2055553822',
        # 'questions_worksheet_id': '1440140115',
    },
    'whales': {
        'groups_worksheet_id': '1687216792', 'characters_worksheet_id': '26168715',
        'questions_worksheet_id': '1440140115',
    },
}

_images_cache: dict = {}


def get_image(path: str, order: int, target: str) -> ContentFile | None:
    if not path:
        return None
    if path in _images_cache.keys():
        return _images_cache[path]
    download_media_headers: dict = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 '
                      'YaBrowser/22.5.3.673 Yowser/2.5 Safari/537.36',
    }
    try:
        response = requests.get(path, timeout=5, headers=download_media_headers)
    except requests.exceptions.SSLError:
        response = requests.get(path, timeout=5, headers=download_media_headers, verify=False)
    file = ContentFile(response.content, f'{target}_{order}.png')
    _images_cache[path] = file
    return file


def _get_worksheet(spreadsheet_id: str, worksheet_id: str) -> gspread.Worksheet:
    """Get a worksheet from Google Spreadsheet."""
    return google_creds.open_by_key(key=spreadsheet_id).get_worksheet_by_id(id=worksheet_id)


def load_game(game_alias: str):
    """Load games characters from google sheet."""
    game = Game.objects.get(alias=game_alias)
    get_groups(game=game, worksheet=_get_worksheet(
        spreadsheet_id=games_data['spreadsheet_id'],
        worksheet_id=games_data[game_alias]['groups_worksheet_id'],
    ))
    get_characters(game=game, worksheet=_get_worksheet(
        spreadsheet_id=games_data['spreadsheet_id'],
        worksheet_id=games_data[game_alias]['characters_worksheet_id'],
    ))
    if 'questions_worksheet_id' in games_data[game_alias]:
        get_questions(game=game, worksheet=_get_worksheet(
            spreadsheet_id=games_data['spreadsheet_id'],
            worksheet_id=games_data[game_alias]['questions_worksheet_id'],
        ))


def get_groups(game: Game, worksheet: gspread.Worksheet) -> None:
    """Parses the groups from google sheet."""
    num_rows = len([item for item in worksheet.col_values(1) if item])
    rows: list[list] = worksheet.get_values(f'A2:G{num_rows}')
    for i, row in enumerate(rows):
        try:
            order, name, description, parent_group_name, *_ = row
            hidden = row[4] == 'TRUE'
            family = row[5] == 'TRUE'
            parent_group = Group.objects.get(name=parent_group_name, family=family) if parent_group_name else None
            group, _ = Group.objects.update_or_create(
                name=name, game_id=game.id, family=family,
                defaults={'hidden': hidden, 'description': description, 'parent': parent_group, 'order': order},
            )
            group.save()
        except Exception as e:
            logger.warning(group)
            logger.warning(readable_exception(e))


def get_characters(game: Game, worksheet: gspread.Worksheet) -> None:
    """Parses the characters from google sheet."""
    num_rows = len([item for item in worksheet.col_values(1) if item])
    rows: list[list] = worksheet.get_values(f'A2:I{num_rows}')
    for i, row in enumerate(rows):
        try:
            name_with_alias = row[1].split(', ')
            character_name = name_with_alias[0]
            alias = name_with_alias[1] if len(name_with_alias) > 1 else '-'
            order, _, name_eng, master, tags, group_name, family_name, description, *_ = row
            image = get_image(path=row[8], target='character', order=order) if len(row) > 8 else None

            group = Group.objects.get(name=group_name, game_id=game.id, family=False) \
                if group_name and group_name != '-' else None
            family = Group.objects.get(name=family_name, game_id=game.id, family=True) \
                if family_name and family_name != '-' else None
            master_obj = User.objects.filter(is_staff=True, first_name=master).first()
            char, _ = Character.objects.update_or_create(
                name=character_name,
                defaults={
                    'alias': alias, 'image': image, 'description': description,
                    'group': group, 'family': family, 'order': order, 'name_eng': name_eng,
                    'master': master_obj,
                },
            )
            for tag in tags.split(', '):
                tag, _ = Tag.objects.get_or_create(name=tag)
                char.tags.add(tag)
            char.save()
        except Exception as e:
            logger.warning(group_name)
            logger.warning(family_name)
            logger.warning(readable_exception(e))


def get_questions(game: Game, worksheet: gspread.Worksheet) -> None:
    """Parses the questions from google sheet."""
    num_rows = len([item for item in worksheet.col_values(1) if item])
    rows: list[list] = worksheet.get_values(f'A2:F{num_rows}')
    for i, row in enumerate(rows):
        # try:
        order, title, description, question_type, choices, line_options, *_ = row
        choices = [choice.strip('\n').strip() for choice in choices.split(';')]
        if '' in choices:
            choices.remove('')
        if line_options:
            line_options = [line_option.strip(' \n').strip() for line_option in line_options.split(';')]
            if '' in line_options:
                line_options.remove('')
            choices = [choices, line_options]
        question, _ = Question.objects.update_or_create(
            order=order,
            defaults={
                'title': title, 'description': description, 'choices': choices,
                'type': {
                    'Строка': 'line',
                    'Абзац': 'paragraph',
                    'Одиночный выбор': 'single_choice',
                    'Множественный выбор': 'multiple_choice',
                    'Шкала': 'scale',
                    'Сетка': 'matrix',
                    'Сетка Флажков': 'matrix_checkbox',
                }[question_type]
            },
        )
        question.games.add(game)
        question.save()
        # except Exception as e:
        #     logger.warning(readable_exception(e))


def load_chars():
    """Entrypoint for loading games characters."""
    for game_alias in ['frostpunk', 'whales']:
        load_game(game_alias=game_alias)


if __name__ == '__main__':
    load_chars()
