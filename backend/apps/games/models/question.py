from django.db import models


class Question(models.Model):
    class Type:
        LINE = "line"
        PARAGRAPH = "paragraph"
        SINGLE_CHOICE = "single_choice"
        MULTIPLE_CHOICE = "multiple_choice"
        SCALE = "scale"
        MATRIX = "matrix"

        CHOICES = [
            (LINE, "Строка"),
            (PARAGRAPH, "Абзац"),
            (SINGLE_CHOICE, "Одиночный выбор"),
            (MULTIPLE_CHOICE, "Множественный выбор"),
            (SCALE, "Шкала"),
            (MATRIX, "Сетка"),
        ]

    game = models.ManyToManyField(
        verbose_name="Игра",
        to="games.Game", related_name="questions",
    )

    title = models.CharField(
        verbose_name="Вопрос", max_length=500,
    )

    description = models.TextField(
        verbose_name="Описание",
        null=True, blank=True
    )

    type = models.CharField(
        verbose_name="Тип", choices=Type.CHOICES,
        default=Type.LINE
    )

    choices = models.JSONField(
        verbose_name="Варианты",
        null=True, blank=True
    )

    order = models.IntegerField(
        verbose_name="Порядковый номер",
        default=1
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["order"]

    def __str__(self):
        return self.title