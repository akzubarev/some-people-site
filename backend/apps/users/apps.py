"""Users app."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersAppConfig(AppConfig):
    """Users app config."""
    name = "apps.users"
    verbose_name = _('Users')
