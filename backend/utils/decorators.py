"""Decorators."""
from typing import Any, Callable

from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response

from apps.games.models import Game


def roles_open(func: Callable, *args, **kwargs) -> Callable:
    """Checks if user has rights to open the roles list."""

    def wrapper(request: Request, *args: Any, **kwargs: Any) -> Response | PermissionDenied:
        game_alias = request.GET.get('game_alias', None)
        game = Game.objects.filter(alias=game_alias).first()
        if request.user.is_staff is False and game.open_character_list is False:
            return PermissionDenied('Сетка ролей еще не опубликована')
        return func(request, *args, **kwargs)

    return wrapper
