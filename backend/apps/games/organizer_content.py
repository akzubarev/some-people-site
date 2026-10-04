"""Game-scoped organizer content, with shared authorization and revision checks."""
import hashlib
import json
from io import BytesIO
from uuid import uuid4

from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.core.files.base import ContentFile
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_field
from PIL import Image
from rest_framework import serializers, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from apps.users.models import User
from .models import Application, Character, Game, Group, Question, Tag


def model_permissions(user, model):
    active = user.is_authenticated and user.is_active and (user.is_staff or user.is_superuser)
    return {action: bool(active and user.has_perm(f'{model._meta.app_label}.{action}_{model._meta.model_name}'))
            for action in ('view', 'add', 'change', 'delete')}


def revision(instance):
    data = {field.attname: str(getattr(instance, field.attname)) for field in instance._meta.concrete_fields}
    for field in instance._meta.many_to_many:
        data[field.name] = list(getattr(instance, field.name).order_by('pk').values_list('pk', flat=True))
    return hashlib.sha256(json.dumps(data, sort_keys=True, cls=DjangoJSONEncoder).encode()).hexdigest()


class Conflict(APIException):
    status_code = 409
    default_detail = 'Запись уже изменена. Обновите данные перед сохранением.'


def audit(request, instance, action, fields=()):
    LogEntry.objects.log_actions(user_id=request.user.pk, queryset=[instance], action_flag=action,
        change_message=json.dumps([{'changed': {'fields': list(fields)}}] if action == CHANGE else
                                  [{'added' if action == ADDITION else 'deleted': {}}]), single_object=True)


class ContentPermission(BasePermission):
    def has_permission(self, request, view):
        rights = model_permissions(request.user, view.queryset.model)
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return rights['view'] or rights['change']
        if view.action == 'upload':
            return rights['add'] or rights['change']
        return rights[{'create': 'add', 'destroy': 'delete'}.get(view.action, 'change')]


class VersionedSerializer(serializers.ModelSerializer):
    revision = serializers.SerializerMethodField()
    expected_revision = serializers.CharField(write_only=True, required=False)
    acknowledge_shared = serializers.BooleanField(write_only=True, required=False, default=False)

    @extend_schema_field(str)
    def get_revision(self, obj):
        return revision(obj)

    def validate(self, attrs):
        expected = attrs.pop('expected_revision', None)
        if self.instance and expected != revision(self.instance):
            raise Conflict()
        attrs.pop('acknowledge_shared', None)
        return attrs

    def validate_image(self, image):
        if image is None:
            return None
        if image.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Максимальный размер — 5 МБ.')
        try:
            with Image.open(image) as source:
                if source.width * source.height > 16_000_000:
                    raise ValueError()
                output = BytesIO()
                source.convert('RGBA').save(output, 'PNG')
            return ContentFile(output.getvalue(), name=f'{uuid4().hex}.png')
        except (ValueError, OSError, Image.DecompressionBombError):
            raise serializers.ValidationError('Нужно изображение до 16 мегапикселей.')


VERSION_FIELDS = ('revision', 'expected_revision', 'acknowledge_shared')


class OrganizerGroupSerializer(VersionedSerializer):
    descendants = serializers.SerializerMethodField()
    character_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'alias', 'description', 'order', 'parent', 'family', 'hidden', 'image',
                  'descendants', 'character_count', *VERSION_FIELDS)

    @extend_schema_field(list[int])
    def get_descendants(self, obj):
        rows = list(Group.objects.filter(game_id=obj.game_id).values_list('id', 'parent_id'))
        found = {obj.pk}
        while True:
            next_ids = {pk for pk, parent in rows if parent in found} - found
            if not next_ids:
                return sorted(found - {obj.pk})
            found.update(next_ids)

    @extend_schema_field(int)
    def get_character_count(self, obj):
        ids = [obj.pk, *self.get_descendants(obj)]
        return Character.objects.filter(Q(group_id__in=ids) | Q(family_id__in=ids)).count()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        parent = attrs.get('parent', getattr(self.instance, 'parent', None))
        family = attrs.get('family', getattr(self.instance, 'family', False))
        seen = {self.instance.pk} if self.instance else set()
        while parent:
            if parent.pk in seen or parent.game_id != self.context['game'].pk or parent.family != family:
                raise serializers.ValidationError({'parent': 'Родитель должен быть того же типа и игры, без циклов.'})
            seen.add(parent.pk)
            parent = parent.parent
        if self.instance and family != self.instance.family:
            if self.instance.subgroups.exists() or self.instance.characters.exists() or self.instance.members.exists():
                raise serializers.ValidationError({'family': 'Сначала перенесите дочерние группы и персонажей.'})
        return attrs


