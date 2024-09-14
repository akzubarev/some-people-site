"""Users viewset."""
from typing import Any

from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import MyUserSerializer, UserCreateSerializer, UserSerializer
from utils.auth import encode_uuid


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin):
    """Users viewset."""

    serializer_class = UserSerializer
    queryset = User.objects
    lookup_field = "uuid"

    def get_serializer_class(self):
        """Gets serializer class based on action."""
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'me':
            return MyUserSerializer
        return self.serializer_class

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args: Any, **kwargs: Any):
        """Makes an action for current user based on query action."""
        self.get_object = lambda: request.user
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request):
        """Create a new user."""
        if request.user.is_authenticated:
            PermissionDenied()
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)

        user = User.objects.filter(id=serializer.instance.id).first()
        user.save()
        data = dict(serializer.data)
        data["auth_token"] = token.key
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args: Any, **kwargs: Any):
        """Retrieves a user."""
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, context={'request': request}
        )
        return Response(serializer.data)

    def list(self, request, *args: Any, **kwargs: Any):
        """Retrieves the list of users."""
        queryset = self.get_queryset()
        serializer = self.serializer_class(
            queryset, context={'request': request}, many=True
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def players(self, request, *args: Any, **kwargs: Any):
        """Retrieves the list of players for a game by alias."""
        game_alias = request.GET.get("game_alias")
        queryset = User.objects.filter(applications__game__alias=game_alias)
        serializer = self.serializer_class(
            queryset, context={'request': request}, many=True
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def mg(self, request, *args: Any, **kwargs: Any):
        """Retrieves the list of master group users."""
        queryset = User.objects.filter(is_staff=True).exclude(username="admin")
        serializer = self.serializer_class(
            queryset, context={'request': request}, many=True
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def telegram_code(self, request, *args: Any, **kwargs: Any):
        """Retrieves the telegram code for current user."""
        return Response(encode_uuid(uuid=request.user.uuid))
