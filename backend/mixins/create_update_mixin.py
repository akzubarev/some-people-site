"""Create-update mixin module."""
from typing import Any

from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.utils.timezone import now


class AutoCreatedUpdatedMixin(models.Model):
    """Create-update mixin."""
    created_at = models.DateTimeField(
        verbose_name='created at',
        unique=False, db_index=True,
        null=True, blank=True
    )

    updated_at = models.DateTimeField(
        verbose_name='updated at',
        unique=False, db_index=True,
        null=True, blank=True
    )

    class Meta:
        """Model meta."""

        abstract = True
        indexes = [BrinIndex(fields=['created_at'])]

    def save(self, *args: Any, **kwargs: Any):
        """Saves model with updated_time and created_time."""
        if not self.id or not self.created_at:
            self.created_at = now()
            self.updated_at = self.created_at
        else:
            auto_updated_at_is_disabled = kwargs.pop('disable_auto_updated_at', False)
            if not auto_updated_at_is_disabled:
                self.updated_at = now()
        super(AutoCreatedUpdatedMixin, self).save(*args, **kwargs)
