"""Questions views module."""
from typing import Any

from rest_framework import mixins, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from apps.games.models import Question
from apps.games.serializers import QuestionSerializer


class QuestionsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Questions viewset."""
    queryset = Question.objects
    serializer_class = QuestionSerializer

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets a question."""
        serializer = self.serializer_class(self.get_object(), context={'request': request})
        return Response(serializer.data)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets questions list."""
        game_alias = request.GET.get("game_alias", None)
        queryset = self.get_queryset()
        if game_alias is not None:
            queryset = queryset.filter(games__alias=game_alias)
        serializer = self.serializer_class(queryset, context={'request': request}, many=True)
        return Response(serializer.data)
