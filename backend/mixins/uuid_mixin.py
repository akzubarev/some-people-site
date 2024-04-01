from django.db import models
from uuid import uuid4


class UUIDMixin(models.Model):
    uuid = models.UUIDField(
        default=uuid4, editable=False, null=False,
        unique=True
    )

    class Meta:
        abstract = True
