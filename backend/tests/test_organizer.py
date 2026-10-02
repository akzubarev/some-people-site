"""Organizer content contracts against synthetic records."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.db import close_old_connections, IntegrityError, transaction
from django.test import TestCase, TransactionTestCase
from rest_framework.test import APIClient

from apps.games.models import Application, Game
from apps.games.organizer import game_revision
from apps.users.models import User

URL = '/api/organizer/games/'


class OrganizerGamesTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user('editor', 'editor@example.invalid', is_staff=True)
        self.staff.user_permissions.set(Permission.objects.filter(content_type__app_label='games',
                                                                  codename__in=['view_game', 'add_game', 'change_game']))
        self.game = Game.objects.create(title='Original', alias='original', price=1000, player_count=75)
        self.client = APIClient()
        self.client.force_authenticate(self.staff)

    def update(self, **data):
        return self.client.patch(URL + str(self.game.pk) + '/',
            {'expected_revision': game_revision(self.game), **data}, format='json')

    def test_anonymous_player_and_unprivileged_staff_cannot_access(self):
        for user in [None, User.objects.create_user('player', 'player@example.invalid'),
                     User.objects.create_user('staff', 'staff@example.invalid', is_staff=True)]:
            self.client.force_authenticate(user)
            for method, path in [('get', URL), ('get', URL + str(self.game.pk) + '/'),
                                 ('post', URL), ('patch', URL + str(self.game.pk) + '/')]:
                with self.subTest(user=user, method=method):
                    self.assertIn(getattr(self.client, method)(path).status_code, [401, 403])

    def test_nonstaff_with_model_permissions_cannot_write(self):
        self.staff.is_staff = False
        self.staff.save()
        self.assertEqual(self.update(title='Forbidden').status_code, 403)

    def test_read_only_staff_cannot_create_or_update(self):
        reader = User.objects.create_user('reader', 'reader@example.invalid', is_staff=True)
        reader.user_permissions.add(Permission.objects.get(codename='view_game', content_type__app_label='games'))
        self.client.force_authenticate(reader)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['permissions']['change'])
        self.assertEqual(self.client.post(URL, {'title': 'No', 'alias': 'no'}).status_code, 403)
        self.assertEqual(self.update(title='No').status_code, 403)

    def test_complete_private_shape_and_public_shape_are_separate(self):
        response = self.client.get(URL)
        self.assertEqual(response['Cache-Control'], 'no-store')
        self.assertEqual(response.data['games'][0]['player_count'], 75)
        self.assertEqual(response.data['games'][0]['price'], 1000)
        self.assertIn('revision', response.data['games'][0])
        public = self.client.get('/api/games/original/').data
        self.assertEqual(public['player_count'], 0)
        self.assertNotIn('revision', public)
        self.assertNotIn('expected_revision', public)

    def test_create_closed_game_then_update_all_fields_and_audit(self):
        response = self.client.post(URL, {'title': 'New', 'alias': 'new-game'}, format='json')
        self.assertEqual(response.status_code, 201, response.data)
        self.assertFalse(response.data['open_applications'])
        self.assertFalse(response.data['open_character_list'])
        payload = {'expected_revision': response.data['revision'], 'title': 'Edited', 'alias': 'edited',
            'description': 'Long text', 'short_description': 'Short text', 'location': 'Venue', 'year': 2028,
            'price': 6500, 'player_count': 80, 'start': '2028-02-01T18:00:00+03:00',
            'end': '2028-02-03T16:00:00+03:00', 'vk': 'example', 'tg': 'example',
            'open_applications': True, 'open_character_list': True}
        changed = self.client.patch(URL + str(response.data['id']) + '/', payload, format='json')
        self.assertEqual(changed.status_code, 200, changed.data)
        for field in ['title', 'alias', 'description', 'short_description', 'location', 'year', 'price',
                      'player_count', 'vk', 'tg', 'open_applications', 'open_character_list']:
            self.assertEqual(changed.data[field], payload[field])
        self.assertNotEqual(changed.data['revision'], response.data['revision'])
        self.assertEqual(LogEntry.objects.filter(object_id=str(response.data['id'])).count(), 2)

    def test_stale_revision_and_missing_revision_do_not_overwrite(self):
        revision = game_revision(self.game)
        self.assertEqual(self.update(title='First').status_code, 200)
        self.assertEqual(self.client.patch(URL + str(self.game.pk) + '/',
            {'expected_revision': revision, 'title': 'Stale'}, format='json').status_code, 409)
        self.assertEqual(self.client.patch(URL + str(self.game.pk) + '/', {'title': 'Missing'}).status_code, 400)
        self.game.refresh_from_db()
        self.assertEqual(self.game.title, 'First')

    def test_invalid_alias_dates_numbers_and_create_publication(self):
        for alias in ['original', '123', 'groups', 'characters', 'tags', 'new', 'bad/path']:
            with self.subTest(alias=alias):
                self.assertEqual(self.client.post(URL, {'title': 'Test', 'alias': alias}).status_code, 400)
        for data in [{'price': -1}, {'player_count': -1}, {'start': '2028-02-02T18:00:00Z', 'end': '2028-02-01T18:00:00Z'}]:
            self.assertEqual(self.update(**data).status_code, 400)
        self.assertEqual(self.client.post(URL, {'title': 'Test', 'alias': 'test', 'open_applications': True}, format='json').status_code, 400)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Game.objects.create(title='Duplicate', alias='ORIGINAL')

    def test_game_fee_and_closing_do_not_change_existing_applications(self):
        application = Application.objects.create(user=self.staff, game=self.game, price=1000)
        self.assertEqual(self.update(price=9000, open_applications=False).status_code, 200)
        application.refresh_from_db()
        self.assertEqual(application.price, 1000)

    def test_session_mutations_require_csrf(self):
        browser = APIClient(enforce_csrf_checks=True)
        browser.force_login(self.staff)
        self.assertEqual(browser.patch(URL + str(self.game.pk) + '/',
            {'expected_revision': game_revision(self.game), 'title': 'CSRF'}, format='json').status_code, 403)


class OrganizerConcurrentSaveTests(TransactionTestCase):
    def test_committed_update_invalidates_cached_public_index_and_detail(self):
        cache.clear()
        user = User.objects.create_superuser('owner', 'owner@example.invalid', 'password')
        game = Game.objects.create(title='Before', alias='cached')
        client = APIClient()
        client.get('/api/games/')
        client.get('/api/games/cached/')
        client.force_authenticate(user)
        self.assertEqual(client.patch(URL + str(game.pk) + '/',
            {'expected_revision': game_revision(game), 'title': 'After'}, format='json').status_code, 200)
        client.force_authenticate(None)
        self.assertEqual(client.get('/api/games/').data[0]['title'], 'After')
        self.assertEqual(client.get('/api/games/cached/').data['title'], 'After')

    def test_only_one_editor_can_save_the_same_revision(self):
        user = User.objects.create_superuser('owner', 'owner@example.invalid', 'password')
        game = Game.objects.create(title='Before', alias='race')
        revision, barrier = game_revision(game), Barrier(2)

        def save(title):
            close_old_connections()
            try:
                client = APIClient()
                client.force_authenticate(User.objects.get(pk=user.pk))
                barrier.wait(timeout=10)
                return client.patch(URL + str(game.pk) + '/',
                    {'expected_revision': revision, 'title': title}, format='json').status_code
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(save, ['One', 'Two']))
        self.assertEqual(sorted(results), [200, 409])
