"""Users viewset."""
from http import HTTPStatus
from typing import Any, Type

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from apps.games.models import Character
from apps.games.visibility import public_characters
from apps.users.models import User
from apps.users.serializers import UserCreateSerializer, UserPrivateSerializer, UserPublicSerializer
from apps.users.serializers.user.private import UserProfileUpdateSerializer
from apps.users.telegram_link import issue_link
from rest_framework.throttling import UserRateThrottle


class TelegramLinkThrottle(UserRateThrottle):
    scope = 'telegram_link'
    rate = '5/minute'


class CharacterLikeSerializer(serializers.Serializer):
    game_alias = serializers.CharField(max_length=20)
    character_id = serializers.IntegerField(min_value=1)
    like = serializers.BooleanField()


class UserViewSet(viewsets.GenericViewSet):
    """Users viewset."""

    serializer_class = UserPublicSerializer
    queryset = User.objects
    permission_classes = [AllowAny]
    lookup_field = "uuid"

    def get_serializer_class(self) -> Type[Serializer]:
        """Gets serializer class based on action."""
        match self.action:
            case 'register':
                return UserCreateSerializer
            case 'me':
                return UserPrivateSerializer
            case 'update_me':
                return UserProfileUpdateSerializer
            case _:
                return self.serializer_class

    @action(['get'], detail=False)
    def me(self, request: Request, *args: Any, **kwargs: Any):
        """Makes an action for current user based on query action."""
        if request.user.is_anonymous:
            return Response(data={}, status=HTTPStatus.NO_CONTENT)
        return Response(UserPrivateSerializer(request.user, context={'request': request}).data)

    @action(['put'], detail=False, permission_classes=[IsAuthenticated])
    def update_me(self, request: Request, *args: Any, **kwargs: Any):
        """Makes an action for current user based on query action."""
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserPrivateSerializer(request.user, context={'request': request}).data)

    @action(['post'], detail=False, permission_classes=[IsAuthenticated], throttle_classes=[TelegramLinkThrottle])
    def telegram_link(self, request):
        code = issue_link(request.user)
        response = Response({'code': code, 'expires_in': 600,
                             'url': f'https://t.me/Somepeopllarpebot?start={code}'})
        response['Cache-Control'] = 'no-store'
        return response

    @action(methods=['post'], detail=False, authentication_classes=[])
    @transaction.atomic
    def register(self, request: Request) -> Response:
        """Create a new user."""
        if request.user.is_authenticated:
            raise PermissionDenied()
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.set_password(request.data['password'])
        user.save()

        token, created = Token.objects.get_or_create(user=user_serializer.instance)
        response_data = dict(user_serializer.data) | {'auth_token': token.key}
        return Response(response_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def players(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieves the list of players for a games by alias."""
        game_alias = request.GET.get("game_alias")
        queryset = User.objects.filter(applications__game__alias=game_alias)
        serializer = self.get_serializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def mg(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieves the list of master group users."""
        queryset = User.objects.filter(is_staff=True).exclude(username="admin")
        serializer = self.get_serializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def like_character(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Likes or dislikes a character."""
        serializer = CharacterLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        game_alias, character_id, like = data.get('game_alias'), data.get('character_id'), data.get('like')
        characters = Character.objects.filter(group__game__alias=game_alias)
        if not request.user.is_staff:
            characters = characters.filter(group__game__open_character_list=True)
        character = get_object_or_404(characters, id=character_id)
        if not public_characters(character.group.game_id).filter(pk=character.pk).exists():
            raise NotFound()
        if like:
            character.liked_by.add(request.user)
        else:
            character.liked_by.remove(request.user)
        return Response(data={'status': 'ok'}, status=HTTPStatus.OK)
