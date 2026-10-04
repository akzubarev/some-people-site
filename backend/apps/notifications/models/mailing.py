"""Mailing models module."""
from django.db import models
from django.utils.translation import gettext as _

from apps.users.models import User
from mixins.create_update_mixin import AutoCreatedUpdatedMixin


class Mailing(AutoCreatedUpdatedMixin):
    """Mailing model."""
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

    users = models.ManyToManyField(to=User, related_name='mailings')
    game = models.ForeignKey('games.Game', on_delete=models.PROTECT, null=True, blank=True,
                             related_name='mailings')
    applications = models.ManyToManyField('games.Application', blank=True, related_name='mailings')
    confirmed_at = models.DateTimeField(null=True, blank=True)
    confirmation_key = models.UUIDField(null=True, blank=True, unique=True)
