from apps.users.models import User
from mixins.models import AutoCreatedUpdatedMixin

from django.utils.translation import gettext as _
from django.db import models

DEFAULT_NOTIFICATION_SETTINGS = {
    "personal": {
        "MatrixBonusNotification": True,
        "ReferalBonusNotification": True,
        "WithdrawNotification": True,
        "NewCloneNotification": True,
        "ActivateMatrixNotification": True,
        "MatrixCompletedNotification": True,
        "ArenaNotification": True,
        "SubscriptionNotification": True,
        "ReSubscriptionNotification": True,
        "LostProfitNotification": True,
        "ProfitNotification": True,
    },
    "team": {
        "MatrixBonusNotification": False,
        "ReferalBonusNotification": False,
        "WithdrawNotification": False,
        "NewCloneNotification": False,
        "ActivateMatrixNotification": False,
        "MatrixCompletedNotification": False,
        "ArenaNotification": False,
        "SubscriptionNotification": True,
        "ReSubscriptionNotification": True,
        "LostProfitNotification": False,
        "ProfitNotification": True,
    },
    "group": {
        "MatrixBonusNotification": True,
        "ReferalBonusNotification": True,
        "WithdrawNotification": True,
        "NewCloneNotification": True,
        "ActivateMatrixNotification": True,
        "MatrixCompletedNotification": True,
        "ArenaNotification": True,
        "SubscriptionNotification": True,
        "ReSubscriptionNotification": True,
        "LostProfitNotification": False,
        "ProfitNotification": True,
    },
}


class Telegram(AutoCreatedUpdatedMixin):
    user = models.OneToOneField(
        User, verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="telegram",
    )
    code = models.CharField(
        verbose_name=_("code"),
        max_length=250,
        blank=True, null=True,
    )

    username = models.CharField(
        verbose_name=_("username"),
        max_length=250, default=None,
        blank=True, null=True,
    )

    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=250, default=None,
        blank=True, null=True,
    )

    chat_id = models.CharField(
        verbose_name=_("chat"),
        max_length=30,
        blank=True, null=True,
    )

    settings = models.JSONField(
        verbose_name=_("settings"),
        default=DEFAULT_NOTIFICATION_SETTINGS,
        blank=True
    )
