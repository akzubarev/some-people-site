"""Application admin module."""
from django.contrib import admin

from apps.games.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Application admin."""

    ordering = ('-id',)
    list_filter = ['game', 'user__username']
    list_display = [
        'id',
        'user',
        'price',
        'payed',
        'game',
        'character',
        'status',
    ]
