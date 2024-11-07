"""Tokens views module."""
from typing import Type

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.serializers import TokenCreateSerializer, TokenSerializer


class TokenViewSet(viewsets.GenericViewSet):
    """Token viewset."""
    serializer_class = TokenSerializer
    queryset = Token.objects
    lookup_field = "user"

    def get_serializer_class(self) -> Type[TokenSerializer | TokenCreateSerializer]:
        """Return serializer class."""
        if self.action == "login":
            return TokenCreateSerializer
        return self.serializer_class

    @action(detail=False, methods=["post"], permission_classes=[AllowAny], authentication_classes=[])
    def login(self, request: Request) -> Response:
        """Logs user in."""
        token_serializer = self.get_serializer()
        token_serializer.validate(request.data)
        token, _ = self.get_queryset().get_or_create(user=token_serializer.user)
        return Response(data=TokenSerializer(token).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request: Request) -> Response:
        """Logs user out."""
        self.get_queryset().filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
