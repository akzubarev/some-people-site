from django.db import models
from django.utils.translation import gettext as _

from apps.users.models import User
from mixins.create_update_mixin import AutoCreatedUpdatedMixin
from .notification import Notification


class Mailing(AutoCreatedUpdatedMixin):
    text = models.TextField(
        verbose_name=_('text'),
        null=True,
        blank=True
    )

    image = models.ImageField(
        verbose_name=_('image'),
        upload_to='mailing/images/',
        blank=True, null=True
    )

    ready = models.BooleanField(
        verbose_name=_('ready'),
        default=False,
    )

    time = models.DateTimeField(
        verbose_name='time',
        db_index=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.ready:
            base_qs = User.objects.all()
            Notification.objects.bulk_create([
                Notification(user=user, mailing=self) for user in base_qs
            ])
