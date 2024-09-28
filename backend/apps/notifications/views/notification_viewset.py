"""Notification views module."""
from typing import Any

from django.db.models import QuerySet
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer


class MyNotificationsFilter(filters.BaseFilterBackend):
    """Filter for personal notifications."""

    def filter_queryset(self, request: Request, queryset: QuerySet, *args: Any, **kwargs: Any) -> QuerySet:
        """Filters personal notifications."""
        return queryset.filter(user=request.user)


class StandardResultsSetPagination(PageNumberPagination):
    """Standard page_number pagination."""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50


class NotificationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Notification viewset"""
    queryset = Notification.objects
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [MyNotificationsFilter]

    def list(self, *args: Any, **kwargs: Any) -> Response:
        """Get all the notifications."""
        self.queryset = self.queryset.order_by('-id')
        return super().list(*args, **kwargs)

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def viewed(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Set notification status as viewed."""
        self.queryset.filter(user_id=request.user.id).update(viewed=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
