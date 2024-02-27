from rest_framework import serializers

from apps.games.models import Character, Application
from .tag_serializer import TagSerializer
from .application_serializer import ApplicationSerializer
from apps.users.models import User


class CharacterSerializer(serializers.ModelSerializer):
    applications = ApplicationSerializer(many=True)
    tags = TagSerializer(many=True)
    player = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = [
            'id',
            'name',
            'alias',
            'description',
            'master',
            'image',
            'applications',
            'player',
            'tags',
        ]

    def get_player(self, obj):
        from apps.users.serializers import UserSerializer
        player = User.objects.filter(
            applications__character=obj,
            applications__status=Application.Status.CONFIRMED
        ).first()
        if player is not None:
            return UserSerializer(player).data
        else:
            return None
