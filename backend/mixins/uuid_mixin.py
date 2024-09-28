"""UUID mixin module."""
from uuid import uuid4

from django.db import models


class UUIDMixin(models.Model):
    """UUID mixin."""

    uuid = models.UUIDField(default=uuid4, editable=False, null=False, unique=True)

    class Meta:
        """Model meta"""
        abstract = True
