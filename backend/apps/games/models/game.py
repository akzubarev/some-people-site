from django.db import models


class Game(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=100
    )

    alias = models.CharField(
        verbose_name='Алиас',
        max_length=20
    )

    description = models.TextField(
        verbose_name="Описание",
        null=True, blank=True
    )

    short_description = models.TextField(
        verbose_name="Короткое описание",
        null=True, blank=True
    )

    price = models.IntegerField(
        verbose_name="Взнос", blank=True, null=True
    )

    location = models.CharField(
        verbose_name='Место',
        max_length=100,
        blank=True, null=True
    )
    year = models.IntegerField(verbose_name="Год", blank=True, null=True)
    start = models.DateTimeField(verbose_name="Начало", blank=True, null=True)
    end = models.DateTimeField(verbose_name="Конец", blank=True, null=True)
    open_character_list = models.BooleanField(
        verbose_name="Сетка открыта", default=False
    )
    open_applications = models.BooleanField(
        verbose_name="Прием заявок открыт", default=False
    )
    vk = models.CharField(
        verbose_name='VK', max_length=100,
        blank=True, null=True
    )
    tg = models.CharField(
        verbose_name='TG', max_length=100,
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ["-id"]

    def __str__(self):
        return self.title
