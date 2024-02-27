from django.contrib import admin

from ..models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'telegram',
        'user',
        'key',
        'data',
        'created_at'
    ]
    raw_id_fields = ['user']

    search_fields = [
        'user__first_name', 'user__last_name', 'user__email', 'user__id',
        'user__telegram__chat_id', 'user__telegram__username'
    ]
