from django.db import models

from .mailing_platform import MailingPlatform


class TelegramMixin(MailingPlatform):
    class Meta:
        abstract = True

    telegram = models.SmallIntegerField(
        default=0, blank=True, choices=MailingPlatform.Status.CHOICES
    )
