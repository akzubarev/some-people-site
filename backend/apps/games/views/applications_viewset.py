"""Application views module."""
from typing import Any

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from apps.games.models import Answer, Application, Game
from apps.games.serializers import ApplicationPrivateSerializer


class ApplicationsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Application viewset."""

    queryset = Application.objects
    serializer_class = ApplicationPrivateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets an application."""
        serializer = self.serializer_class(self.get_object(), context={'request': request})
        return Response(serializer.data)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets list of applications."""
        game_alias = request.GET.get('game_alias', None)
        queryset = self.get_queryset()
        if game_alias is not None:
            queryset = queryset.filter(game__alias=game_alias)
        serializer = self.serializer_class(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets an application."""
        user_id = request.GET.get('user_id')
        if user_id is not None and user_id != str(request.user.pk):
            raise ValidationError({'user_id': 'Only your own application may be requested.'})
        game_alias = request.GET.get('game_alias')
        application = self.get_queryset().filter(game__alias=game_alias).first()
        if application is None:
            return Response({})
        serializer = self.serializer_class(application, context={'request': request})
        return Response(serializer.data)

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def apply(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Creates an application."""
        user, data = request.user, request.data
        game = Game.objects.filter(alias=data.pop('game_alias')).first()
        application, _ = Application.objects.get_or_create(user=user, game=game)
        for question_name, answer_value in data.items():
            question_id = question_name.split('_')[-1]
            answer, _ = Answer.objects.update_or_create(
                question_id=question_id, application=application,
                defaults={'value': answer_value}
            )
        serializer = self.serializer_class(application, context={'request': request})
        return Response(serializer.data)

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Deletes an application."""
        user, game_alias = request.user, request.data.get('game_alias')
        application = get_object_or_404(self.get_queryset(), game__alias=game_alias)
        application.status = Application.Status.DELETED
        application.save()
        serializer = self.serializer_class(application, context={'request': request})
        return Response(serializer.data)

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def restore(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Restores an application."""
        user, game_alias = request.user, request.data.get('game_alias')
        application = get_object_or_404(self.get_queryset(), game__alias=game_alias)
        application.status = Application.Status.PENDING
        application.save()
        serializer = self.serializer_class(application, context={'request': request})
        return Response(serializer.data)
