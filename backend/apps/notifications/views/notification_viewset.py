from rest_framework import filters
from rest_framework import mixins
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..models import Notification
from ..serializers import NotificationSerializer
from ..serializers.telegram_serializer import \
    TelegramSerializer


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50


class NotificationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Notification.objects
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        IsOwnerFilterBackend,
    ]

    def list(self, *args, **kwargs):
        self.queryset = self.queryset.order_by('-id')
        return super().list(*args, **kwargs)

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def viewed(self, request, *args, **kwargs):
        self.queryset.filter(user_id=request.user.id).update(
            viewed=True
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def save_settings(self, request, *args, **kwargs):
        tg = request.user.telegram
        serializer = TelegramSerializer(tg, data={"settings": request.data})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)
