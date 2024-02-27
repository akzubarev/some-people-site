from django.db import models


class Answer(models.Model):
    question = models.ForeignKey(
        verbose_name="Вопрос",
        to="games.Question", related_name="answers",
        on_delete=models.CASCADE
    )
    application = models.ForeignKey(
        verbose_name="Заявка",
        to="games.Application", related_name="answers",
        on_delete=models.CASCADE
    )
    value = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"{self.application} {self.question} {self.value}"
