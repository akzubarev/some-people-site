from django.db import IntegrityError, transaction

from apps.users.conf import settings
from apps.users.utils import ActivationEmail
from apps.users.models import User
from apps.users.utils import is_email_verify_enabled


class UserCreateMixin:
    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.email_active = False
                user.save(update_fields=["email_active"])
                try:
                    ActivationEmail(self.request, self.context).send(
                        user.email)
                except Exception as e:
                    print(e)
        return user


class UserFunctionsMixin:
    def get_user(self, is_active=True, force_email=False):
        try:
            user = User._default_manager.get(
                is_active=is_active,
                **{self.email_field: self.data.get(self.email_field, "")},
            )
            if (force_email is False and not user.email_active
                    and is_email_verify_enabled(user)):
                self.fail("email_not_active")
            if user.has_usable_password():
                return user
        except User.DoesNotExist:
            pass
        if (
                settings.PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND
                or settings.USERNAME_RESET_SHOW_EMAIL_NOT_FOUND
        ):
            self.fail("email_not_found")
