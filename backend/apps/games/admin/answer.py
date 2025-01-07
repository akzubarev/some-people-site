"""Answer admin module."""
from django.contrib import admin

from apps.games.models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Answer admin."""

    ordering = ('-id',)
    list_filter = ['application__user__username']
    list_display = [
        'id',
        'question',
        'user_str',
        'value',
    ]

    @admin.display
    def user_str(self, answer: Answer) -> str:  # type: ignore
        user = answer.application.user
        return f'{user.username} ({user.first_name} {user.last_name})'
