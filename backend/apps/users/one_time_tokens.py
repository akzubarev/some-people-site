"""Reusable one-time credentials with atomic, purpose-specific consumption."""
import hashlib
import re
import secrets
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from .models import OneTimeToken, User


def validate_action(action):
    if action not in OneTimeToken.Action.values:
        raise ValueError('Unknown token action.')


@transaction.atomic
def issue_token(user, action, *, lifetime=timedelta(minutes=10)):
    validate_action(action)
    if lifetime <= timedelta(0):
        raise ValueError('Token lifetime must be positive.')
    account = User.objects.select_for_update().get(pk=user.pk)
    if not account.is_active:
        raise ValueError('Inactive account.')
    code = secrets.token_urlsafe(32)
    now = timezone.now()
    OneTimeToken.objects.update_or_create(user=account, action=action, defaults={
        'digest': hashlib.sha256(code.encode()).hexdigest(),
        'created_at': now, 'expires_at': now + lifetime, 'consumed_at': None,
    })
    return code


@transaction.atomic
def consume_token(code, action, apply):
    """Apply a database change to the locked user and consume in one transaction.

    The caller supplies the expected action, never a value from the request.
    `apply(user)` must perform database work only; an exception rolls back both
    its changes and consumption. Schedule external effects with on_commit.
    """
    validate_action(action)
    if not isinstance(code, str) or not re.fullmatch(r'[A-Za-z0-9_-]{43}', code):
        raise ValueError('Invalid or expired code.')
    digest = hashlib.sha256(code.encode()).hexdigest()
    query = OneTimeToken.objects.filter(digest=digest, action=action)
    token = query.first()
    if token is None:
        raise ValueError('Invalid or expired code.')
    # Same user -> token locking order as issuance prevents rotation races.
    user = User.objects.select_for_update().get(pk=token.user_id)
    token = query.select_for_update().first()
    now = timezone.now()
    if token is None or token.consumed_at or token.expires_at <= now or not user.is_active:
        raise ValueError('Invalid or expired code.')
    token.consumed_at = now
    token.save(update_fields=['consumed_at'])
    return apply(user)
