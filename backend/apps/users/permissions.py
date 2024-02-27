from rest_framework import permissions


# from rest_framework.permissions import SAFE_METHODS


class CurrentUserOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff or obj.pk == user.pk


class IsStaff(permissions.BasePermission):
    def is_staff(self, request):
        user = request.user
        return (bool(request.user and request.user.is_authenticated) and
                user.groups.filter(name='Staff').exists())
