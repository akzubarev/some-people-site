from rest_framework import serializers

from ..models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'user',
            'mailing',
            'viewed',
            'created_at'
        ]
        read_only_fields = fields
