"""Character admin module."""
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import path
from django.views.decorators.http import require_POST

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
            path('reload/', self.admin_site.admin_view(require_POST(self.reload))),
        ]
        return my_urls + urls

    def reload(self, request):
        if not self.has_change_permission(request):
            raise PermissionDenied
        load_chars()
        return HttpResponseRedirect("../")
