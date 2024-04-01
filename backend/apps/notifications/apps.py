from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class NotificationsAppConfig(AppConfig):
    name = 'apps.notifications'
    verbose_name = _('Notifications')

    def ready(self):
        # from .models import Notification
        pass
