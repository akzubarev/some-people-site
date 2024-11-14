"""Character admin module."""
from django.contrib import admin

from apps.games.models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """Character admin."""

    ordering = ('-id',)
    list_filter = ['game__alias', 'master__username']
    list_display = [
        'id',
        'name',
        'alias',
        'description',
        'group',
        'master',
        'image',
    ]
