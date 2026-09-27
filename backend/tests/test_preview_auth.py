"""A restored account must authenticate with the same password as on the live site."""
from django.contrib.auth.hashers import MD5PasswordHasher, PBKDF2PasswordHasher, identify_hasher
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from config.preview_settings import PASSWORD_HASHERS
from apps.games.models import Game
from apps.users.models import User


@override_settings(PASSWORD_HASHERS=PASSWORD_HASHERS)
class PreviewAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.password = 'restored-account-test-123'
        hasher = PBKDF2PasswordHasher()
        # Encode directly: the broken MD5-only configuration cannot resolve this hasher.
        encoded = hasher.encode(self.password, hasher.salt())
        self.user = User.objects.create(username='restored-player', email='restored@example.invalid', password=encoded)
        self.game = Game.objects.create(alias='preview-game', title='Preview', open_applications=True)

    def test_restored_password_opens_session_and_application(self):
        csrf = self.client.get('/api/session/').data['csrfToken']
        response = self.client.post('/api/session/', {
            'login_field': self.user.email, 'password': self.password,
        }, HTTP_X_CSRFTOKEN=csrf)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get('/api/session/').data['user']['id'], self.user.pk)
        self.assertEqual(self.client.get('/api/applications/get/', {'game_alias': self.game.alias}).data, {})
        response = self.client.post('/api/applications/apply/', {'game_alias': self.game.alias},
                                    HTTP_X_CSRFTOKEN=response.data['csrfToken'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get('/api/applications/get/', {'game_alias': self.game.alias}).data['id'], response.data['id'])
        self.user.refresh_from_db()
        self.assertEqual(identify_hasher(self.user.password).algorithm, 'pbkdf2_sha256')

    def test_new_preview_accounts_use_normal_password_hashing(self):
        response = self.client.post('/api/session/register/', {
            'username': 'new-preview-player', 'email': 'new-preview@example.invalid',
            'first_name': 'Test', 'last_name': 'Player', 'password': self.password,
        }, HTTP_X_CSRFTOKEN=self.client.get('/api/session/').data['csrfToken'])
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='new-preview-player')
        self.assertEqual(identify_hasher(user.password).algorithm, 'pbkdf2_sha256')
        self.assertEqual(self.client.get('/api/session/').data['user']['id'], user.pk)

    def test_earlier_preview_accounts_upgrade_on_login(self):
        hasher = MD5PasswordHasher()
        self.user.password = hasher.encode(self.password, hasher.salt())
        self.user.save(update_fields=['password'])
        response = self.client.post('/api/session/', {
            'login_field': self.user.username, 'password': self.password,
        }, HTTP_X_CSRFTOKEN=self.client.get('/api/session/').data['csrfToken'])
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(identify_hasher(self.user.password).algorithm, 'pbkdf2_sha256')
