from rest_framework import serializers

from apps.games.serializers import ApplicationSerializer
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    telegram = serializers.SerializerMethodField()
    applications = serializers.SerializerMethodField()
    mg = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'email_active', 'first_name',
            'last_name', 'uuid', 'mg',
            'phone', 'created_at', 'avatar', 'telegram', 'applications',
            'country_iso', 'instagram', 'country',
        )
        read_only_fields = (
            'id', 'email', 'email_active', 'uuid', 'created_at', 'telegram',
            'updated_at',  'applications',  'country',
        )

    def get_telegram(self, obj):
        try:
            return obj.telegram.username
        except AttributeError:
            return ''

    def get_applications(self, obj):
        applications = obj.applications.all()
        return {
            application.game.alias: ApplicationSerializer(application).data
            for application in applications
        }

    def get_mg(self, obj):
        return obj.is_superuser or obj.is_staff
