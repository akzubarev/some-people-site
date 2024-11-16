"""Notifications admin module."""
from django.contrib import admin

from apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notifications admin."""

    ordering = ('-id',)
    list_filter = ['mailing', 'sent', 'viewed', 'user__username']
    list_display = [
        'id',
        'mailing',
        'user',
        'sent',
        'viewed',
    ]
    raw_id_fields = ['user']

    search_fields = [
        'user__first_name', 'user__last_name', 'user__email', 'user__id'
    ]
