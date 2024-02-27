from django.db import models


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100
    )
    private = models.BooleanField(
        default=False,
        verbose_name='Виден только внутри тэга'
    )
    mg = models.BooleanField(
        default=False,
        verbose_name='Виден только МГ',
    )
    color = models.CharField(
        verbose_name="Цвет",
        max_length=10,
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name
