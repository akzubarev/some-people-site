"""Application admin module."""
from django.contrib import admin
from django.utils.html import format_html

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
        'likes',
        'status',
    ]

    def likes(self, application: Application) -> str:
        return format_html('<br>'.join([str(characters) for characters in application.user.likes.all()]))
