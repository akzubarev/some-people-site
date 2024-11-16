"""Application model."""
from django.db import models


class Application(models.Model):
    """Application model."""

    class Status:
        PENDING = "pending"
        DISCUSSING = "discussing"
        CONFIRMED = "confirmed"
        DECLINED = "declined"
        DELETED = "deleted"

        CHOICES = [
            (PENDING, "Подана"),
            (DISCUSSING, "Обсуждается"),
            (CONFIRMED, "Принята"),
            (DECLINED, "Отклонена"),
            (DELETED, "Удалена"),
        ]

    user = models.ForeignKey(
        verbose_name="Игрок",
        to="users.User", related_name="applications",
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        verbose_name="Игра",
        to="games.Game", related_name="applications",
        on_delete=models.CASCADE
    )
    character = models.OneToOneField(
        verbose_name="Персонаж",
        to="games.Character", related_name="application",
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    status = models.CharField(
        verbose_name="Статус", choices=Status.CHOICES,
        default=Status.PENDING
    )
    price = models.IntegerField(
        verbose_name="Взнос", blank=True, null=True
    )

    payed = models.IntegerField(
        verbose_name="Оплачено", default=0
    )

    def save(self, *args, **kwargs):
        """Save with price calculation."""
        if not self.id:
            self.price = self.game.price
        super().save(*args, **kwargs)

    class Meta:
        """Model meta."""

        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.user} {self.game} {self.character or ''}"
