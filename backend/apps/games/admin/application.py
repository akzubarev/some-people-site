"""Application admin module."""
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html

from apps.games.models import Application
from scripts.export_applications import export_apps


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Application admin."""

    change_list_template = "games/applications_changelist.html"
    ordering = ('-id',)
    list_filter = ['game', 'user__username', 'status', 'payed']
    list_display = [
        'id',
        'user_str',
        'price',
        'payed',
        'game',
        'character',
        'likes',
        'status',
    ]

    def likes(self, application: Application) -> str:
        return format_html('<br>'.join([str(characters) for characters in application.user.likes.all()]))

    @admin.display
    def user_str(self, application: Application) -> str:
        user = application.user
        return f'{user.username} ({user.first_name} {user.last_name})'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('export/', self.export),
        ]
        return my_urls + urls

    def export(self, request):
        export_apps()
        return HttpResponseRedirect("../")

    def unfinished(self, request):
        export_apps()
        return HttpResponseRedirect("../")
