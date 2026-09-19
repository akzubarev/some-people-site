"""Existing links survive the transition to purpose-scoped credentials."""
import hashlib
import secrets
from datetime import timedelta

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase
from django.utils import timezone

from apps.users.models import OneTimeToken, User
from apps.users.telegram_link import consume_link


class TokenMigration(TransactionTestCase):
    def test_existing_unexpired_link_remains_usable(self):
        executor = MigrationExecutor(connection)
        before = [('users', '0006_telegram_link_token')]
        after = [('users', '0007_one_time_token')]
        executor.migrate(before)
        try:
            historical = executor.loader.project_state(before).apps
            user = User.objects.create_user('migration-link', 'migration@example.invalid')
            code = secrets.token_urlsafe(32)
            now = timezone.now()
            historical.get_model('users', 'TelegramLinkToken').objects.create(
                user_id=user.pk, digest=hashlib.sha256(code.encode()).hexdigest(),
                created_at=now, expires_at=now + timedelta(minutes=10),
            )
        finally:
            MigrationExecutor(connection).migrate(after)
        token = OneTimeToken.objects.get(user_id=user.pk)
        self.assertEqual(token.action, OneTimeToken.Action.TELEGRAM_LINK)
        self.assertFalse(consume_link(code, 12001, 'migration'))
        user.refresh_from_db()
        self.assertEqual(user.telegram_chat_id, '12001')
