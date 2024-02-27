from rest_framework import serializers
from ..models import Telegram


class TelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telegram
        fields = ['code', 'chat_id', 'username', 'settings']
        read_only_fields = ['code', 'chat_id', 'username']
