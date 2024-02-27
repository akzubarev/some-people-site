from uuid import uuid4

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
    PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from mixins.models import AutoCreatedUpdatedMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_('the given email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class User(AutoCreatedUpdatedMixin, AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)

    email = models.EmailField(
        verbose_name=_('email'),
        unique=True, max_length=255
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

    username = models.CharField(
        verbose_name="Никнейм",
        max_length=30, unique=True,
        null=True, blank=True
    )

    avatar = models.ImageField(
        verbose_name=('picture'),
        upload_to='tgavatars/pictures/',
        blank=True, null=True
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

    phone = PhoneNumberField(blank=True, default=None, null=True)
    is_active = models.BooleanField(verbose_name=_('active'), default=True)
    is_staff = models.BooleanField(verbose_name=_('admin'), default=False)
    email_active = models.BooleanField(default=False)
    instagram = models.CharField(
        verbose_name=_("instagram"), max_length=250,
        blank=True, null=True,
        default=None
    )

    # Fields settings
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()
