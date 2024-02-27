from django.db import models
from .mailing_platform import MailingPlatform


class EmailMixin(models.Model):
    class Meta:
        abstract = True

    email_status = models.SmallIntegerField(
        default=0, blank=True,
        choices=MailingPlatform.Status.CHOICES
    )
