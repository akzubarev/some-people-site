from django.db import models

from mixins.models import AutoCreatedUpdatedMixin


class ChatData(AutoCreatedUpdatedMixin):
    chat_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
