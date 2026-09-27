"""Game views module."""
from typing import Any

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from apps.games.models import Character, Game, Group, Tag
from apps.games.serializers import CharacterSerializer, GameSerializer, GroupSerializer, TagSerializer
from apps.games.visibility import public_characters, visible_group_ids
from apps.games.public_cache import cached_payload


@extend_schema_view(
    retrieve=extend_schema(parameters=[OpenApiParameter('id', str, OpenApiParameter.PATH,
        description='Game alias or numeric ID')]),
    characters=extend_schema(parameters=[OpenApiParameter('game_alias', str, required=True),
        OpenApiParameter('search', str), OpenApiParameter('tag', str)], responses=CharacterSerializer(many=True)),
    groups=extend_schema(parameters=[OpenApiParameter('game_alias', str, required=True)], responses=GroupSerializer(many=True)),
    tags=extend_schema(parameters=[OpenApiParameter('game_alias', str, required=True)], responses=TagSerializer(many=True)),
)
class GameViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Game viewset"""
    queryset = Game.objects
    serializer_class = GameSerializer
    permission_classes = (AllowAny,)
    throttle_classes = ()

    def public_response(self, request, scope, build):
        # Keep browsers/proxies from retaining visibility or consent changes.
        # Only the server payload cache is reused, after normal permission checks.
        response = Response(cached_payload(scope, request.build_absolute_uri(), build))
        response['Cache-Control'] = 'no-store'
        return response

    def published_game(self, request):
        games = Game.objects.all()
        if not request.user.is_staff:
            games = games.filter(open_character_list=True)
        return get_object_or_404(games, alias=request.query_params.get('game_alias'))

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets a games."""
        alias = self.kwargs['pk']
        instance = Game.objects.filter(alias=alias).first() or self.get_object()
        return self.public_response(request, instance.pk,
            lambda: self.serializer_class(instance, context={'request': request}).data)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets games list."""
        return self.public_response(request, 'index', lambda:
            self.serializer_class(self.get_queryset().order_by('-id'), context={'request': request}, many=True).data)

    @action(detail=False, methods=['get'])
    def characters(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets games characters."""
        game = self.published_game(request)
        def build():
            char_filter = character_filter(
                game_alias=game.alias, tag=request.GET.get('tag'), search=request.GET.get('search'),
            ).filter(pk__in=public_characters(game.pk).values('pk'))
            return CharacterSerializer(char_filter, many=True).data
        return self.public_response(request, game.pk, build)

    @action(detail=False, methods=['get'])
    def groups(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets games groups."""
        game = self.published_game(request)
        def build():
            visible = visible_group_ids(game.pk)
            groups = Group.objects.filter(pk__in=visible, parent__isnull=True)
            return GroupSerializer(groups, many=True, context={'visible_group_ids': visible}).data
        return self.public_response(request, game.pk, build)

    @action(detail=False, methods=['get'])
    def tags(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Gets games tags."""
        game = self.published_game(request)
        return self.public_response(request, game.pk, lambda: TagSerializer(
            Tag.objects.filter(characters__in=public_characters(game.pk)).distinct(), many=True).data)


def character_filter(game_alias: str, tag: str, search: str) -> QuerySet[Character]:
    """Filters characters by games, tag and search."""
    characters = Character.objects.filter(group__game__alias=game_alias)
    if tag is not None:
        characters = characters.filter(tags__name=tag)
    if search is not None:
        characters = characters.filter(Q(name__contains=search) | Q(alias__contains=search))
    return characters
