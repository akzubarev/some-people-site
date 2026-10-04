"""Read-only mailing records; composition belongs to the organizer cabinet."""
from django.contrib import admin
from django.utils.html import format_html, strip_tags
from apps.notifications.models import Mailing


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = ('id', 'game', 'ready', 'display_text', 'time')
    search_fields = ('text',)
    readonly_fields = ('organizer_link', 'display_text', 'game', 'ready', 'time', 'confirmed_at',
                       'created_at', 'updated_at')
    fields = readonly_fields

    def display_text(self, obj):
        return strip_tags(obj.text or '')

    def organizer_link(self, obj):
        if obj.game_id:
            return format_html('<a href="/organizer/{}/mailings/{}">Открыть в кабинете организатора</a>', obj.game_id, obj.pk)
        return 'Архивная рассылка без привязки к игре'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
