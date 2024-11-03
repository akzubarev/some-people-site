"""Script for uploading characters from google sheet."""
import os
import sys
from logging import getLogger

import django
import gspread

sys.path[0] = '/app/'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.games.models import Game, Character, Tag, Group
from utils.text_utils import readable_exception

logger = getLogger(__name__)
google_creds = gspread.api_key(os.getenv('GOOGLE_API_KEY'))
games_data = {
    'spreadsheet_id': '1y1k7p41v9C7sSDES4Ojs1AOERYsXrnosQeKNoDgnxNI',
    'frostpunk': {'groups_worksheet_id': '1746120384', 'characters_worksheet_id': '2055553822'},
    'whales': {'groups_worksheet_id': '1687216792', 'characters_worksheet_id': '26168715'},
}


def _get_worksheet(spreadsheet_id: str, worksheet_id: str) -> gspread.Worksheet:
    """Get a worksheet from Google Spreadsheet."""
    return google_creds.open_by_key(key=spreadsheet_id).get_worksheet_by_id(id=worksheet_id)


def load_game(game_alias: str):
    """Load game characters from google sheet."""
    game = Game.objects.get(alias=game_alias)
    get_groups(game=game, worksheet=_get_worksheet(
        spreadsheet_id=games_data['spreadsheet_id'],
        worksheet_id=games_data[game_alias]['groups_worksheet_id'],
    ))
    get_characters(game=game, worksheet=_get_worksheet(
        spreadsheet_id=games_data['spreadsheet_id'],
        worksheet_id=games_data[game_alias]['characters_worksheet_id'],
    ))


def get_groups(game: Game, worksheet: gspread.Worksheet) -> None:
    num_rows = len([item for item in worksheet.col_values(1) if item])
    rows: list[list] = worksheet.get_values(f'A2:F{num_rows}')
    for i, row in enumerate(rows):
        # try:
        name, description, parent_group_name, hidden = row[0], row[1], row[2], row[3] == 'TRUE'
        image = row[4] if len(row) > 4 else None
        parent_group = Group.objects.get(name=parent_group_name) if parent_group_name else None
        group, _ = Group.objects.update_or_create(
            name=name, game_id=game.id,
            defaults={'hidden': hidden, 'image': image, 'description': description, 'parent': parent_group},
        )
        group.save()
    # except Exception as e:
    #     logger.warning(readable_exception(e))


def get_characters(game: Game, worksheet: gspread.Worksheet) -> None:
    num_rows = len([item for item in worksheet.col_values(1) if item])
    rows: list[list] = worksheet.get_values(f'A2:F{num_rows}')
    for i, row in enumerate(rows):
        # try:
        name_with_alias = row[0].split(', ')
        character_name = name_with_alias[0]
        alias = name_with_alias[1] if len(name_with_alias) > 1 else '-'
        master, tags, group_name, description = row[1], row[2], row[3], row[4]
        image = row[5] if len(row) > 5 else None
        group = Group.objects.get(name=group_name, game_id=game.id)
        char, _ = Character.objects.update_or_create(
            name=character_name,
            defaults={
                'alias': alias, 'image': image, 'description': description, 'group': group,
                'master_id': {'Леша': 2, 'Настя': 3, 'Аня': 4, 'Катя': 5, 'Лиза': 6}.get(master, None)
            },
        )
        for tag in tags.split(', '):
            tag, _ = Tag.objects.get_or_create(name=tag)
            char.tags.add(tag)
        char.save()
    # except Exception as e:
    #     logger.warning(readable_exception(e))


def load_chars():
    """Entrypoint for loading game characters."""
    for game_alias in ['frostpunk', 'whales']:
        load_game(game_alias=game_alias)


if __name__ == '__main__':
    load_chars()
