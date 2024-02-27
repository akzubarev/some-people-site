from django.contrib import admin

from ..models import ChatData


@admin.register(ChatData)
class ChatDataAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'chat_id',
        'user_id',
        'created_at'
    ]

    search_fields = ['user_id', 'chat_id']
