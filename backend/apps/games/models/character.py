from django.db import models


class Character(models.Model):
    name = models.CharField(
        verbose_name='Имя',
        max_length=100
    )
    alias = models.CharField(
        verbose_name='Никнейм',
        max_length=100
    )

    description = models.TextField(
        verbose_name="Описание",
        null=True, blank=True
    )

    faction = models.ForeignKey(
        to="games.Faction",
        verbose_name='Фракция',
        related_name="characters",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    master = models.ForeignKey(
        to="users.User",
        verbose_name='Мастер',
        related_name="characters",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    image = models.ImageField(
        verbose_name='image',
        upload_to='characters/images/',
        blank=True, null=True
    )

    tags = models.ManyToManyField(
        verbose_name="Тэги",
        to="games.Tag", related_name="characters",
    )

    kventa = models.FileField(
        upload_to='kventas/pdf/',
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонаж'
        ordering = ["name"]

    def __str__(self):
        return self.name
