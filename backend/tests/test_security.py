"""Security contracts exercised against synthetic PostgreSQL records only."""
import asyncio
from base64 import b64encode
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from django.core.cache import cache
from django.db import close_old_connections
from django.test import TestCase, TransactionTestCase, SimpleTestCase
from django.test import Client
from django.contrib.auth.models import Permission
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.games.models import Answer, Application, Character, Game, Group, Question, Tag
from apps.notifications.models import Notification
from apps.users.models import OneTimeToken, User
from apps.users.telegram_link import consume_link, issue_link
from apps.users.one_time_tokens import consume_token, issue_token
from apps.users.one_time_tokens import consume_token, issue_token

PUBLIC_FIELDS = {'username', 'first_name', 'last_name', 'avatar', 'vk', 'telegram'}
PRIVATE_FIELDS = {'id', 'email', 'username', 'first_name', 'last_name', 'uuid', 'mg',
                  'phone', 'vk', 'telegram', 'created_at', 'avatar', 'applications',
                  'likes', 'vk_public', 'tg_public'}


class SecurityAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.a = User.objects.create_user('synthetic-a', 'a@example.invalid', 'safe-test-password',
            phone='+12025550101', first_name='Synthetic', last_name='Alpha',
            vk='alpha', telegram_username='alpha', vk_public=False, tg_public=False)
        cls.b = User.objects.create_user('synthetic-b', 'b@example.invalid', 'safe-test-password')
        cls.staff = User.objects.create_user('synthetic-staff', 'staff@example.invalid',
                                            'safe-test-password', is_staff=True)
        cls.game = Game.objects.create(title='Public game', alias='public', open_character_list=True, price=100)
        cls.closed = Game.objects.create(title='Closed game', alias='closed')
        cls.group = Group.objects.create(name='Public group', game=cls.game)
        cls.child = Group.objects.create(name='Nested group', game=cls.game, parent=cls.group)
        cls.char = Character.objects.create(name='Character', alias='character', group=cls.child, family=cls.group)
        cls.secret_group = Group.objects.create(name='Unpublished group', game=cls.closed, parent=cls.group)
        cls.secret_char = Character.objects.create(name='Unpublished character', alias='secret',
                                                   group=cls.secret_group, family=cls.group)
        cls.app_a = Application.objects.create(user=cls.a, game=cls.game, character=cls.char,
                                               status=Application.Status.CONFIRMED, payed=10)
        cls.app_b = Application.objects.create(user=cls.b, game=cls.game, payed=20)
        cls.closed_app = Application.objects.create(user=cls.a, game=cls.closed, character=cls.secret_char)
        question = Question.objects.create(title='Synthetic private answer')
        question.games.add(cls.game)
        Answer.objects.create(application=cls.app_a, question=question, value='only-alpha')
        Answer.objects.create(application=cls.app_b, question=question, value='only-beta')

    def setUp(self):
        cache.clear()
        self.client = APIClient()

    def auth(self, user):
        self.client.force_authenticate(user=user)

    def test_public_profile_exact_allowlist_recursively(self):
        for endpoint in ['characters', 'groups']:
            response = self.client.get(f'/api/games/{endpoint}/?game_alias=public')
            self.assertEqual(response.status_code, 200)
            players = []
            def walk(value):
                if isinstance(value, dict):
                    if value.get('player'):
                        players.append(value['player'])
                    self.assertNotIn('master', value)
                    self.assertNotIn('application', value)
                    for child in value.values():
                        walk(child)
                elif isinstance(value, list):
                    for child in value:
                        walk(child)
            walk(response.data)
            self.assertTrue(players)
            for player in players:
                self.assertEqual(set(player), PUBLIC_FIELDS)
                self.assertIsNone(player['vk'])
                self.assertIsNone(player['telegram'])
            self.assertNotIn('Unpublished', str(response.data))

    def test_public_social_flags(self):
        self.a.vk_public = self.a.tg_public = True
        self.a.save()
        player = self.client.get('/api/games/characters/?game_alias=public').data[0]['player']
        self.assertEqual((player['vk'], player['telegram']), ('alpha', 'alpha'))

    def test_user_directory_and_generic_writes_removed(self):
        for user in [None, self.a, self.staff]:
            self.auth(user)
            for method in ['get', 'put', 'patch']:
                self.assertIn(getattr(self.client, method)(f'/api/users/{self.b.uuid}/', {}).status_code, [404, 405])
            self.assertIn(self.client.get('/api/users/').status_code, [404, 405])

    def test_staff_lists_are_restricted_and_minimal(self):
        for user, expected in [(None, 401), (self.a, 403), (self.staff, 200)]:
            self.auth(user)
            for endpoint in ['mg', 'players/?game_alias=public']:
                response = self.client.get('/api/users/' + endpoint.rstrip('/') + ('/' if '?' not in endpoint else ''))
                self.assertEqual(response.status_code, expected)
                if expected == 200:
                    self.assertTrue(response.data)
                    self.assertTrue(all(set(profile) == PUBLIC_FIELDS for profile in response.data))

    def test_me_and_profile_update_allowlist(self):
        self.assertEqual(self.client.get('/api/users/me/').status_code, 204)
        self.auth(self.a)
        me = self.client.get('/api/users/me/').data
        self.assertEqual(set(me), PRIVATE_FIELDS)
        self.assertEqual(me['email'], self.a.email)
        self.assertTrue(me['phone'])
        response = self.client.put('/api/users/update_me/', {
            'username': self.a.username, 'first_name': 'Changed', 'last_name': 'Alpha',
            'email': 'attacker@example.invalid', 'is_staff': True, 'id': self.b.pk,
            'telegram_chat_id': '999', 'password': 'replacement', 'phone': '+12025550102',
        }, format='json')
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(set(response.data), PRIVATE_FIELDS)
        self.a.refresh_from_db()
        self.assertEqual(self.a.first_name, 'Changed')
        self.assertEqual(self.a.email, 'a@example.invalid')
        self.assertFalse(self.a.is_staff)
        self.assertIsNone(self.a.telegram_chat_id)
        self.assertTrue(self.a.check_password('safe-test-password'))

    def test_unauthenticated_mutations_rejected(self):
        for method, url in [('put', '/api/users/update_me/'), ('post', '/api/users/like_character/'),
                            ('post', '/api/users/telegram_link/'), ('post', '/api/notifications/viewed/')]:
            self.assertEqual(getattr(self.client, method)(url, {}, format='json').status_code, 401)

    def test_application_ownership_all_read_paths(self):
        self.assertEqual(self.client.get('/api/applications/').status_code, 401)
        for user in [self.a, self.b, self.staff]:
            self.auth(user)
            expected = list(Application.objects.filter(user=user).values_list('pk', flat=True))
            data = self.client.get('/api/applications/?user_id=999').data
            self.assertCountEqual([item['id'] for item in data], expected)
            foreign = self.app_b if user != self.b else self.app_a
            self.assertEqual(self.client.get(f'/api/applications/{foreign.pk}/').status_code, 404)
            self.assertEqual(self.client.get(f'/api/applications/get/?game_alias=public&user_id={foreign.user_id}').status_code, 400)
        self.auth(self.a)
        data = self.client.get('/api/applications/get/?game_alias=public').data
        self.assertEqual(data['id'], self.app_a.pk)
        self.assertIn('only-alpha', str(data))
        self.assertNotIn('only-beta', str(data))
        self.assertEqual(self.client.get('/api/applications/get/?game_alias=missing').data, {})

    def test_application_owner_delete_restore(self):
        self.auth(self.a)
        for action, status in [('delete', Application.Status.DELETED), ('restore', Application.Status.PENDING)]:
            response = self.client.post(f'/api/applications/{action}/', {'game_alias': 'public', 'user_id': self.b.pk})
            self.assertEqual(response.status_code, 200)
            self.app_a.refresh_from_db()
            self.app_b.refresh_from_db()
            self.assertEqual(self.app_a.status, status)
            self.assertEqual(self.app_b.status, Application.Status.PENDING)

    def test_closed_roles_all_paths_and_staff_preview(self):
        for user in [None, self.a, self.staff]:
            self.auth(user)
            for endpoint in ['characters', 'groups', 'tags']:
                response = self.client.get(f'/api/games/{endpoint}/?game_alias=closed')
                self.assertEqual(response.status_code, 200 if user == self.staff else 404)
        self.auth(self.a)
        self.assertEqual(self.client.get(f'/api/applications/{self.closed_app.pk}/').data['character']['id'], self.secret_char.pk)

    def test_hidden_groups_ancestors_and_families_never_leak(self):
        hidden = Group.objects.create(name='Secret faction', game=self.game, hidden=True)
        descendant = Group.objects.create(name='Secret descendant', game=self.game, parent=hidden)
        deep = Group.objects.create(name='Secret deep descendant', game=self.game, parent=descendant)
        hidden_family = Group.objects.create(name='Secret family', game=self.game, family=True, hidden=True)
        secret_chars = [Character.objects.create(name='Secret role', alias='secret', group=g, family=self.group)
                        for g in [hidden, descendant, deep]]
        secret_chars.append(Character.objects.create(name='Secret family role', alias='secret', group=self.child, family=hidden_family))
        secret_tag = Tag.objects.create(name='Secret tag')
        for character in secret_chars:
            character.tags.add(secret_tag)
        for user in [None, self.a, self.staff]:
            self.auth(user)
            for endpoint in ['groups', 'characters', 'tags']:
                response = self.client.get(f'/api/games/{endpoint}/?game_alias=public')
                self.assertEqual(response.status_code, 200)
                self.assertNotIn('Secret', str(response.data))
            games = self.client.get('/api/games/').data
            self.assertEqual(next(g for g in games if g['alias'] == 'public')['player_count'], 1)
            if user:
                for character in secret_chars:
                    response = self.client.post('/api/users/like_character/', {
                        'game_alias': 'public', 'character_id': character.pk, 'like': True}, format='json')
                    self.assertEqual(response.status_code, 404)

    def test_likes_validate_input_and_publication(self):
        self.auth(self.a)
        url = '/api/users/like_character/'
        for data, expected in [({}, 400), ({'game_alias': 'public', 'character_id': 999, 'like': True}, 404),
                               ({'game_alias': 'closed', 'character_id': self.secret_char.pk, 'like': True}, 404),
                               ({'game_alias': 'public', 'character_id': self.char.pk, 'like': 'nonsense'}, 400)]:
            self.assertEqual(self.client.post(url, data, format='json').status_code, expected)
        for liked in [True, False]:
            self.assertEqual(self.client.post(url, {'game_alias': 'public', 'character_id': self.char.pk, 'like': liked}, format='json').status_code, 200)
            self.assertEqual(self.a.likes.filter(pk=self.char.pk).exists(), liked)

    def test_notifications_only_current_user(self):
        own = Notification.objects.create(user=self.a)
        other = Notification.objects.create(user=self.b)
        self.auth(self.a)
        self.assertEqual(self.client.post('/api/notifications/viewed/').status_code, 204)
        own.refresh_from_db()
        other.refresh_from_db()
        self.assertTrue(own.viewed)
        self.assertFalse(other.viewed)

    def test_login_validation_inactive_and_logout_revocation(self):
        url = '/api/token/login/'
        for data in [{}, {'login_field': self.a.username}, {'login_field': self.a.username, 'password': 'wrong'}]:
            self.assertEqual(self.client.post(url, data).status_code, 400)
        self.b.is_active = False
        self.b.save()
        self.assertEqual(self.client.post(url, {'login_field': self.b.username, 'password': 'safe-test-password'}).status_code, 400)
        self.assertFalse(Token.objects.filter(user=self.b).exists())
        for login in [self.a.username, self.a.email]:
            response = self.client.post(url, {'login_field': login, 'password': 'safe-test-password'})
            self.assertEqual(response.status_code, 200)
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.assertEqual(self.client.post('/api/token/logout/').status_code, 204)
        self.assertEqual(self.client.get('/api/users/me/').status_code, 401)

    def test_telegram_issue_is_post_only_and_not_in_me(self):
        self.auth(self.a)
        self.assertEqual(self.client.get('/api/users/telegram_link/').status_code, 405)
        response = self.client.post('/api/users/telegram_link/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Cache-Control'], 'no-store')
        self.assertEqual(len(response.data['code']), 43)
        self.assertNotIn('telegram_code', self.client.get('/api/users/me/').data)
        self.assertNotEqual(OneTimeToken.objects.get(user=self.a).digest, response.data['code'])

    def test_link_issuance_is_throttled(self):
        self.auth(self.a)
        for _ in range(5):
            self.assertEqual(self.client.post('/api/users/telegram_link/').status_code, 200)
        self.assertEqual(self.client.post('/api/users/telegram_link/').status_code, 429)

    def test_admin_side_effect_urls_require_staff_model_permission_post_and_csrf(self):
        for path, target, permission in [
            ('application/export', 'apps.games.admin.application.export_apps', 'view_application'),
            ('character/reload', 'apps.games.admin.character.load_chars', 'change_character'),
        ]:
            url = f'/admin/games/{path}/'
            client = Client()
            with patch(target) as external:
                for user in [None, self.a]:
                    if user:
                        client.force_login(user)
                    self.assertEqual(client.post(url).status_code, 302)
                    external.assert_not_called()
                client.force_login(self.staff)
                self.assertEqual(client.get(url).status_code, 405)
                self.assertEqual(client.post(url).status_code, 403)
                self.staff.user_permissions.add(Permission.objects.get(codename=permission))
                csrf_client = Client(enforce_csrf_checks=True)
                csrf_client.force_login(self.staff)
                self.assertEqual(csrf_client.post(url).status_code, 403)
                external.assert_not_called()
                self.assertEqual(client.post(url).status_code, 302)
                external.assert_called_once()


