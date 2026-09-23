"""Browser authentication must enforce CSRF even before a session exists."""
from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from apps.users.models import User


class BrowserSessionTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user('browser', 'browser@example.invalid', 'test-password-123')
        self.client = APIClient(enforce_csrf_checks=True)

    def bootstrap(self):
        response = self.client.get('/api/session/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Cache-Control'], 'no-store')
        return response.data['csrfToken']

    def test_login_requires_csrf_and_rotates_session(self):
        credentials = {'login_field': 'browser', 'password': 'test-password-123'}
        self.assertEqual(self.client.post('/api/session/', credentials).status_code, 403)
        csrf = self.bootstrap()
        response = self.client.post('/api/session/', credentials, HTTP_X_CSRFTOKEN=csrf)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['username'], 'browser')
        self.assertNotIn('auth_token', response.data)
        self.assertTrue(self.client.cookies['sessionid']['httponly'])
        self.assertFalse(Token.objects.filter(user=self.user).exists())
        profile = {'username': 'browser', 'first_name': 'Test', 'last_name': 'Person'}
        self.assertEqual(self.client.put('/api/users/update_me/', profile).status_code, 403)
        self.assertEqual(self.client.put('/api/users/update_me/', profile,
                         HTTP_X_CSRFTOKEN=response.data['csrfToken']).status_code, 200)
        self.assertEqual(self.client.delete('/api/session/').status_code, 403)
        self.assertEqual(self.client.delete('/api/session/', HTTP_X_CSRFTOKEN=csrf).status_code, 403)
        self.assertEqual(self.client.delete('/api/session/',
                         HTTP_X_CSRFTOKEN=response.data['csrfToken']).status_code, 200)
        self.assertIsNone(self.client.get('/api/session/').data['user'])

    def test_cross_origin_login_and_registration_blocked(self):
        csrf = self.bootstrap()
        for url in ['/api/session/', '/api/session/register/']:
            response = self.client.post(url, {}, HTTP_X_CSRFTOKEN=csrf,
                                        HTTP_ORIGIN='https://untrusted.example')
            self.assertEqual(response.status_code, 403)

    def test_registration_creates_session_without_token(self):
        payload = {'username': 'new-browser', 'email': 'new@example.invalid',
                   'first_name': 'Test', 'last_name': 'Person', 'password': 'different-password-123'}
        self.assertEqual(self.client.post('/api/session/register/', payload).status_code, 403)
        response = self.client.post('/api/session/register/', payload,
                                    HTTP_X_CSRFTOKEN=self.bootstrap())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.get('/api/users/me/').data['username'], 'new-browser')
        self.assertFalse(Token.objects.filter(user__username='new-browser').exists())

    def test_session_discovery_does_not_exhaust_login_quota(self):
        for _ in range(12):
            csrf = self.bootstrap()
        response = self.client.post('/api/session/',
            {'login_field': 'browser', 'password': 'test-password-123'}, HTTP_X_CSRFTOKEN=csrf)
        self.assertEqual(response.status_code, 200)
