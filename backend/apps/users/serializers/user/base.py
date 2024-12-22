"""User serializers module."""
from rest_framework import serializers

from apps.games.serializers import ApplicationPublicSerializer
from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    applications = serializers.SerializerMethodField()
    mg = serializers.SerializerMethodField()
    telegram = serializers.SerializerMethodField()

    class Meta:
        """Serializer meta."""
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'uuid',
            'mg', 'phone', 'vk', 'telegram', 'created_at', 'avatar', 'applications',
        )
        read_only_fields = (
            'id', 'email', 'uuid', 'created_at', 'updated_at', 'applications', 'telegram',
        )

    def get_applications(self, user: User) -> dict[str, dict]:
        """Gets users applications."""
        return {
            application.game.alias: ApplicationPublicSerializer(application).data
            for application in user.applications.all()
        }

    def get_mg(self, user: User) -> bool:
        """Gets user mg status."""
        return user.is_superuser or user.is_staff

    def get_telegram(self, user: User) -> str:
        """Gets users telegram username."""
        return user.telegram_username if user.tg_public else None
