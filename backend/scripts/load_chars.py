"""Script for uploading characters from google sheet."""
import os
import sys
from logging import getLogger

import django
import gspread

sys.path[0] = '/app/'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.games.models import Game, Character, Tag, Faction
from utils.text_utils import readable_exception

logger = getLogger(__name__)
google_creds = gspread.api_key(os.getenv('GOOGLE_API_KEY'))
games_data = {
    'frostpunk': {
        'spreadsheet_id': '1y1k7p41v9C7sSDES4Ojs1AOERYsXrnosQeKNoDgnxNI',
        'worksheet_id': '2055553822',
    },
    'whales': {
        'spreadsheet_id': '1y1k7p41v9C7sSDES4Ojs1AOERYsXrnosQeKNoDgnxNI',
        'worksheet_id': '26168715',
    },
}


def _get_worksheet(spreadsheet_id: str, worksheet_id: str) -> gspread.Worksheet:
    """Get a worksheet from Google Spreadsheet."""
    return google_creds.open_by_key(key=spreadsheet_id).get_worksheet_by_id(id=worksheet_id)


def load_game(game_alias: str):
    """Load game characters from google sheet."""
    game = Game.objects.get(alias=game_alias)
    try:
        worksheet = _get_worksheet(
            spreadsheet_id=games_data[game_alias]['spreadsheet_id'],
            worksheet_id=games_data[game_alias]['worksheet_id'],
        )
        num_rows = len([item for item in worksheet.col_values(1) if item])
        rows: list[list] = worksheet.get_values(f'A2:F{num_rows}')
        for i, row in enumerate(rows):
            try:
                ch_al = row[0].split(', ')
                character_name = ch_al[0]
                alias = ch_al[1] if len(ch_al) > 1 else '-'
                master, tags, fraction, description, char_id = row[1], row[2], row[3], row[4], row[5]
                char, _ = Character.objects.get_or_create(name=character_name, alias=alias, char_id=char_id)
                for tag in tags.split(', '):
                    tag, _ = Tag.objects.get_or_create(name=tag)
                    char.tags.add(tag)
                faction, _ = Faction.objects.get_or_create(name=fraction, game=game)
                char.faction = faction
                char.description = description
                char.master_id = {'Леша': 2, 'Настя': 3, 'Аня': 4, 'Катя': 5, 'Лиза': 6}.get(master, None)
                char.save()
            except Exception as e:
                logger.warning(readable_exception(e))

    except Exception as e:
        logger.warning(readable_exception(e))


def load_chars():
    """Entrypoint for loading game characters."""
    for game_alias in ['frostpunk', 'whales']:
        load_game(game_alias=game_alias)


if __name__ == '__main__':
    load_chars()
