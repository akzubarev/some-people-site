"""Users models."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from mixins import AutoCreatedUpdatedMixin, UUIDMixin


class User(AutoCreatedUpdatedMixin, UUIDMixin, AbstractUser):
    """User model."""

    email = models.EmailField(
        verbose_name='email',
        unique=True, max_length=255
    )
    first_name = models.CharField(
        verbose_name='name',
        max_length=100,
    )
    last_name = models.CharField(
        verbose_name='surname',
        max_length=100,
    )

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=30, unique=True,
    )

    avatar = models.ImageField(
        verbose_name='picture',
        upload_to='users/avatars/',
        blank=True, null=True
    )

    phone = PhoneNumberField(blank=True, default=None, null=True)
    is_staff = models.BooleanField(verbose_name='admin', default=False)

    telegram_chat_id = models.CharField(
        verbose_name='telegram_chat_id', max_length=250,
        blank=True, null=True, default=None
    )
    telegram_username = models.CharField(
        verbose_name='telegram_username', max_length=250,
        blank=True, null=True, default=None
    )
    vk = models.CharField(
        verbose_name='vk', max_length=250,
        blank=True, null=True, default=None
    )
    vk_public = models.BooleanField(verbose_name='vk_public', default=True)
    tg_public = models.BooleanField(verbose_name='tg_public', default=True)

    # Fields settings
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username} ({self.first_name} {self.last_name})'
