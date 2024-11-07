"""Notification serializers package."""
from rest_framework import serializers

from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Notification model serializer."""

    class Meta:
        """Serializer metadata"""
        model = Notification
        fields = [
            'user',
            'mailing',
            'viewed',
            'created_at'
        ]
        read_only_fields = fields
