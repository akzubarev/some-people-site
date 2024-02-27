from django.db import models


class Faction(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100
    )

    alias = models.CharField(
        verbose_name='Алиас',
        max_length=100
    )

    hidden = models.BooleanField(
        default=False, verbose_name="Секретная",
    )

    description = models.TextField(
        verbose_name="Описание",
        null=True, blank=True
    )

    game = models.ForeignKey(
        to="games.Game",
        verbose_name='Игра',
        related_name="factions",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    parent = models.ForeignKey(
        to="games.Faction",
        verbose_name='Родительская фракция',
        related_name="subfactions", on_delete=models.SET_NULL,
        null=True, blank=True
    )

    image = models.ImageField(
        verbose_name='image',
        upload_to='factions/images/',
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Фракция'
        verbose_name_plural = 'Фракция'
        ordering = ["name"]

    def __str__(self):
        return self.name
