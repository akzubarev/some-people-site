from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.serializers import TokenSerializer, TokenCreateSerializer


class TokenViewSet(viewsets.GenericViewSet):
    serializer_class = TokenSerializer
    queryset = Token.objects
    lookup_field = "user"

    def get_serializer_class(self):
        if self.action == "login":
            return TokenCreateSerializer
        return self.serializer_class

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = self.get_serializer()
        serializer.validate(request.data)
        token, _ = self.get_queryset().get_or_create(user=serializer.user)
        return Response(
            data=TokenSerializer(token).data, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def logout(self, request):
        self.get_queryset().filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
