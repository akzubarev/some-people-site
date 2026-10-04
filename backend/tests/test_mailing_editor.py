"""Mailing editor permissions, safe uploads and existing HTML compatibility."""
from io import BytesIO
from unittest.mock import patch

from django.contrib.auth.models import Permission
from django.core.files.storage import InMemoryStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from PIL import Image

from apps.notifications.organizer import OrganizerMailingSerializer
from apps.games.models import Game
from rest_framework.test import APIClient
from apps.users.models import User
from config.media_storage import EditorMediaStorage


def picture():
    output = BytesIO()
    Image.new('RGB', (3, 3), 'green').save(output, format='PNG')
    return SimpleUploadedFile('input.png', output.getvalue(), content_type='image/png')


class MailingEditorTests(TestCase):
    def setUp(self):
        game = Game.objects.create(title='Upload game', alias='upload-game')
        self.url = f'/api/organizer/games/{game.pk}/mailings/upload/'
        self.client = APIClient()
        self.user = User.objects.create_user(username='editor', password='synthetic', is_staff=True)
        self.user.user_permissions.add(Permission.objects.get(codename='change_mailing'))
        self.client.force_login(self.user)

    def test_editor_assets_and_existing_html(self):
        html = ('<p><strong>Bold</strong><em>Italic</em><u>Underline</u><br>'
                '<a href="https://example.org/">Link</a></p>'
                '<table><tbody><tr><td><p>Cell</p></td></tr></tbody></table>'
                '<img src="/api/media/editor/legacy-token/" alt="Image">')
        cleaned = OrganizerMailingSerializer().validate_text(html)
        for part in ('<strong>Bold</strong>', '<em>Italic</em>', '<u>Underline</u>',
                     '<br>', 'https://example.org/', '<table>', 'Cell',
                     '/api/media/editor/legacy-token/'):
            self.assertIn(part, cleaned)

    def test_html_is_sanitized_on_server(self):
        cleaned = OrganizerMailingSerializer().validate_text(
            '<script>alert(1)</script><p onclick="alert(2)">Safe</p>'
            '<a href="javascript:alert(3)">Link</a><img src="x" onerror="alert(4)">')
        for forbidden in ('<script', 'onclick', 'javascript:', 'onerror'):
            self.assertNotIn(forbidden, cleaned)
        self.assertIn('Safe', cleaned)

    def test_old_editor_routes_are_removed(self):
        self.assertEqual(self.client.get('/editor/upload/').status_code, 404)
        self.assertEqual(self.client.get('/ckeditor/upload/').status_code, 404)
        self.assertEqual(self.client.get('/ckeditor/browse/').status_code, 404)

    def test_anonymous_nonstaff_and_staff_without_permissions_are_denied(self):
        self.client.logout()
        self.assertIn(self.client.post(self.url, {'image': picture()}, format='multipart').status_code, [401, 403])
        for staff, active, permission in ((False, True, True), (True, True, False),
                                          (True, False, True)):
            self.user.is_staff = staff
            self.user.is_active = active
            self.user.save()
            self.user.user_permissions.clear()
            if permission:
                self.user.user_permissions.add(Permission.objects.get(codename='change_mailing'))
            self.client.force_login(self.user)
            self.assertIn(self.client.post(self.url, {'image': picture()}, format='multipart').status_code, [401, 403])

    def test_add_only_organizer_can_upload(self):
        self.user.user_permissions.clear()
        self.user.user_permissions.add(Permission.objects.get(codename='add_mailing'))
        with patch('apps.notifications.editor.default_storage', InMemoryStorage()):
            self.assertEqual(self.client.post(self.url, {'image': picture()}, format='multipart').status_code, 201)

    @override_settings(MEDIA_STORAGE='local')
    def test_local_upload_is_reencoded_and_returns_persistent_url(self):
        storage = InMemoryStorage(base_url='/media/')
        with patch('apps.notifications.editor.default_storage', storage):
            response = self.client.post(self.url, {'image': picture(), 'callback': 7})
        self.assertEqual(response.status_code, 201, response.data)
        result = response.data
        self.assertTrue(result['url'].startswith('/media/editor/'))
        self.assertTrue(result['url'].endswith('.png'))
        name = result['url'].removeprefix('/media/')
        with storage.open(name) as file:
            self.assertEqual(Image.open(file).format, 'PNG')
        self.assertIn('no-store', response['Cache-Control'])

    @override_settings(MEDIA_STORAGE='s3')
    def test_s3_upload_uses_durable_links(self):
        with patch('apps.notifications.editor.EditorMediaStorage') as storage:
            storage.return_value.save.side_effect = lambda name, content: name
            storage.return_value.url.side_effect = lambda name: EditorMediaStorage.url(None, name)
            response = self.client.post(self.url, {'image': picture(), 'callback': 1})
        url = response.data['url']
        self.assertTrue(url.startswith('/api/media/editor/'))
        self.assertNotIn('X-Amz', url)
        with patch('config.media_storage.default_storage.url', return_value='https://example.org/signed'):
            self.assertRedirects(self.client.get(url), 'https://example.org/signed', fetch_redirect_response=False)

    def test_invalid_images_callback_and_large_files_never_reach_storage(self):
        with patch('apps.notifications.editor.default_storage') as storage:
            for data in (
                {'image': SimpleUploadedFile('bad.svg', b'<svg onload="alert(1)"/>'), 'callback': 1},
                {'image': SimpleUploadedFile('big.png', b'x' * (5 * 1024 * 1024 + 1)), 'callback': 1},
            ):
                response = self.client.post(self.url, data)
                self.assertEqual(response.status_code, 400)
            storage.save.assert_not_called()

    def test_csrf_is_required(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.post(self.url, {'image': picture(), 'callback': 1}).status_code, 403)
        client.get('/api/session/')
        with patch('apps.notifications.editor.default_storage', InMemoryStorage()):
            response = client.post(self.url, {'image': picture(), 'callback': 1},
                                   HTTP_X_CSRFTOKEN=client.cookies['csrftoken'].value)
        self.assertEqual(response.status_code, 201)

    def test_storage_failure_keeps_actionable_form_error(self):
        with patch('apps.notifications.editor.default_storage.save', side_effect=OSError):
            response = self.client.post(self.url, {'image': picture(), 'callback': 1})
        self.assertEqual(response.status_code, 400)
        self.assertIn('image', response.data)
