from rest_framework import serializers

from ..models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        try:
            del getattr(obj.Types, obj.key).image
        except:
            pass
        ntype = {}
        try:
            ntype = obj.type
        except:
            pass
        return ntype

    class Meta:
        model = Notification
        fields = [
            'telegram', 'viewed',
            'type', 'created_at'
        ]
        read_only_fields = fields