class TelegramLinks(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user('link-test', 'link@example.invalid')

    def test_expiry_rotation_replay_legacy_and_existing_chat(self):
        old = issue_link(self.user)
        code = issue_link(self.user)
        for bad in [old, 'invalid', b64encode(str(self.user.uuid).encode()).decode()]:
            with self.assertRaises(ValueError):
                consume_link(bad, 1001, 'synthetic')
        OneTimeToken.objects.filter(user=self.user).update(expires_at=timezone.now()-timedelta(seconds=1))
        with self.assertRaises(ValueError):
            consume_link(code, 1001, 'synthetic')
        code = issue_link(self.user)
        self.assertFalse(consume_link(code, 1001, 'synthetic'))
        with self.assertRaises(ValueError):
            consume_link(code, 1002, 'other')
        other = User.objects.create_user('other-link', 'other-link@example.invalid')
        with self.assertRaises(ValueError):
            consume_link(issue_link(other), 1001, 'synthetic')
        self.assertTrue(consume_link(issue_link(self.user), 1002, 'changed'))

    def test_actions_are_independent_and_cannot_be_substituted(self):
        telegram = issue_link(self.user)
        password = issue_token(self.user, OneTimeToken.Action.PASSWORD_CHANGE)
        with self.assertRaises(ValueError):
            consume_link(password, 1001, 'synthetic')
        with self.assertRaises(ValueError):
            consume_token(telegram, OneTimeToken.Action.PASSWORD_CHANGE, lambda user: None)
        replacement = issue_token(self.user, OneTimeToken.Action.PASSWORD_CHANGE)
        with self.assertRaises(ValueError):
            consume_token(password, OneTimeToken.Action.PASSWORD_CHANGE, lambda user: None)
        self.assertFalse(consume_link(telegram, 1001, 'synthetic'))
        self.assertEqual(consume_token(replacement, OneTimeToken.Action.PASSWORD_CHANGE, lambda user: user.pk), self.user.pk)
        with self.assertRaises(ValueError):
            consume_token(replacement, OneTimeToken.Action.PASSWORD_CHANGE, lambda user: None)

    def test_effect_failure_rolls_back_consumption_and_database_changes(self):
        code = issue_token(self.user, OneTimeToken.Action.PASSWORD_CHANGE)
        def failing_change(user):
            user.first_name = 'Should roll back'
            user.save(update_fields=['first_name'])
            raise RuntimeError('Synthetic failure')
        with self.assertRaises(RuntimeError):
            consume_token(code, OneTimeToken.Action.PASSWORD_CHANGE, failing_change)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, '')
        self.assertIsNone(OneTimeToken.objects.get(user=self.user).consumed_at)
        consume_token(code, OneTimeToken.Action.PASSWORD_CHANGE, lambda user: None)

    def test_inactive_accounts_and_unknown_actions_are_rejected(self):
        code = issue_link(self.user)
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])
        with self.assertRaises(ValueError):
            consume_link(code, 1001, 'synthetic')
        with self.assertRaises(ValueError):
            issue_link(self.user)
        with self.assertRaises(ValueError):
            issue_token(self.user, 'unrecognised')

    def test_actions_are_independent_and_cannot_be_substituted(self):
        telegram = issue_link(self.user)
        password = issue_token(self.user, OneTimeToken.Action.PASSWORD_CHANGE)
        with self.assertRaises(ValueError):
            consume_link(password, 1001, 'synthetic')
        with self.assertRaises(ValueError):
            consume_token(telegram, OneTimeToken.Action.PASSWORD_CHANGE, lambda user: None)
        replacement = issue_token(self.user, OneTimeToken.Action.PASSWORD_CHANGE)
        with self.assertRaises(ValueError):
            consume_token(password, OneTimeToken.Action.PASSWORD_CHANGE, lambda user: None)
        self.assertFalse(consume_link(telegram, 1001, 'synthetic'))
        self.assertEqual(consume_token(replacement, OneTimeToken.Action.PASSWORD_CHANGE, lambda user: user.pk), self.user.pk)
        with self.assertRaises(ValueError):
            consume_token(replacement, OneTimeToken.Action.PASSWORD_CHANGE, lambda user: None)

    def test_effect_failure_rolls_back_consumption_and_database_changes(self):
        code = issue_token(self.user, OneTimeToken.Action.PASSWORD_CHANGE)
        def failing_change(user):
            user.first_name = 'Should roll back'
            user.save(update_fields=['first_name'])
            raise RuntimeError('Synthetic failure')
        with self.assertRaises(RuntimeError):
            consume_token(code, OneTimeToken.Action.PASSWORD_CHANGE, failing_change)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, '')
        self.assertIsNone(OneTimeToken.objects.get(user=self.user).consumed_at)
        consume_token(code, OneTimeToken.Action.PASSWORD_CHANGE, lambda user: None)

    def test_inactive_accounts_and_unknown_actions_are_rejected(self):
        code = issue_link(self.user)
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])
        with self.assertRaises(ValueError):
            consume_link(code, 1001, 'synthetic')
        with self.assertRaises(ValueError):
            issue_link(self.user)
        with self.assertRaises(ValueError):
            issue_token(self.user, 'unrecognised')

    def race(self, codes, chats):
        barrier = Barrier(2)
        def worker(args):
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                consume_link(args[0], args[1], 'synthetic')
                return True
            except ValueError:
                return False
            finally:
                close_old_connections()
        with ThreadPoolExecutor(max_workers=2) as pool:
            return list(pool.map(worker, zip(codes, chats)))

    def test_concurrent_replay_has_exactly_one_winner(self):
        code = issue_link(self.user)
        self.assertCountEqual(self.race([code, code], [1001, 1002]), [True, False])

    def test_concurrent_chat_claim_has_exactly_one_winner(self):
        other = User.objects.create_user('other-link', 'other-link@example.invalid')
        self.assertCountEqual(self.race([issue_link(self.user), issue_link(other)], [1001, 1001]), [True, False])
        self.assertEqual(User.objects.filter(telegram_chat_id='1001').count(), 1)


class BotGuards(SimpleTestCase):
    def test_group_and_supergroup_cannot_link(self):
        from bot.conversations.login_conversation import code, start
        for kind in ['group', 'supergroup', 'channel']:
            update = SimpleNamespace(effective_chat=SimpleNamespace(type=kind))
            with patch('bot.database.user_tg', new_callable=AsyncMock) as link:
                asyncio.run(start(update, SimpleNamespace(args=['anything'])))
                asyncio.run(code(update, SimpleNamespace(args=['anything'])))
                link.assert_not_called()

    def test_invalid_code_replies_without_logging_credentials(self):
        from bot.conversations.login_conversation import code, chat_attempts
        chat_attempts.cache_clear()
        update = SimpleNamespace(effective_chat=SimpleNamespace(type='private', id=1003),
                                 effective_user=SimpleNamespace(username='synthetic'),
                                 message=SimpleNamespace(reply_text=AsyncMock()))
        with patch('bot.database.user_tg', new_callable=AsyncMock, side_effect=ValueError) as link:
            for _ in range(6):
                asyncio.run(code(update, SimpleNamespace(args=['malformed'])))
            self.assertEqual(link.await_count, 5)
            self.assertEqual(update.message.reply_text.await_count, 6)
