"""Application views module."""
from typing import Any

from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.games.models import Answer, Application, Game, Question
from apps.games.serializers import ApplicationSerializer


class ApplicationsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Application viewset."""

    queryset = Application.objects
    serializer_class = ApplicationSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets an application."""
        serializer = self.serializer_class(self.get_object(), context={'request': request})
        return Response(serializer.data)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets list of applications."""
        game_alias = request.GET.get("game_alias", None)
        queryset = self.get_queryset()
        if game_alias is not None:
            queryset = queryset.filter(game__alias=game_alias)
        serializer = self.serializer_class(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets an application."""
        user_id = request.GET.get("user_id")
        game_alias = request.GET.get("game_alias")
        application = Application.objects.filter(user__id=user_id, game__alias=game_alias).first()
        serializer = self.serializer_class(application, context={'request': request})
        return Response(serializer.data)

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def apply(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Creates an application."""
        user, data = request.user, request.data
        game = Game.objects.filter(alias=data.pop("game_alias")).first()
        application, _ = Application.objects.get_or_create(user=user, game=game)
        for question_name, answer_value in data.items():
            question_id = question_name.split("_")[-1]
            question = Question.objects.filter(id=question_id).first()
            answer, _ = Answer.objects.get_or_create(question=question, application=application)
            answer.value = answer_value
            answer.save()
        serializer = self.serializer_class(application, context={'request': request})
        return Response(serializer.data)
