"""Character admin module."""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from apps.games.models import Character
from scripts.load_chars import load_chars


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """Character admin."""

    change_list_template = "games/characters_changelist.html"
    ordering = ('-id',)
    list_filter = ['group__name', 'group__game__title', 'master__username']
    list_display = [
        'id',
        'order',
        'name',
        'name_eng',
        'alias',
        'description',
        'group',
        'family',
        'application__user',
        'master',
        'image',
        # 'liked_by',
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('reload/', self.reload),
        ]
        return my_urls + urls

    def reload(self, request):
        load_chars()
        return HttpResponseRedirect("../")
