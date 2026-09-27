"""Contracts used by the React forms, exercised with synthetic data."""
from io import BytesIO
from PIL import Image
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from apps.games.models import Answer, Application, Game, Question
from apps.users.models import User


class BrowserInputTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user('form-user', 'form@example.invalid', 'password')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.game = Game.objects.create(title='Open game', alias='forms', open_applications=True)
        self.question = Question.objects.create(title='Choice', type='single_choice', choices=['A', 'B'])
        self.question.games.add(self.game)

    def test_partial_save_rejects_foreign_questions_and_invalid_choices(self):
        other = Question.objects.create(title='Other game')
        for payload in [{f'question_{other.pk}': 'other'}, {f'question_{self.question.pk}': 'C'},
                        {'unexpected': 'value'}]:
            response = self.client.post('/api/applications/apply/', {'game_alias': 'forms', **payload}, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertFalse(Application.objects.exists())
        response = self.client.post('/api/applications/apply/',
            {'game_alias': 'forms', f'question_{self.question.pk}': 'A'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Answer.objects.get().value, 'A')
        self.assertEqual(self.client.post('/api/applications/apply/', {}, format='json').status_code, 404)

    def test_closed_and_deleted_application_writes_are_rejected(self):
        self.game.open_applications = False
        self.game.save()
        self.assertEqual(self.client.post('/api/applications/apply/', {'game_alias': 'forms'}, format='json').status_code, 400)
        Application.objects.create(user=self.user, game=self.game, status='deleted')
        self.assertEqual(self.client.post('/api/applications/apply/', {'game_alias': 'forms'}, format='json').status_code, 400)

    def test_matrix_and_checkbox_shapes(self):
        self.question.type, self.question.choices = 'matrix', [['A', 'B'], ['One', 'Two']]
        self.question.save()
        for value, expected in [([['A'], []], 200), ([['A', 'B'], []], 400),
                                ([['A']], 400), ([['C'], ['A']], 400)]:
            response = self.client.post('/api/applications/apply/',
                {'game_alias': 'forms', f'question_{self.question.pk}': value}, format='json')
            self.assertEqual(response.status_code, expected)

    def test_multipart_profile_preserves_explicit_empty_and_consent_values(self):
        self.user.vk = 'previous'
        self.user.save()
        response = self.client.put('/api/users/update_me/', {
            'username': 'form-user', 'first_name': 'Test', 'last_name': 'Person', 'phone': '',
            'vk': '', 'vk_public': 'false', 'tg_public': 'false',
        }, format='multipart')
        self.assertEqual(response.status_code, 200, response.data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.vk, '')
        self.assertFalse(self.user.vk_public)
        self.assertFalse(self.user.tg_public)

    def test_avatar_decodes_as_image_and_rejects_non_image(self):
        image = BytesIO()
        Image.new('RGB', (4, 4)).save(image, format='PNG')
        for upload, expected in [
            (SimpleUploadedFile('avatar.png', image.getvalue(), 'image/png'), 200),
            (SimpleUploadedFile('avatar.png', b'not an image', 'image/png'), 400),
        ]:
            response = self.client.put('/api/users/update_me/',
                {'username': 'form-user', 'first_name': 'Test', 'last_name': 'Person', 'avatar': upload}, format='multipart')
            self.assertEqual(response.status_code, expected, response.data)
