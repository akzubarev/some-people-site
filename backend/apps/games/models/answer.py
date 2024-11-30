"""Answer models."""
from django.db import models

from .question import Question


class Answer(models.Model):
    """Answer model."""

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

    def __str__(self):
        return f"{self.application} {self.question} {self.value}"

    class Meta:
        """Model meta."""

        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    @property
    def filled(self) -> bool:
        """If question is fully answered."""
        if self.question.type in [Question.Type.MATRIX, Question.Type.MATRIX_CHECKBOX]:
            return all(self.value)
        else:
            return bool(self.value)
