from rest_framework import serializers
from apps.users.models import User


class UserSmallSerializer(serializers.ModelSerializer):
    email_hidden = serializers.SerializerMethodField()

    def get_email_hidden(self, obj):
        hide_chars = 3
        max_width = 15
        try:
            hidden_email = obj.email.split('@')[0][0:(0 if len(
                obj.email.split('@')[
                    0]) < max_width else max_width) - hide_chars]
            return hidden_email + '*' * hide_chars + '@' + \
                obj.email.split('@')[1]
        except IndexError:
            return ''

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email_hidden', 'created_at',
            'country_iso')
        read_only_fields = fields
