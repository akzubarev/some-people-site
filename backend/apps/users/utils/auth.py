import random
from django.contrib.auth import user_logged_in, user_logged_out
from django.utils import timezone
from rest_framework.authtoken.models import Token
from utils.feature_dates import EMAIL_CONFIRMATION_ENABLED


def login_user(request, user):
    token, _ = Token.objects.get_or_create(user=user)
    # if settings.CREATE_SESSION_ON_LOGIN:
    # login(request, user)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return token


def logout_user(request):
    Token.objects.filter(user=request.user).delete()
    user_logged_out.send(
        sender=request.user.__class__, request=request, user=request.user
    )
    # if settings.CREATE_SESSION_ON_LOGIN:
    #     logout(request)


def is_email_verify_enabled(user):
    year, month, day = EMAIL_CONFIRMATION_ENABLED
    return user.created_at >= timezone.now().replace(
        year=year, month=month, day=day, hour=0, minute=0, second=0
    )


def generate_phone_code():
    return random.randint(100000, 999999)
