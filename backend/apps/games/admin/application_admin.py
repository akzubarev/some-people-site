from django.contrib import admin
from apps.games.models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "price",
        "payed",
        "game",
        "character",
        "status",
    ]
