"""User serializers module."""
from rest_framework import serializers

from apps.games.serializers import ApplicationSerializer
from apps.users.models import User
from config.settings import DEBUG


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    telegram = serializers.SerializerMethodField()
    applications = serializers.SerializerMethodField()
    mg = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        """Serializer meta."""
        model = User
        fields = (
            'id', 'email', 'username', 'email_active', 'first_name',
            'last_name', 'uuid', 'mg', 'phone', 'created_at', 'avatar',
            'telegram', 'applications', 'country_iso', 'instagram', 'country',
        )
        read_only_fields = (
            'id', 'email', 'email_active', 'uuid', 'created_at', 'telegram',
            'updated_at', 'applications', 'country',
        )

    def get_telegram(self, user: User) -> str:
        """Gets users telegram username."""
        try:
            return user.telegram_username
        except AttributeError:
            return ''

    def get_applications(self, user: User) -> dict[str, dict]:
        """Gets users applications."""
        return {
            application.game.alias: ApplicationSerializer(application).data
            for application in user.applications.all()
        }

    def get_mg(self, user: User) -> bool:
        """Gets user mg status."""
        return user.is_superuser or user.is_staff

    def get_avatar(self, user: User) -> str | None:
        """Gets user avatar."""
        if not user.avatar:
            return None
        if DEBUG:
            return user.avatar.path.replace('/app', 'http://v1.admin.some-people.localhost:1337')
        return user.avatar.path
