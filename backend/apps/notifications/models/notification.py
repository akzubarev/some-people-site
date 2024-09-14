import dataclasses
from datetime import datetime

from django.core.files import File
from django.db import models


class Notification(models.Model):
    # text = models.TextField()
    # image = models.ImageField()

    user = models.ForeignKey(
        to="users.User", verbose_name="user",
        related_name="notifications",
        on_delete=models.CASCADE,
    )
    mailing = models.ForeignKey(
        to="notifications.Mailing", verbose_name="mailing",
        related_name="notifications",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    sent = models.BooleanField(default=False, blank=True)
    viewed = models.BooleanField(default=False, blank=True)

    def data(self):
        """Returns a dataclass representation of the model."""
        return NotificationData(
            id=self.id,
            text=self.mailing.text, image=self.mailing.image,
            chat_id=self.user.telegram_chat_id, time=self.mailing.time,
        )


@dataclasses.dataclass
class NotificationData:
    id: int
    text: str
    chat_id: str
    image: File | None
    time: datetime
