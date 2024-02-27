from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from apps.users.models import User


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, password=None, **kwargs):
        login_field = (
                kwargs.get("login_field") or
                kwargs.get("email") 
                # or
                # kwargs.get("username")
        )
        # Q(**{"username": login_field}) | 
        users = User.objects.filter(
            Q(**{"email": login_field})
        )
        if users.count() == 1:
            user = users.first()
            return user if user.check_password(password) else None
        else:
            return None