class OrganizerCharacterSerializer(VersionedSerializer):
    assigned_application = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = ('id', 'name', 'name_eng', 'alias', 'description', 'order', 'group', 'family',
                  'master', 'image', 'tags', 'kventa', 'assigned_application', *VERSION_FIELDS)
        extra_kwargs = {'tags': {'required': False, 'allow_empty': True}}

    @extend_schema_field(serializers.IntegerField(allow_null=True))
    def get_assigned_application(self, obj):
        return Application.objects.filter(character=obj).values_list('id', flat=True).first()

    def validate_kventa(self, upload):
        if upload is None:
            return None
        if upload.size > 20 * 1024 * 1024 or upload.read(5) != b'%PDF-':
            raise serializers.ValidationError('Нужен PDF не больше 20 МБ.')
        upload.seek(0)
        upload.name = f'{uuid4().hex}.pdf'
        return upload

    def validate(self, attrs):
        attrs = super().validate(attrs)
        group = attrs.get('group', getattr(self.instance, 'group', None))
        family = attrs.get('family', getattr(self.instance, 'family', None))
        if not group and not family:
            raise serializers.ValidationError({'group': 'Укажите фракцию или семью этой игры.'})
        for key, related, is_family in [('group', group, False), ('family', family, True)]:
            if related and (related.game_id != self.context['game'].pk or related.family != is_family):
                raise serializers.ValidationError({key: 'Неверный тип группы или другая игра.'})
        master = attrs.get('master')
        if master and (not master.is_active or not (master.is_staff or master.is_superuser)):
            raise serializers.ValidationError({'master': 'Выберите действующего мастера.'})
        return attrs


class OrganizerTagSerializer(VersionedSerializer):
    color = serializers.RegexField(r'^#[0-9a-fA-F]{6}$')
    used_games = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'private', 'mg', 'used_games', *VERSION_FIELDS)

    @extend_schema_field(list[int])
    def get_used_games(self, obj):
        return sorted(set(x for pair in obj.characters.values_list('group__game_id', 'family__game_id')
                          for x in pair if x is not None))

    def validate(self, attrs):
        if self.instance and set(self.get_used_games(self.instance)) - {self.context['game'].pk}:
            if not attrs.get('acknowledge_shared'):
                raise serializers.ValidationError({'acknowledge_shared': 'Подтвердите изменение общего тега в других играх.'})
        return super().validate(attrs)


class OrganizerQuestionSerializer(VersionedSerializer):
    answer_count = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'title', 'description', 'type', 'choices', 'required', 'order', 'games',
                  'answer_count', *VERSION_FIELDS)
        extra_kwargs = {'games': {'required': False}}

    @extend_schema_field(int)
    def get_answer_count(self, obj):
        return obj.answers.count()

    def validate(self, attrs):
        if self.instance and self.instance.games.exclude(pk=self.context['game'].pk).exists():
            if not attrs.get('acknowledge_shared'):
                raise serializers.ValidationError({'acknowledge_shared': 'Этот вопрос общий для нескольких игр. Подтвердите изменение.'})
        attrs = super().validate(attrs)
        games = attrs.get('games', list(self.instance.games.all()) if self.instance else [self.context['game']])
        if self.context['game'] not in games:
            raise serializers.ValidationError({'games': 'Нельзя убрать вопрос из текущей игры при редактировании.'})
        if self.instance and self.instance.answers.exclude(application__game__in=games).exists():
            raise serializers.ValidationError({'games': 'Нельзя убрать игру, участники которой уже ответили на вопрос.'})
        attrs['games'] = games
        kind = attrs.get('type', getattr(self.instance, 'type', 'line'))
        choices = attrs.get('choices', getattr(self.instance, 'choices', None))
        if kind not in ('line', 'paragraph'):
            lists = choices if kind in ('matrix', 'matrix_checkbox') else [choices]
            if not isinstance(lists, list) or (kind in ('matrix', 'matrix_checkbox') and len(lists) != 2):
                raise serializers.ValidationError({'choices': 'Нужны варианты, а для таблицы — столбцы и строки.'})
            for values in lists:
                if not isinstance(values, list) or not values or len(values) > 100 or any(
                        not isinstance(v, str) or not v.strip() or len(v) > 500 for v in values):
                    raise serializers.ValidationError({'choices': 'Заполните каждый вариант (до 100 вариантов по 500 символов).'})
                if len(set(values)) != len(values):
                    raise serializers.ValidationError({'choices': 'Варианты должны отличаться.'})
        else:
            attrs['choices'] = None
        if self.instance and self.instance.answers.exists():
            if kind != self.instance.type or attrs.get('choices', choices) != self.instance.choices:
                raise serializers.ValidationError({'choices': 'На вопрос уже ответили. Создайте новый вместо изменения типа или вариантов.'})
        return attrs


