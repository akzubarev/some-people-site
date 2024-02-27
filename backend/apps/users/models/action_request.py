import datetime

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from .request_types import ActionRequestType
from mixins.models import AutoCreatedUpdatedMixin


# Action permission to perform an action
class ActionRequest(AutoCreatedUpdatedMixin):
    user = models.ForeignKey(
        "users.User", verbose_name=_("user"),
        on_delete=models.CASCADE,
        blank=False, null=False,
    )
    otp = models.CharField(
        max_length=6, blank=True,
    )
    expired_at = models.DateTimeField(
        verbose_name=_("expired at"),
        null=False, blank=False,
    )
    key = models.CharField(
        verbose_name=_('key'),
        max_length=30, default=''
    )
    data = models.JSONField(default=dict, blank=True)

    confirmed = models.BooleanField(blank=True, default=False)
    is_used = models.BooleanField(blank=True, default=False)

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.otp:
            import random
            otp = random.randint(0, 999999)
            self.otp = f"{otp:06d}"
            self.expired_at = timezone.now() + datetime.timedelta(minutes=10)

        if self.confirmed and timezone.now() > self.expired_at:
            raise Exception(_('Action request expired'))
        return super().save(*args, **kwargs)

    def send_otp(self, user, email=None):
        from django.core.mail import send_mail
        from django.utils.html import strip_tags
        if email is None:
            email = user.email
        html_msg = _("Your confirmation code is: ") + \
                   f"<br><h2>{self.otp}</h2>"
        send_mail(
            _("Action confirmation"), strip_tags(html_msg),
            None, [email],
            html_message=html_msg, fail_silently=False,
        )

    @staticmethod
    def confirm_otp(user, otp, key: str = None, data: dict = None):
        result = False
        requests = ActionRequest.objects.filter(user_id=user.id).filter(
            confirmed=False, expired_at__gte=timezone.now(),
        )
        if key is not None:
            requests = requests.filter(key=key)
        if data is not None:
            requests = requests.filter(**{
                f"data__{data_key}": value for data_key, value in data.items()
            })
        actionRequest = requests.order_by("-expired_at").first()

        if actionRequest is not None and actionRequest.otp == otp:
            actionRequest.confirmed = True
            actionRequest.save()
            result = True
        return result, actionRequest

    @staticmethod
    def add_request(user, type: ActionRequestType):
        return ActionRequest.objects.create(
            user=user, key=type.title, data=type.dict
        )
