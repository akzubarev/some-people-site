from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.indexes import BrinIndex


class AutoCreatedUpdatedMixin(models.Model):
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
        abstract = True
        indexes = (
            BrinIndex(fields=['created_at']),
        )

    def save(self, *args, **kwargs):
        if not self.id or not self.created_at:
            self.created_at = now()
            self.updated_at = self.created_at
        else:
            auto_updated_at_is_disabled = kwargs.pop(
                'disable_auto_updated_at', False)
            if not auto_updated_at_is_disabled:
                self.updated_at = now()
        super(AutoCreatedUpdatedMixin, self).save(*args, **kwargs)
