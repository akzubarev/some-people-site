"""Google subject identities and browser-bound one-use login challenges."""
from django.conf import settings
from django.db import models


class GoogleIdentity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='google_identity')
    subject = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)


class GoogleChallenge(models.Model):
    digest = models.CharField(max_length=64, unique=True)
    browser_digest = models.CharField(max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=8, choices=[('signin', 'Sign in'), ('link', 'Link')])
    expires_at = models.DateTimeField()
    consumed_at = models.DateTimeField(null=True)
