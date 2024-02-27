from django.contrib import admin
from apps.games.models import Faction


@admin.register(Faction)
class FactionAdmin(admin.ModelAdmin):
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
