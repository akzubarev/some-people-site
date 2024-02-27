from django.db import models

from .mixins import TelegramMixin
from mixins.events import Event


class Notification(Event, TelegramMixin):
    class Types:
        pass

    viewed = models.BooleanField(default=False, blank=True)
