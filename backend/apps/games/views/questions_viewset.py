from rest_framework import mixins, viewsets
from rest_framework.response import Response

from apps.games.models import Question
from apps.games.serializers import QuestionSerializer


class QuestionsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Question.objects
    serializer_class = QuestionSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance,
                                           context={'request': request})
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        game_alias = request.GET.get("game_alias", None)
        queryset = self.get_queryset()
        if game_alias is not None:
            queryset = queryset.filter(game__alias=game_alias)
        serializer = self.serializer_class(
            queryset, context={'request': request}, many=True
        )
        return Response(serializer.data)
