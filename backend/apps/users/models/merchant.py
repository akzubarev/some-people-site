import secrets
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

from mixins.models import AutoCreatedUpdatedMixin

TOKEN_LENGTH = 10


def gen_api_token():
    return secrets.token_urlsafe(nbytes=TOKEN_LENGTH)


class Merchant(AutoCreatedUpdatedMixin):
    uuid = models.UUIDField(
        default=uuid4, editable=False, unique=True
    )
    promo_link = models.CharField(
        default=gen_api_token, max_length=2 * TOKEN_LENGTH,
        editable=False, unique=True
    )
    p2p_id = models.IntegerField(
        blank=True, null=True
    )

    user = models.ForeignKey(
        'users.User',
        verbose_name='user',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='merchants',
    )

    email = models.EmailField(
        verbose_name=_('email'),
        unique=True,
        max_length=255
    )
    first_name = models.CharField(
        verbose_name=_('name'),
        max_length=100, default=None,
        null=True, blank=True
    )
    last_name = models.CharField(
        verbose_name=_('surname'),
        max_length=100, default=None,
        null=True, blank=True
    )

    country = models.CharField(
        verbose_name=_('Country'),
        max_length=100, default=None,
        null=True, blank=True
    )
    country_iso = models.CharField(
        verbose_name=_('Country ISO code'),
        max_length=5, default=None,
        null=True, blank=True
    )
    city = models.CharField(
        verbose_name=_('City'),
        max_length=100, default=None,
        null=True, blank=True
    )
    phone = PhoneNumberField(
        blank=True, null=True,
        default=None,
    )
    address = models.CharField(
        verbose_name=_("address"),
        max_length=250, blank=True, null=True,
        default=None
    )
    company = models.CharField(
        verbose_name=_("company"),
        max_length=250, blank=True, null=True,
        default=None
    )
    website = models.CharField(
        verbose_name=_("website"),
        max_length=250, blank=True, null=True,
        default=None
    )
    instagram = models.CharField(
        verbose_name=_("instagram"),
        max_length=250, blank=True, null=True,
        default=None
    )
    telegram = models.CharField(
        verbose_name=_("telegram"),
        max_length=250, blank=True, null=True,
        default=None
    )
    twitter = models.CharField(
        verbose_name=_("twitter"),
        max_length=250, blank=True, null=True,
        default=None
    )
    facebook = models.CharField(
        verbose_name=_("facebook"),
        max_length=250, blank=True, null=True,
        default=None
    )
    youtube = models.CharField(
        verbose_name=_("youtube"),
        max_length=250, blank=True, null=True,
        default=None
    )

    def referal_link(self):
        return f"https://app.pintopay.me/register?refcode={self.promo_link}"
