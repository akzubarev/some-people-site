from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from uuid import uuid4
from django.contrib.postgres.indexes import BrinIndex

from django.db.models.signals import post_init

def track_data(*fields):
    """
    Tracks property changes on a model instance.
    
    The changed list of properties is refreshed on model initialization
    and save.
    
    >>> @track_data('name')
    >>> class Post(models.Model):
    >>>     name = models.CharField(...)
    >>> 
    >>>     @classmethod
    >>>     def post_save(cls, sender, instance, created, **kwargs):
    >>>         if instance.has_changed('name'):
    >>>             print "Hooray!"
    """
    
    UNSAVED = dict()

    def _store(self):
        "Updates a local copy of attributes values"
        if self.id:
            self.__data = dict((f, getattr(self, f)) for f in fields)
        else:
            self.__data = UNSAVED

    def inner(cls):
        # contains a local copy of the previous values of attributes
        cls.__data = {}

        def has_changed(self, field):
            "Returns ``True`` if ``field`` has changed since initialization."
            if self.__data is UNSAVED:
                return False
            return self.__data.get(field) != getattr(self, field)
        cls.has_changed = has_changed

        def old_value(self, field):
            "Returns the previous value of ``field``"
            return self.__data.get(field)
        cls.old_value = old_value

        def whats_changed(self):
            "Returns a list of changed attributes."
            changed = {}
            if self.__data is UNSAVED:
                return changed
            for k, v in self.__data.iteritems():
                if v != getattr(self, k):
                    changed[k] = v
            return changed
        cls.whats_changed = whats_changed

        # Ensure we are updating local attributes on model init
        def _post_init(sender, instance, **kwargs):
            _store(instance)
        post_init.connect(_post_init, sender=cls, weak=False)

        # Ensure we are updating local attributes on model save
        def save(self, *args, **kwargs):
            save._original(self, *args, **kwargs)
            _store(self)
        save._original = cls.save
        cls.save = save
        return cls
    return inner

class AutoCreatedUpdatedMixin(models.Model):

    uuid = models.UUIDField(default=uuid4, editable=False, null=False, unique=True)

    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        unique=False,
        null=True,
        blank=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        verbose_name=_('updated at'),
        unique=False,
        null=True,
        blank=True,
        db_index=True,
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

class UUUIDModel(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, null=False, unique=True)

    class Meta:
        abstract = True
