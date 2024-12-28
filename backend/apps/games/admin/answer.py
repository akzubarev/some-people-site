"""Answer admin module."""
from django.contrib import admin

from apps.games.models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Answer admin."""

    ordering = ('-id',)
    list_display = [
        "id",
        "question",
        "application__user",
        "value",
    ]
