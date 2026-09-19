"""Telegram-specific effects applied through purpose-scoped one-time tokens."""
from django.db import connection, transaction

from .models import OneTimeToken, User
from .one_time_tokens import consume_token, issue_token


def issue_link(user):
    return issue_token(user, OneTimeToken.Action.TELEGRAM_LINK)


@transaction.atomic
def consume_link(code, chat_id, username):
    if not str(chat_id).isdigit() or int(chat_id) <= 0:
        raise ValueError('Private chat required.')
    # Serialize chat ownership checks across bot workers. Issuance does not
    # acquire this lock, so both paths retain the user -> token lock order.
    with connection.cursor() as cursor:
        cursor.execute('SELECT pg_advisory_xact_lock(1936748396, 1)')

    def link(user):
        if User.objects.filter(telegram_chat_id=str(chat_id)).exclude(pk=user.pk).exists():
            raise ValueError('Chat is already linked to another account.')
        changed = user.telegram_chat_id is not None
        user.telegram_chat_id = str(chat_id)
        user.telegram_username = username
        user.save(update_fields=['telegram_chat_id', 'telegram_username'])
        return changed

    return consume_token(code, OneTimeToken.Action.TELEGRAM_LINK, link)
