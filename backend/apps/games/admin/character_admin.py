from django.contrib import admin
from apps.games.models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "alias",
        "description",
        "faction",
        "master",
        "image",
    ]
