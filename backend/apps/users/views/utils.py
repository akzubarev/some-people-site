from django.utils import timezone
from rest_framework import filters, permissions
from rest_framework.pagination import PageNumberPagination


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class EmailConfirmedPermission(permissions.IsAuthenticated):
    EMAIL_CONFIRMATION_ENABLED = (2023, 7, 25)

    def has_permission(self, request, view):
        year, month, day = self.EMAIL_CONFIRMATION_ENABLED
        created_earlier = request.user.created_at < timezone.now().replace(
            year=year, month=month, day=day, hour=0, minute=0, second=0
        )
        emailConfirmed = request.user.email_active or created_earlier
        return emailConfirmed and super().has_permission(request, view)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200

