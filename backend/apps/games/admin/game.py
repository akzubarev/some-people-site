"""Game admin module."""
from django.contrib import admin

from apps.games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """Game admin."""

    ordering = ('-id',)
    list_display = [
        'id',
        'title',
        'description',
        'short_description',
        'price',
        'year',
        'location',
        'start',
        'end',
        # 'vk',
        # 'tg',
        'open_applications',
        'open_character_list',
    ]
