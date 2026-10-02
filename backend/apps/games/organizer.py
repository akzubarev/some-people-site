"""Organizer game access and explicit, transactional content mutations."""
import hashlib
import json

from django.conf import settings
from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_field
from rest_framework import serializers, viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from .models import Game


GAME_FIELDS = (
    'title', 'alias', 'description', 'short_description', 'price', 'player_count',
    'location', 'year', 'start', 'end', 'open_character_list', 'open_applications', 'vk', 'tg',
)


def game_revision(game):
    content = {name: getattr(game, name) for name in GAME_FIELDS}
    return hashlib.sha256(json.dumps(content, cls=DjangoJSONEncoder, sort_keys=True).encode()).hexdigest()


def game_permissions(user):
    organizer = user.is_authenticated and user.is_active and (user.is_staff or user.is_superuser)
    return {action: bool(organizer and user.has_perm(f'games.{action}_game'))
            for action in ('view', 'add', 'change')}


class OrganizerGamePermission(BasePermission):
    """One policy for the shell, read endpoints and write endpoints."""
    def has_permission(self, request, view):
        permissions = game_permissions(request.user)
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return permissions['view'] or permissions['change']
        return permissions['add'] if view.action == 'create' else permissions['change']


class EditConflict(APIException):
    status_code = 409
    default_detail = 'Игра изменена другим организатором. Обновите данные перед сохранением.'


class OrganizerGameSerializer(serializers.ModelSerializer):
    revision = serializers.SerializerMethodField()
    expected_revision = serializers.CharField(write_only=True, required=False, max_length=64)
    alias = serializers.RegexField(r'^[a-z][a-z0-9-]*$', max_length=20)
    price = serializers.IntegerField(min_value=0, required=False, allow_null=True)
    player_count = serializers.IntegerField(min_value=0, required=False, allow_null=True)

    class Meta:
        model = Game
        fields = ('id', *GAME_FIELDS, 'revision', 'expected_revision')
        read_only_fields = ('id',)

    @extend_schema_field(str)
    def get_revision(self, obj):
        return game_revision(obj)

    def validate_alias(self, value):
        if value in {'groups', 'characters', 'tags', 'new'}:
            raise serializers.ValidationError('Этот алиас зарезервирован.')
        matches = Game.objects.filter(alias__iexact=value)
        if self.instance:
            matches = matches.exclude(pk=self.instance.pk)
        if matches.exists():
            raise serializers.ValidationError('Этот алиас уже используется.')
        return value

    def validate(self, attrs):
        start = attrs.get('start', getattr(self.instance, 'start', None))
        end = attrs.get('end', getattr(self.instance, 'end', None))
        if start and end and end <= start:
            raise serializers.ValidationError({'end': 'Конец игры должен быть позже начала.'})
        if self.instance:
            revision = attrs.pop('expected_revision', None)
            if not revision:
                raise serializers.ValidationError({'expected_revision': 'Обновите страницу перед сохранением.'})
            if revision != game_revision(self.instance):
                raise EditConflict()
        else:
            attrs.pop('expected_revision', None)
            # Creation is a draft; publication is a separate explicit update.
            if attrs.get('open_applications') or attrs.get('open_character_list'):
                raise serializers.ValidationError({'detail': 'Сначала создайте игру с закрытыми заявками и сеткой.'})
        return attrs


class GamePermissionsSerializer(serializers.Serializer):
    view = serializers.BooleanField()
    add = serializers.BooleanField()
    change = serializers.BooleanField()


class OrganizerGameIndexSerializer(serializers.Serializer):
    games = OrganizerGameSerializer(many=True)
    permissions = GamePermissionsSerializer()
    timezone = serializers.CharField()


class OrganizerGameViewSet(viewsets.GenericViewSet):
    queryset = Game.objects.all()
    serializer_class = OrganizerGameSerializer
    permission_classes = (OrganizerGamePermission,)
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        response['Cache-Control'] = 'no-store'
        return response

    @extend_schema(responses=OrganizerGameIndexSerializer)
    def list(self, request):
        return Response({'games': self.get_serializer(self.get_queryset(), many=True).data,
                         'permissions': game_permissions(request.user), 'timezone': settings.TIME_ZONE})

    def retrieve(self, request, pk=None):
        return Response(self.get_serializer(self.get_object()).data)

    def audit(self, instance, action, fields):
        LogEntry.objects.log_actions(
            user_id=self.request.user.pk,
            queryset=[instance], action_flag=action,
            change_message=json.dumps([{'added': {}}] if action == ADDITION else
                                      [{'changed': {'fields': list(fields)}}]),
            single_object=True,
        )

    @extend_schema(responses={201: OrganizerGameSerializer})
    def create(self, request):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                self.audit(instance, ADDITION, ())
        except IntegrityError as error:
            if getattr(getattr(error.__cause__, 'diag', None), 'constraint_name', None) != 'game_alias_unique_ci':
                raise
            raise serializers.ValidationError({'alias': 'Этот алиас уже используется.'}) from error
        return Response(self.get_serializer(instance).data, status=201)

    @extend_schema(responses={200: OrganizerGameSerializer, 409: None})
    def partial_update(self, request, pk=None):
        try:
            with transaction.atomic():
                instance = get_object_or_404(self.get_queryset().select_for_update(), pk=pk)
                self.check_object_permissions(request, instance)
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                changed = [name for name, value in serializer.validated_data.items()
                           if getattr(instance, name) != value]
                instance = serializer.save()
                if changed:
                    self.audit(instance, CHANGE, changed)
        except IntegrityError as error:
            if getattr(getattr(error.__cause__, 'diag', None), 'constraint_name', None) != 'game_alias_unique_ci':
                raise
            raise serializers.ValidationError({'alias': 'Этот алиас уже используется.'}) from error
        return Response(self.get_serializer(instance).data)
