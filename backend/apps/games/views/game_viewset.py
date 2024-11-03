"""Game views module."""
from typing import Any

from django.db.models import Q, QuerySet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.games.models import Character, Game, Tag
from apps.games.serializers import CharacterSerializer, GameSerializer, TagSerializer


class GameViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Game viewset"""
    queryset = Game.objects
    serializer_class = GameSerializer
    authentication_classes: list = []
    permission_classes = (AllowAny,)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets a game."""
        alias = request.get_full_path().split("/")[-2]
        instance = Game.objects.filter(alias=alias).first() or self.get_object()
        serializer = self.serializer_class(instance, context={'request': request})
        return Response(serializer.data)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets games list."""
        queryset = self.get_queryset().order_by("-id")
        serializer = self.serializer_class(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def characters(self, request: Request, *args: Any, **kwargs: Any) -> Response | PermissionDenied:
        """Gets game characters."""
        game_alias = request.GET.get('game_alias', None)
        game = Game.objects.filter(alias=game_alias).first()
        if request.user.is_staff is False and game.open_character_list is False:
            return PermissionDenied('Сетка ролей еще не опубликована')
        char_filter = character_filter(
            game_alias=game_alias,
            tag=request.GET.get('tag', None),
            search=request.GET.get('search', None),
        )
        serializer = CharacterSerializer(char_filter, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def tags(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets game tags."""
        game_alias = request.GET.get("game_alias", None)
        characters = Character.objects.filter(group__game__alias=game_alias)
        tags = Tag.objects.filter(characters__in=characters).distinct()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)


def character_filter(game_alias: str, tag: str, search: str) -> QuerySet[Character]:
    """Filters characters by game, tag and search."""
    characters = Character.objects.filter(group__game__alias=game_alias)
    if tag is not None:
        characters = characters.filter(tags__name=tag)
    if search is not None:
        characters = characters.filter(Q(name__contains=search) | Q(alias__contains=search))
    return characters
