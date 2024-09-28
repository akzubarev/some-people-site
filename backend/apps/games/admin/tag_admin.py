"""Tag admin module."""
from django.contrib import admin

from apps.games.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin."""

    ordering = ('-id',)
    list_display = [
        "id",
        "name",
        "color",
    ]
