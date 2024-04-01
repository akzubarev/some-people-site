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
        verbose_name=_('private'),
        default=False
    )

    def save(self, *args, **kwargs):
        if self.ready is False:
            base_qs = User.objects.all()
            super().save(*args, **kwargs)
            for user in base_qs:
                Notification.objects.create(
                    user=user, mailing=self,
                )
        else:
            super().save(*args, **kwargs)
