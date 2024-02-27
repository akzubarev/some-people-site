from django.db import models
from django.utils.translation import gettext as _


class MailingPlatform(models.Model):
    class Meta:
        abstract = True

    class Status:
        NEW = 0
        SUCCESS = 1
        CANCELLED = 2
        TIMEOUT = 3
        NETWORK_ERROR = 4
        BAD_REQUEST = 5
        TELEGRAM_CONFL = 6
        TOKEN_ERROR = 7

        CHOICES = [
            (NEW, _('New')),
            (SUCCESS, _('Success')),
            (CANCELLED, _('Cancelled')),
            (TIMEOUT, _('Timeout')),
            (NETWORK_ERROR, _('NetworkError')),
            (BAD_REQUEST, _('BadRequest')),
            (TELEGRAM_CONFL, _('TelegramConfl')),
            (TOKEN_ERROR, _('TokenError')),
        ]
