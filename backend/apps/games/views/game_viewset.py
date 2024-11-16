"""Game views module."""
from typing import Any

from django.db.models import Q, QuerySet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.games.models import Character, Game, Group, Tag
from apps.games.serializers import CharacterSerializer, GameSerializer, GroupSerializer, TagSerializer
from utils.decorators import roles_open


class GameViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Game viewset"""
    queryset = Game.objects
    serializer_class = GameSerializer
    authentication_classes: list = []
    permission_classes = (AllowAny,)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets a games."""
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
    # @roles_open
    def characters(self, request: Request, *args: Any, **kwargs: Any) -> Response | PermissionDenied:
        """Gets games characters."""
        char_filter = character_filter(
            game_alias=request.GET.get('game_alias', None),
            tag=request.GET.get('tag', None), search=request.GET.get('search', None),
        )
        serializer = CharacterSerializer(char_filter, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    # @roles_open
    def groups(self, request: Request, *args: Any, **kwargs: Any) -> Response | PermissionDenied:
        """Gets games groups."""
        game_alias = request.GET.get('game_alias', None)
        groups = Group.objects.filter(game__alias=game_alias, parent__isnull=True)
        return Response(GroupSerializer(groups, many=True).data)

    @action(detail=False, methods=['get'])
    def tags(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets games tags."""
        game_alias = request.GET.get("game_alias", None)
        tags = Tag.objects.filter(characters__group__game__alias=game_alias).distinct()
        return Response(TagSerializer(tags, many=True).data)


def character_filter(game_alias: str, tag: str, search: str) -> QuerySet[Character]:
    """Filters characters by games, tag and search."""
    characters = Character.objects.filter(group__game__alias=game_alias)
    if tag is not None:
        characters = characters.filter(tags__name=tag)
    if search is not None:
        characters = characters.filter(Q(name__contains=search) | Q(alias__contains=search))
    return characters
