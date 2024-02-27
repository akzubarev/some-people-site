from django.db import models
from django.utils.translation import gettext as _

from apps.users.models import User
from mixins.enums import MatrixPermissionLevel, Locale
from mixins.fields import ChoiceArrayField
from mixins.models import AutoCreatedUpdatedMixin
from .mixins import TelegramMixin, EmailMixin


class Mailing(AutoCreatedUpdatedMixin):
    locales = ChoiceArrayField(
        base_field=models.CharField(
            verbose_name=_('locale'),
            max_length=2,
            choices=Locale.choices,
            default=Locale.en
        ),
        default=[]
    )

    entry_level = models.IntegerField(
        verbose_name=_('entry level'),
        choices=MatrixPermissionLevel.choices,
        default=MatrixPermissionLevel.free,
    )

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

    private = models.BooleanField(
        verbose_name=_('private'),
        default=False
    )

    telegram = models.BooleanField(
        verbose_name='telegram', default=True
    )

    email = models.BooleanField(
        verbose_name='email', default=False
    )

    def save(self, *args, **kwargs):
        if self.private is False:
            base_qs = User.objects.all()
            if len(self.locales) > 0:
                base_qs = base_qs.filter(locale__in=self.locales)
            if self.entry_level != MatrixPermissionLevel.free:
                base_qs = (base_qs.annotate(
                    max_level=models.Max('matrix_refers__lvl')
                ).filter(max_level__gte=self.entry_level))

            # if hasattr(self, 'id'):
            #     MailingRecipient.objects.filter(mailing_id=self.id).delete()

            super().save(*args, **kwargs)
            for user in base_qs:
                MailingRecipient.objects.create(
                    user=user, mailing=self,
                )
        else:
            super().save(*args, **kwargs)

        # for user in base_qs:
        #     m = MailingRecipient(mailing_id=self.id, user=user)
        #     m.save()
        #     print(user, m)


class MailingRecipient(AutoCreatedUpdatedMixin, TelegramMixin, EmailMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

# @receiver(pre_save, sender=Mailing, dispatch_uid="create_mailing_recipients")
# def create_mailing_recipients(sender, instance, **kwargs):
#     base_qs = User.objects.all()

#     if len(instance.locales) > 0:
#         base_qs = base_qs.filter(locale__in=instance.locales)
#     if instance.entry_level != MatrixPermissionLevel.free:
#         base_qs = (base_qs
#             .annotate(max_level=models.Max('matrix_refers__lvl'))
#             .filter(max_level__gte=instance.entry_level))

#     instance.user.set(base_qs)
