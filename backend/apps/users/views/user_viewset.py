"""Users viewset."""
from http import HTTPStatus
from typing import Any, Type

from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from apps.games.models import Character
from apps.users.models import User
from apps.users.serializers import UserCreateSerializer, UserPrivateSerializer, UserPublicSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
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
            case 'me' | 'update_me':
                return UserPrivateSerializer
            case _:
                return self.serializer_class

    def get_object(self) -> User:
        if self.action in ['me', 'update_me']:
            return self.request.user
        else:
            return super().get_object()

    @action(['get'], detail=False)
    def me(self, request: Request, *args: Any, **kwargs: Any):
        """Makes an action for current user based on query action."""
        # if request.user.is_anonymous:
        #     return Response(data={}, status=HTTPStatus.NO_CONTENT)
        return self.retrieve(request, *args, **kwargs)

    @action(['put'], detail=False)
    def update_me(self, request: Request, *args: Any, **kwargs: Any):
        """Makes an action for current user based on query action."""
        return self.update(request, *args, **kwargs)

    @action(methods=['post'], detail=False, authentication_classes=[])
    @transaction.atomic
    def register(self, request: Request) -> Response:
        """Create a new user."""
        if request.user.is_authenticated:
            PermissionDenied()
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.set_password(request.data['password'])
        user.save()

        token, created = Token.objects.get_or_create(user=user_serializer.instance)
        response_data = dict(user_serializer.data) | {'auth_token': token.key}
        return Response(response_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieves a user."""
        serializer = self.get_serializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieves the list of users."""
        serializer = self.get_serializer(self.get_queryset(), context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def players(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieves the list of players for a games by alias."""
        game_alias = request.GET.get("game_alias")
        queryset = User.objects.filter(applications__game__alias=game_alias)
        serializer = self.get_serializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def mg(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieves the list of master group users."""
        queryset = User.objects.filter(is_staff=True).exclude(username="admin")
        serializer = self.get_serializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def like_character(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Likes or dislikes a character."""
        data = request.data
        game_alias, character_id, like = data.get('game_alias'), data.get('character_id'), data.get('like')
        character = Character.objects.get(id=character_id, group__game__alias=game_alias)
        if like:
            character.liked_by.add(request.user)
        else:
            character.liked_by.remove(request.user)
        return Response(data={'status': 'ok'}, status=HTTPStatus.OK)
