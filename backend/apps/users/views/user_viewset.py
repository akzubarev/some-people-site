"""Users viewset."""
from typing import Any, Type

from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import MyUserSerializer, UserCreateSerializer, UserSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    """Users viewset."""

    serializer_class = UserSerializer
    queryset = User.objects
    lookup_field = "uuid"

    def get_serializer_class(self) -> Type[UserCreateSerializer | UserSerializer]:
        """Gets serializer class based on action."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'me':
            print(self.action)
            return MyUserSerializer
        return self.serializer_class

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request: Request, *args: Any, **kwargs: Any):
        """Makes an action for current user based on query action."""
        self.get_object = lambda: request.user
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        # elif request.method == 'DELETE':
        #     return self.destroy(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request: Request) -> Response:
        """Create a new user."""
        if request.user.is_authenticated:
            PermissionDenied()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)

        user = User.objects.filter(id=serializer.instance.id).first()
        user.save()
        response_data = dict(serializer.data) | {'auth_token': token.key}
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieves a user."""
        serializer = self.get_serializer(self.get_object(), context={'request': request})
        return Response(serializer.data)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieves the list of users."""
        serializer = self.get_serializer(self.get_queryset(), context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def players(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieves the list of players for a game by alias."""
        game_alias = request.GET.get("game_alias")
        queryset = User.objects.filter(applications__game__alias=game_alias)
        serializer = self.get_serializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def mg(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieves the list of master group users."""
        queryset = User.objects.filter(is_staff=True).exclude(username="admin")
        serializer = self.get_serializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)
