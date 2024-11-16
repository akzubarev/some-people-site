"""Group models."""
from django.db import models


class Group(models.Model):
    """Group model."""

    order = models.IntegerField(verbose_name='Порядковый номер', default=1)
    name = models.CharField(verbose_name='Название', max_length=100)
    alias = models.CharField(verbose_name='Алиас', max_length=100, blank=True, null=True)
    hidden = models.BooleanField(default=False, verbose_name='Секретная')
    family = models.BooleanField(default=False, verbose_name='Семья')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    game = models.ForeignKey(
        to='games.Game',
        verbose_name='Игра',
        related_name='groups',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    parent = models.ForeignKey(
        to='games.Group',
        verbose_name='Родительская фракция',
        related_name='subgroups', on_delete=models.SET_NULL,
        null=True, blank=True
    )

    image = models.ImageField(
        verbose_name='image',
        upload_to='groups/images/',
        blank=True, null=True
    )

    class Meta:
        """Model meta."""

        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['order']

    def __str__(self):
        return self.name
