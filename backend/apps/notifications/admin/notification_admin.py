from django.contrib import admin

from apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'mailing',
        'user',
        'viewed'
    ]
    raw_id_fields = ['user']

    search_fields = [
        'user__first_name', 'user__last_name', 'user__email', 'user__id'
    ]
