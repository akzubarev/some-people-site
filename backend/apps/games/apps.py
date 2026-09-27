"""Games app."""
from django.apps import AppConfig


class GamesAppConfig(AppConfig):
    """Games app config."""
    name = 'apps.games'
    verbose_name = 'Games'

    def ready(self):
        from . import public_cache  # noqa: F401
