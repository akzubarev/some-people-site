"""Mailing serializers module."""
from rest_framework import serializers

from apps.notifications.models import Mailing


class MailingSerializer(serializers.ModelSerializer):
    """Mailing model serializer."""

    class Meta:
        """Serializer metadata."""
        model = Mailing
        fields = [
            'text',
            'image',
            # 'created_at'
        ]
        # read_only_fields = fields
