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
    viewed = models.BooleanField(default=False, blank=True)
