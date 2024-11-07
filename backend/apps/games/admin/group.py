"""Group admin module."""
from django.contrib import admin

from apps.games.models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Group admin."""

    ordering = ('-id',)
    list_display = [
        "id",
        "name",
        "alias",
        "hidden",
        "description",
        "game",
        "parent",
        "image",
    ]
