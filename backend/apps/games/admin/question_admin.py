from django.contrib import admin
from apps.games.models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "description",
        "type",
        "choices",
        "order",
    ]