class OrganizerMultipartSerializer(serializers.Serializer):
    payload = serializers.JSONField(help_text='JSON object using the resource request fields, including expected_revision for updates.')
    image = serializers.ImageField(required=False)
    kventa = serializers.FileField(required=False)


class ContentViewSet(viewsets.GenericViewSet):
    permission_classes = (ContentPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def game(self, lock=False):
        queryset = Game.objects.select_for_update() if lock else Game.objects.all()
        return get_object_or_404(queryset, pk=self.kwargs['game_id'])

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {**super().get_serializer_context(), 'game': self.game()}

    def get_throttles(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return []
        return super().get_throttles()

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        response['Cache-Control'] = 'no-store'
        return response

    def payload(self):
        if 'payload' not in self.request.data:
            return self.request.data
        try:
            result = json.loads(self.request.data['payload'])
            if not isinstance(result, dict):
                raise ValueError()
        except (ValueError, TypeError):
            raise serializers.ValidationError({'payload': 'Некорректные данные формы.'})
        return {**result, **dict(self.request.FILES.items())}

    def list(self, request, **kwargs):
        self.game()
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    def retrieve(self, request, **kwargs):
        return Response(self.get_serializer(self.get_object()).data)

    def create(self, request, **kwargs):
        with transaction.atomic():
            game = self.game(lock=True)
            serializer = self.get_serializer(data=self.payload())
            serializer.is_valid(raise_exception=True)
            instance = serializer.save(**({'game': game} if self.queryset.model == Group else {}))
            audit(request, instance, ADDITION)
            return Response(self.get_serializer(instance).data, status=201)

    def partial_update(self, request, **kwargs):
        with transaction.atomic():
            self.game(lock=True)
            instance = get_object_or_404(self.get_queryset().select_for_update(of=('self',)), pk=kwargs['pk'])
            serializer = self.get_serializer(instance, data=self.payload(), partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            audit(request, instance, CHANGE, serializer.validated_data)
            if getattr(self, 'contribution_reason', None):
                LogEntry.objects.log_actions(user_id=request.user.pk, queryset=[instance],
                    action_flag=CHANGE, change_message=self.contribution_reason, single_object=True)
            return Response(self.get_serializer(instance).data)

    def destroy(self, request, **kwargs):
        with transaction.atomic():
            self.game(lock=True)
            instance = get_object_or_404(self.get_queryset().select_for_update(of=('self',)), pk=kwargs['pk'])
            if self.payload().get('expected_revision') != revision(instance):
                raise Conflict()
            self.check_delete(instance)
            audit(request, instance, DELETION)
            instance.delete()
        return Response(status=204)


class OrganizerGroupViewSet(ContentViewSet):
    queryset = Group.objects.all()
    serializer_class = OrganizerGroupSerializer

    def get_queryset(self):
        return self.queryset.filter(game_id=self.kwargs['game_id']).order_by('order', 'id')

    def check_delete(self, obj):
        if obj.subgroups.exists() or obj.characters.exists() or obj.members.exists():
            raise serializers.ValidationError({'detail': 'Перенесите дочерние группы и персонажей перед удалением.'})


class OrganizerCharacterViewSet(ContentViewSet):
    queryset = Character.objects.all()
    serializer_class = OrganizerCharacterSerializer

    def get_queryset(self):
        return self.queryset.filter(Q(group__game_id=self.kwargs['game_id']) |
                                    Q(family__game_id=self.kwargs['game_id'])).order_by('order', 'id')

    def check_delete(self, obj):
        if Application.objects.filter(character=obj).exists() or obj.liked_by.exists():
            raise serializers.ValidationError({'detail': 'Персонаж связан с заявкой или избранным. Скройте его группу вместо удаления.'})


class OrganizerTagViewSet(ContentViewSet):
    queryset = Tag.objects.all().order_by('name', 'id')
    serializer_class = OrganizerTagSerializer

    def check_delete(self, obj):
        if obj.characters.exists():
            raise serializers.ValidationError({'detail': 'Сначала снимите тег с персонажей всех игр.'})


class OrganizerQuestionViewSet(ContentViewSet):
    queryset = Question.objects.all()
    serializer_class = OrganizerQuestionSerializer

    def get_queryset(self):
        return self.queryset.filter(games=self.kwargs['game_id']).order_by('order', 'id')

    def check_delete(self, obj):
        if obj.answers.exists() or obj.games.exclude(pk=self.kwargs['game_id']).exists():
            raise serializers.ValidationError({'detail': 'Нельзя удалить вопрос с ответами или связью с другой игрой.'})
