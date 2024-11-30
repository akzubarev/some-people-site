"""Game character models."""
from django.db import models


class Character(models.Model):
    """Game character model."""

    order = models.IntegerField(verbose_name="Порядковый номер", default=1)
    name = models.CharField(verbose_name='Имя', max_length=100)
    alias = models.CharField(verbose_name='Никнейм', max_length=100)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    group = models.ForeignKey(
        to='games.Group', on_delete=models.SET_NULL,
        verbose_name='Фракция', related_name='characters',
        null=True, blank=True
    )

    family = models.ForeignKey(
        to='games.Group', on_delete=models.SET_NULL,
        verbose_name='Семья', related_name='members',
        null=True, blank=True,
    )

    master = models.ForeignKey(
        to='users.User', on_delete=models.SET_NULL,
        verbose_name='Мастер', related_name='members',
        null=True, blank=True,
    )

    image = models.ImageField(
        verbose_name='image', upload_to='characters/images/',
        blank=True, null=True
    )

    tags = models.ManyToManyField(verbose_name='Тэги', to='games.Tag', related_name='characters')
    kventa = models.FileField(upload_to='kventas/pdf/', blank=True, null=True)
    liked_by = models.ManyToManyField(
        to='users.User', verbose_name='Лайки',
        related_name='likes', null=True, blank=True,
    )

    class Meta:
        """Model meta."""

        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'
        ordering = ['order']

    def __str__(self):
        return self.name
