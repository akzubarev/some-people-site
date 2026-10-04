"""Explicit draft, audience preview and idempotent mailing confirmation."""
import hashlib
import json

from django.db import transaction, IntegrityError
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_field
import nh3
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.games.models import Application
from apps.users.models import User
from .telegram_html import telegram_html
from telegram.constants import MessageLimit
from django.utils.html import strip_tags
from html import unescape
from apps.games.organizer_content import (ContentViewSet, VersionedSerializer, VERSION_FIELDS,
                                          Conflict, revision, audit, CHANGE)
from .models import Mailing, Notification
from .editor import EditorUploadForm, save_editor_image


def audience(mailing):
    return list(mailing.applications.filter(game=mailing.game).exclude(status='deleted')
                .filter(user__is_active=True).exclude(user__telegram_chat_id__isnull=True)
                .exclude(user__telegram_chat_id='').order_by('id').values('id', 'user_id', 'user__telegram_chat_id'))


def audience_revision(mailing, rows):
    return hashlib.sha256(json.dumps([revision(mailing), rows], sort_keys=True).encode()).hexdigest()


class OrganizerMailingSerializer(VersionedSerializer):
    applications = serializers.PrimaryKeyRelatedField(many=True, queryset=Application.objects.all(), required=False)
    delivery = serializers.SerializerMethodField()
    text = serializers.CharField(max_length=30000)

    class Meta:
        model = Mailing
        fields = ('id', 'text', 'time', 'applications', 'ready', 'confirmed_at', 'delivery', *VERSION_FIELDS)
        read_only_fields = ('ready', 'confirmed_at')

    @extend_schema_field(serializers.DictField())
    def get_delivery(self, obj):
        return {'total': obj.notifications.count(), 'sent': obj.notifications.filter(sent=True).count(),
            'failed': obj.notifications.exclude(last_error='').count(),
            'recipients': list(obj.notifications.order_by('id').values('user_id', 'sent', 'attempts', 'last_attempt_at', 'last_error'))}

    def validate_text(self, value):
        cleaned = nh3.clean(value, tags={'p', 'br', 'strong', 'em', 'u', 's', 'h1', 'h2', 'h3',
            'ul', 'ol', 'li', 'blockquote', 'pre', 'code', 'a', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'hr', 'img'},
            attributes={'a': {'href', 'title'}, 'img': {'src', 'alt'}, 'td': {'colspan', 'rowspan'},
                        'th': {'colspan', 'rowspan'}}, url_schemes={'http', 'https', 'mailto', 'tg'})
        plain = unescape(strip_tags(telegram_html(cleaned, base_url=f'https://{settings.DOMAIN}/')))
        if not plain.strip() or len(plain) > MessageLimit.MAX_TEXT_LENGTH:
            raise serializers.ValidationError('Нужен непустой текст до 4096 символов после форматирования.')
        return cleaned

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if self.instance and self.instance.ready:
            raise serializers.ValidationError({'detail': 'Подтверждённую рассылку нельзя редактировать. Создайте новую.'})
        if any(app.game_id != self.context['game'].pk for app in attrs.get('applications', [])):
            raise serializers.ValidationError({'applications': 'Все заявки должны принадлежать выбранной игре.'})
        return attrs

    def create(self, validated_data):
        return super().create({**validated_data, 'game': self.context['game'], 'ready': False})


class MailingImageSerializer(serializers.Serializer):
    image = serializers.ImageField()


class MailingImageResultSerializer(serializers.Serializer):
    url = serializers.CharField()


class MailingPreviewSerializer(serializers.Serializer):
    selected = serializers.IntegerField()
    eligible = serializers.IntegerField()
    audience_revision = serializers.CharField()
    application_ids = serializers.ListField(child=serializers.IntegerField())


class MailingConfirmSerializer(serializers.Serializer):
    audience_revision = serializers.CharField()
    idempotency_key = serializers.UUIDField()


class OrganizerMailingViewSet(ContentViewSet):
    queryset = Mailing.objects.all()
    serializer_class = OrganizerMailingSerializer

    @extend_schema(request=MailingImageSerializer, responses=MailingImageResultSerializer)
    @action(detail=False, methods=['post'])
    def upload(self, request, **kwargs):
        self.game()
        form = EditorUploadForm({}, request.FILES)
        if not form.is_valid():
            raise serializers.ValidationError(form.errors)
        try:
            return Response({'url': save_editor_image(form.cleaned_data['image'])}, status=201)
        except DjangoValidationError as error:
            raise serializers.ValidationError({'image': error.messages})

    def get_queryset(self):
        return self.queryset.filter(game_id=self.kwargs['game_id']).order_by('-id')

    def check_delete(self, obj):
        if obj.ready or obj.notifications.exists():
            raise serializers.ValidationError({'detail': 'Рассылка уже подтверждена.'})

    @extend_schema(responses=MailingPreviewSerializer)
    @action(detail=True, methods=['get'])
    def preview(self, request, **kwargs):
        mailing = self.get_object()
        rows = audience(mailing)
        return Response({'selected': mailing.applications.count(), 'eligible': len(rows),
            'audience_revision': audience_revision(mailing, rows), 'application_ids': [row['id'] for row in rows]})

    @extend_schema(request=MailingConfirmSerializer, responses=OrganizerMailingSerializer)
    @action(detail=True, methods=['post'])
    def confirm(self, request, **kwargs):
        params = MailingConfirmSerializer(data=request.data)
        params.is_valid(raise_exception=True)
        with transaction.atomic():
            self.game(lock=True)
            mailing = get_object_or_404(self.get_queryset().select_for_update(), pk=kwargs['pk'])
            key = params.validated_data['idempotency_key']
            if mailing.ready:
                if mailing.confirmation_key != key:
                    raise Conflict('Рассылка уже подтверждена.')
                return Response(self.get_serializer(mailing).data)
            apps = list(mailing.applications.order_by('id').select_for_update())
            list(User.objects.filter(pk__in=[app.user_id for app in apps]).order_by('pk').select_for_update())
            rows = audience(mailing)
            if audience_revision(mailing, rows) != params.validated_data['audience_revision']:
                raise Conflict('Состав получателей изменился. Проверьте предпросмотр заново.')
            if not rows:
                raise serializers.ValidationError({'detail': 'Нет доступных получателей. Пустой выбор никому не отправляется.'})
            if Mailing.objects.filter(confirmation_key=key).exists():
                raise serializers.ValidationError({'idempotency_key': 'Этот ключ уже использован.'})
            user_ids = sorted({row['user_id'] for row in rows})
            mailing.users.set(user_ids)
            mailing.ready = True
            mailing.confirmation_key = key
            mailing.confirmed_at = timezone.now()
            try:
                with transaction.atomic():
                    mailing.save()
            except IntegrityError:
                raise Conflict('Ключ подтверждения уже использован другой рассылкой.')
            Notification.objects.bulk_create([Notification(mailing=mailing, user_id=pk) for pk in user_ids])
            audit(request, mailing, CHANGE, ['ready', 'time', 'users'])
            return Response(self.get_serializer(mailing).data)
