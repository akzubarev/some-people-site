"""Question admin module."""
from django.contrib import admin
from apps.games.models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Question admin."""

    ordering = ('-id',)
    list_filter = ['games__alias']
    list_display = [
        'id',
        'title',
        # 'games',
        'description',
        'type',
        'choices',
        'order',
    ]
