"""Purpose-scoped credentials; only a digest is persisted."""
from django.conf import settings
from django.db import models


class OneTimeToken(models.Model):
    class Action(models.TextChoices):
        TELEGRAM_LINK = 'telegram_link', 'Link Telegram'
        PASSWORD_CHANGE = 'password_change', 'Change password'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=32, choices=Action.choices)
    digest = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'action'], name='unique_user_token_action')]
