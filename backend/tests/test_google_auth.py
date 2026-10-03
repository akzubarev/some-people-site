"""Google auth regression coverage uses synthetic claims and a disposable DB."""
from datetime import timedelta
from unittest.mock import patch
from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError
from apps.users.google_auth import verify_identity
from apps.users.models import GoogleChallenge, GoogleIdentity, User


@override_settings(GOOGLE_OAUTH_CLIENT_ID='synthetic-client')
class GoogleAuthTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient(enforce_csrf_checks=True)
        self.user = User.objects.create_user('existing', 'existing@example.invalid', 'synthetic-password')
        self.csrf = self.client.get('/api/session/').data['csrfToken']

    def send(self, path, data, method='post', client=None):
        return getattr(client or self.client, method)('/api/session/google/' + path, data, format='json', HTTP_X_CSRFTOKEN=self.csrf)

    def challenge(self, purpose='signin', **kwargs):
        response = self.send('challenge/', {'purpose': purpose, **kwargs})
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response['Cache-Control'], 'no-store')
        return response.data['nonce']

    def claims(self, challenge_nonce, **kwargs):
        return {'iss': 'https://accounts.google.com', 'aud': 'synthetic-client', 'sub': 'subject-1',
                'email': 'new@example.invalid', 'email_verified': True, 'nonce': challenge_nonce, **kwargs}

    def finish(self, nonce, **kwargs):
        with patch('apps.users.google_auth.id_token.verify_oauth2_token', return_value=self.claims(nonce, **kwargs)):
            return self.send('', {'nonce': nonce, 'credential': 'synthetic-credential'})

    def signin_password(self):
        response = self.client.post('/api/session/', {'login_field': 'existing', 'password': 'synthetic-password'}, format='json', HTTP_X_CSRFTOKEN=self.csrf)
        self.assertEqual(response.status_code, 200)
        self.csrf = response.data['csrfToken']

    def test_registration_and_returning_login_issue_only_browser_session(self):
        nonce = self.challenge()
        response = self.finish(nonce)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('auth_token', response.data)
        account = User.objects.get(email='new@example.invalid')
        self.assertFalse(account.has_usable_password())
        self.assertFalse(account.is_staff)
        self.assertEqual(GoogleIdentity.objects.get(subject='subject-1').user, account)
        self.csrf = response.data['csrfToken']
        self.client.delete('/api/session/', HTTP_X_CSRFTOKEN=self.csrf)
        self.csrf = self.client.get('/api/session/').data['csrfToken']
        response = self.finish(self.challenge(), email='changed@example.invalid')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['user']['email'], 'new@example.invalid')

    def test_same_email_never_auto_links_or_creates_duplicate(self):
        response = self.finish(self.challenge(), email='EXISTING@example.invalid')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 1)
        self.assertFalse(GoogleIdentity.objects.exists())
        self.assertIsNone(self.client.get('/api/session/').data['user'])

    def test_explicit_link_preserves_password_and_unlink(self):
        self.signin_password()
        self.assertEqual(self.send('challenge/', {'purpose': 'link'}).status_code, 403)
        nonce = self.challenge('link', password='synthetic-password')
        response = self.finish(nonce, email=self.user.email)
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('synthetic-password'))
        self.csrf = response.data['csrfToken']
        self.assertEqual(self.send('identity/', {'password': 'wrong'}, 'delete').status_code, 403)
        self.assertTrue(GoogleIdentity.objects.exists())
        self.assertEqual(self.send('identity/', {'password': 'synthetic-password'}, 'delete').status_code, 200)
        self.assertFalse(GoogleIdentity.objects.exists())

    def test_link_cannot_move_identity_between_accounts(self):
        other = User.objects.create_user('other', 'other@example.invalid', 'other-password')
        GoogleIdentity.objects.create(user=other, subject='subject-1', email=other.email)
        self.signin_password()
        response = self.finish(self.challenge('link', password='synthetic-password'), email=self.user.email)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(GoogleIdentity.objects.get().user, other)

    def test_second_google_identity_cannot_replace_first(self):
        GoogleIdentity.objects.create(user=self.user, subject='original', email=self.user.email)
        self.signin_password()
        response = self.finish(self.challenge('link', password='synthetic-password'), email=self.user.email)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(GoogleIdentity.objects.get().subject, 'original')

    def test_link_email_cannot_collide_with_other_account(self):
        User.objects.create_user('other', 'other@example.invalid', 'other-password')
        self.signin_password()
        response = self.finish(self.challenge('link', password='synthetic-password'), email='OTHER@example.invalid')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(GoogleIdentity.objects.exists())

    def test_google_only_account_cannot_unlink(self):
        response = self.finish(self.challenge())
        self.csrf = response.data['csrfToken']
        self.assertFalse(self.client.get('/api/session/google/identity/').data['can_unlink'])
        self.assertEqual(self.send('identity/', {'password': 'anything'}, 'delete').status_code, 403)
        self.assertTrue(GoogleIdentity.objects.exists())

    def test_invalid_credentials_are_consumed_and_cannot_be_replayed(self):
        nonce = self.challenge()
        with patch('apps.users.google_auth.id_token.verify_oauth2_token', side_effect=ValueError('invalid signature')):
            self.assertEqual(self.send('', {'nonce': nonce, 'credential': 'invalid'}).status_code, 400)
        self.assertEqual(self.finish(nonce).status_code, 400)
        self.assertFalse(GoogleIdentity.objects.exists())

    def test_success_cannot_be_replayed_from_original_anonymous_session(self):
        nonce = self.challenge()
        original = APIClient(enforce_csrf_checks=True)
        original.cookies = self.client.cookies.copy()
        self.assertEqual(self.finish(nonce).status_code, 200)
        self.assertEqual(self.send('', {'nonce': nonce, 'credential': 'synthetic'}, client=original).status_code, 400)

    def test_cancel_and_expiry_invalidate_challenge(self):
        nonce = self.challenge()
        self.assertEqual(self.send('challenge/', {'nonce': nonce}, 'delete').status_code, 204)
        self.assertEqual(self.finish(nonce).status_code, 400)
        nonce = self.challenge()
        GoogleChallenge.objects.update(expires_at=timezone.now() - timedelta(seconds=1))
        self.assertEqual(self.finish(nonce).status_code, 400)

    def test_challenge_is_bound_to_browser_and_purpose(self):
        nonce = self.challenge()
        stranger = APIClient(enforce_csrf_checks=True)
        csrf = stranger.get('/api/session/').data['csrfToken']
        response = stranger.post('/api/session/google/', {'nonce': nonce, 'credential': 'synthetic'}, format='json', HTTP_X_CSRFTOKEN=csrf)
        self.assertEqual(response.status_code, 400)
        self.signin_password()
        self.assertEqual(self.finish(nonce).status_code, 400)
        self.assertEqual(self.send('challenge/', {'purpose': 'signin'}).status_code, 403)

    def test_csrf_cross_origin_and_anonymous_link_are_blocked(self):
        for path in ['challenge/', '', 'identity/']:
            self.assertEqual(self.client.post('/api/session/google/' + path, {}).status_code, 403)
        self.assertEqual(self.send('challenge/', {'purpose': 'link', 'password': 'synthetic-password'}).status_code, 403)
        self.assertEqual(self.client.post('/api/session/google/challenge/', {}, format='json', HTTP_X_CSRFTOKEN=self.csrf, HTTP_ORIGIN='https://evil.invalid').status_code, 403)

    def test_inactive_google_account_is_rejected(self):
        self.user.is_active = False
        self.user.save()
        GoogleIdentity.objects.create(user=self.user, subject='subject-1', email=self.user.email)
        self.assertEqual(self.finish(self.challenge(), email=self.user.email).status_code, 403)

    def test_verifier_rejects_wrong_audience_issuer_nonce_unverified_email(self):
        for fields in [{'aud': 'other'}, {'iss': 'https://evil.invalid'}, {'nonce': 'different'}, {'nonce': 'неверно'}, {'email_verified': False}, {'sub': ''}]:
            with self.subTest(fields=fields), patch('apps.users.google_auth.id_token.verify_oauth2_token', return_value=self.claims('nonce', **fields)):
                with self.assertRaises(ValidationError):
                    verify_identity('synthetic', 'nonce')

    def test_case_insensitive_email_and_subject_constraints(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            User.objects.create_user('duplicate', 'EXISTING@example.invalid', 'password')
        GoogleIdentity.objects.create(user=self.user, subject='unique', email=self.user.email)
        other = User.objects.create_user('other', 'other@example.invalid', 'password')
        with self.assertRaises(IntegrityError), transaction.atomic():
            GoogleIdentity.objects.create(user=other, subject='unique', email=other.email)

    @override_settings(GOOGLE_OAUTH_CLIENT_ID='')
    def test_disabled_google_keeps_password_login(self):
        self.assertFalse(self.client.get('/api/session/google/identity/').data['enabled'])
        self.assertEqual(self.send('challenge/', {'purpose': 'signin'}).status_code, 400)
        self.signin_password()



@override_settings(GOOGLE_OAUTH_CLIENT_ID='synthetic-client')
class GoogleSignatureTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        cls.key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.private_pem = cls.key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
        cls.public_pem = cls.key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()

    def token(self, **overrides):
        import time
        from google.auth import crypt, jwt
        claims = {'iss': 'https://accounts.google.com', 'aud': 'synthetic-client', 'sub': 'subject',
                  'email': 'synthetic@example.invalid', 'email_verified': True, 'nonce': 'nonce',
                  'iat': int(time.time()) - 10, 'exp': int(time.time()) + 300, **overrides}
        return jwt.encode(crypt.RSASigner.from_string(self.private_pem, key_id='synthetic-key'), claims).decode()

    def transport(self):
        import json
        from types import SimpleNamespace
        response = SimpleNamespace(status=200, data=json.dumps({'synthetic-key': self.public_pem}).encode())
        return patch('apps.users.google_auth.Request', return_value=lambda *args, **kwargs: response)

    def test_real_signature_verification_accepts_valid_and_rejects_expired_or_tampered(self):
        with self.transport():
            self.assertEqual(verify_identity(self.token(), 'nonce')['sub'], 'subject')
            import time
            for token in [self.token(exp=int(time.time()) - 100), self.token(aud='wrong-client'), self.token() + 'tampered']:
                with self.subTest(token=token[-12:]), self.assertRaises(ValidationError):
                    verify_identity(token, 'nonce')


from django.test import TransactionTestCase
from django.db import close_old_connections
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier


@override_settings(GOOGLE_OAUTH_CLIENT_ID='synthetic-client')
class GoogleConcurrencyTests(TransactionTestCase):
    def setUp(self):
        cache.clear()

    def attempt(self):
        client = APIClient(enforce_csrf_checks=True)
        csrf = client.get('/api/session/').data['csrfToken']
        response = client.post('/api/session/google/challenge/', {'purpose': 'signin'}, format='json', HTTP_X_CSRFTOKEN=csrf)
        self.assertEqual(response.status_code, 200)
        return client, csrf, response.data['nonce']

    def run_attempts(self, attempts, subject_by_nonce):
        barrier = Barrier(2)
        def verify(credential, nonce):
            return {'sub': subject_by_nonce[nonce], 'email': 'concurrent@example.invalid', 'given_name': 'Test'}
        def finish(attempt):
            client, csrf, nonce = attempt
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                return client.post('/api/session/google/', {'nonce': nonce, 'credential': 'synthetic'}, format='json', HTTP_X_CSRFTOKEN=csrf).status_code
            finally:
                close_old_connections()
        with patch('apps.users.views.google.verify_identity', side_effect=verify), ThreadPoolExecutor(max_workers=2) as pool:
            return list(pool.map(finish, attempts))

    def test_concurrent_registration_with_same_email_creates_one_account(self):
        first, second = self.attempt(), self.attempt()
        result = self.run_attempts([first, second], {first[2]: 'first-subject', second[2]: 'second-subject'})
        self.assertEqual(sorted(result), [200, 400])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(GoogleIdentity.objects.count(), 1)

    def test_concurrent_replay_creates_one_session_and_account(self):
        original = self.attempt()
        clone = APIClient(enforce_csrf_checks=True)
        clone.cookies = original[0].cookies.copy()
        result = self.run_attempts([original, (clone, original[1], original[2])], {original[2]: 'one-subject'})
        self.assertEqual(sorted(result), [200, 400])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(GoogleIdentity.objects.count(), 1)
