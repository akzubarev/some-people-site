from rest_framework import serializers

from apps.users.utils.compat import get_user_email_field_name
from apps.users.conf import settings
from apps.users.models import User
from apps.users.serializers.mixins import UserFunctionsMixin


class SendEmailResetSerializer(serializers.Serializer, UserFunctionsMixin):
    default_error_messages = {
        "email_not_found": settings.CONSTANTS.messages.EMAIL_NOT_FOUND,
        # "email_not_active": settings.CONSTANTS.messages.INACTIVE_EMAIL_ERROR
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.email_field = get_user_email_field_name(User)
        self.fields[self.email_field] = serializers.EmailField()
