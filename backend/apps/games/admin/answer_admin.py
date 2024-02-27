from django.contrib import admin
from apps.games.models import Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "question",
        "value",
    ]
