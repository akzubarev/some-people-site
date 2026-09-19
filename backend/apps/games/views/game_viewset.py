"""Game views module."""
from typing import Any

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.games.models import Character, Game, Group, Tag
from apps.games.serializers import CharacterSerializer, GameSerializer, GroupSerializer, TagSerializer
from apps.games.visibility import public_characters, visible_group_ids


class GameViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Game viewset"""
    queryset = Game.objects
    serializer_class = GameSerializer
    permission_classes = (AllowAny,)

    def published_game(self, request):
        games = Game.objects.all()
        if not request.user.is_staff:
            games = games.filter(open_character_list=True)
        return get_object_or_404(games, alias=request.query_params.get('game_alias'))

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
    def characters(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets games characters."""
        game = self.published_game(request)
        char_filter = character_filter(
            game_alias=request.GET.get('game_alias', None),
            tag=request.GET.get('tag', None), search=request.GET.get('search', None),
        )
        char_filter = char_filter.filter(pk__in=public_characters(game.pk).values('pk'))
        serializer = CharacterSerializer(char_filter, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def groups(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets games groups."""
        game = self.published_game(request)
        visible = visible_group_ids(game.pk)
        groups = Group.objects.filter(pk__in=visible, parent__isnull=True)
        return Response(GroupSerializer(groups, many=True, context={'visible_group_ids': visible}).data)

    @action(detail=False, methods=['get'])
    def tags(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets games tags."""
        game = self.published_game(request)
        tags = Tag.objects.filter(characters__in=public_characters(game.pk)).distinct()
        return Response(TagSerializer(tags, many=True).data)


def character_filter(game_alias: str, tag: str, search: str) -> QuerySet[Character]:
    """Filters characters by games, tag and search."""
    characters = Character.objects.filter(group__game__alias=game_alias)
    if tag is not None:
        characters = characters.filter(tags__name=tag)
    if search is not None:
        characters = characters.filter(Q(name__contains=search) | Q(alias__contains=search))
    return characters
