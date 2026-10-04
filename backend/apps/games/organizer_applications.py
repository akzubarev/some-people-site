"""Organizer application detail, assignment and contributions use one record."""
from django.db.models import Q
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Application, Character
from .organizer_content import ContentViewSet, VersionedSerializer, VERSION_FIELDS


class OrganizerApplicationSerializer(VersionedSerializer):
    player = serializers.SerializerMethodField()
    missing_questions = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    reason = serializers.CharField(write_only=True, required=False, max_length=500)
    payed = serializers.IntegerField(min_value=0, required=False)
    price = serializers.IntegerField(min_value=0, allow_null=True, required=False)

    class Meta:
        model = Application
        fields = ('id', 'game', 'player', 'status', 'character', 'price', 'payed', 'missing_questions',
                  'answers', 'likes', 'reason', *VERSION_FIELDS)
        read_only_fields = ('game',)

    @extend_schema_field(serializers.DictField())
    def get_player(self, obj):
        return {'id': obj.user_id, 'name': str(obj.user), 'telegram': bool(obj.user.telegram_chat_id)}

    @extend_schema_field(list[int])
    def get_missing_questions(self, obj):
        return obj.unfilled()

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_answers(self, obj):
        if self.context['view'].action == 'list':
            return []
        return list(obj.answers.filter(question__games=obj.game).values('question_id', 'value'))

    @extend_schema_field(list[int])
    def get_likes(self, obj):
        return list(obj.user.likes.filter(Q(group__game=obj.game) | Q(family__game=obj.game))
                    .values_list('id', flat=True))

    def validate(self, attrs):
        attrs = super().validate(attrs)
        reason = attrs.pop('reason', '').strip()
        if any(key in attrs and attrs[key] != getattr(self.instance, key) for key in ('price', 'payed')):
            if not reason:
                raise serializers.ValidationError({'reason': 'Укажите причину изменения взноса.'})
            self.context['view'].contribution_reason = reason
        character = attrs.get('character')
        if character:
            character = Character.objects.select_for_update().get(pk=character.pk)
            game_id = self.context['game'].pk
            linked_games = {g for g in (getattr(character.group, 'game_id', None),
                                        getattr(character.family, 'game_id', None)) if g is not None}
            if linked_games != {game_id}:
                raise serializers.ValidationError({'character': 'Персонаж должен относиться к этой игре.'})
            if Application.objects.filter(character=character).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError({'character': 'Персонаж уже назначен другой заявке.'})
            if attrs.get('status', self.instance.status) == Application.Status.DELETED:
                raise serializers.ValidationError({'character': 'Нельзя назначить персонажа удалённой заявке.'})
        return attrs


class OrganizerApplicationViewSet(ContentViewSet):
    queryset = Application.objects.all()
    serializer_class = OrganizerApplicationSerializer
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_queryset(self):
        return self.queryset.filter(game_id=self.kwargs['game_id']).select_related('user').order_by('id')
