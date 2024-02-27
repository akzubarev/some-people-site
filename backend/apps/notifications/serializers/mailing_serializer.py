from rest_framework import serializers

from ..models import Mailing


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = [
            'text',
            'image',
            'private',
            'entry_level',
            'locales',
            # 'created_at'
        ]
        # read_only_fields = fields
