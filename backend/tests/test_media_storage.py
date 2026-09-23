"""Media contracts using synthetic bytes and no database or real cloud credentials."""
from io import StringIO
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from botocore.stub import ANY, Stubber
from django.core import signing
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage, InMemoryStorage
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, override_settings
from django.urls import reverse
from storages.backends.s3 import S3Storage

from config.media import media_storages
from config.media_storage import EDITOR_LINK_SALT, EditorMediaStorage
from apps.users.models import User
from apps.users.serializers.user.public import UserPublicSerializer


S3_ENV = {
    'MEDIA_STORAGE': 's3',
    'MEDIA_S3_ENDPOINT_URL': 'https://namespace.compat.objectstorage.region.oraclecloud.com',
    'MEDIA_S3_REGION': 'region',
    'MEDIA_S3_BUCKET': 'synthetic-media',
    'MEDIA_S3_ACCESS_KEY_ID': 'synthetic-access',
    'MEDIA_S3_SECRET_ACCESS_KEY': 'synthetic-secret',
}


class MediaConfiguration(SimpleTestCase):
    def test_local_default_and_static_storage_unchanged(self):
        config = media_storages({})
        self.assertEqual(config['default']['BACKEND'], 'django.core.files.storage.FileSystemStorage')
        self.assertEqual(config['staticfiles']['BACKEND'],
                         'django.contrib.staticfiles.storage.StaticFilesStorage')
        with TemporaryDirectory() as directory:
            storage = FileSystemStorage(location=directory, base_url='/media/')
            self.assertEqual(storage.save('users/avatars/test.txt', ContentFile(b'local')),
                             'users/avatars/test.txt')
            self.assertEqual(storage.url('users/avatars/test.txt'), '/media/users/avatars/test.txt')

    def test_incomplete_or_invalid_config_fails_without_exposing_credentials(self):
        for updates in ({'MEDIA_STORAGE': 'typo'}, {'MEDIA_S3_BUCKET': ''},
                        {'MEDIA_S3_ENDPOINT_URL': 'http://example.invalid'},
                        {'MEDIA_S3_ENDPOINT_URL': 'https://user:password@example.invalid'},
                        {'MEDIA_S3_ENDPOINT_URL': 'https://example.invalid/bucket'},
                        {'MEDIA_S3_PREFIX': '../private'}, {'MEDIA_S3_PREFIX': 'a//b'},
                        {'MEDIA_S3_URL_TTL': '0'}, {'MEDIA_S3_URL_TTL': 'invalid'}):
            with self.subTest(updates=updates), self.assertRaises(ImproperlyConfigured) as error:
                media_storages({**S3_ENV, **updates})
            self.assertNotIn(S3_ENV['MEDIA_S3_SECRET_ACCESS_KEY'], str(error.exception))

    def test_private_path_style_url_uses_oci_region_and_keeps_database_name(self):
        storage = S3Storage(**media_storages({**S3_ENV, 'MEDIA_S3_PREFIX': 'media'})['default']['OPTIONS'])
        name = 'characters/images/portrait with space.png'
        url = urlsplit(storage.url(name))
        self.assertEqual(url.netloc, urlsplit(S3_ENV['MEDIA_S3_ENDPOINT_URL']).netloc)
        self.assertEqual(url.path, '/synthetic-media/media/characters/images/portrait%20with%20space.png')
        query = parse_qs(url.query)
        self.assertEqual(query['X-Amz-Algorithm'], ['AWS4-HMAC-SHA256'])
        self.assertIn('/region/s3/aws4_request', query['X-Amz-Credential'][0])
        self.assertEqual(query['X-Amz-Expires'], ['3600'])
        self.assertFalse(storage.file_overwrite)
        self.assertIsNone(storage.default_acl)

    def test_upload_bytes_and_key_use_s3_without_an_acl(self):
        storage = S3Storage(**media_storages(S3_ENV)['default']['OPTIONS'])
        client = storage.connection.meta.client
        # S3Transfer submits this request for an ordinary avatar upload.
        with Stubber(client) as stub:
            stub.add_response('put_object', {'ETag': '"synthetic"'}, {
                'Bucket': 'synthetic-media', 'Key': 'users/avatars/test.png',
                'Body': ANY, 'ContentType': 'image/png',
            })
            self.assertEqual(storage._save('users/avatars/test.png', ContentFile(b'synthetic-image')),
                             'users/avatars/test.png')
            stub.assert_no_pending_responses()

    def test_wire_upload_signs_payload_without_optional_chunked_trailers(self):
        storage = S3Storage(**media_storages(S3_ENV)['default']['OPTIONS'])
        client = storage.connection.meta.client
        requests = []

        def capture(request, **kwargs):
            requests.append(request)
            raise RuntimeError('stop before network')

        client.meta.events.register('before-send.s3.PutObject', capture)
        payload = b'synthetic-avatar'
        with self.assertRaisesMessage(RuntimeError, 'stop before network'):
            client.put_object(Bucket='synthetic-media', Key='users/avatars/test.png', Body=payload)
        headers = {key.lower(): value for key, value in requests[0].headers.items()}
        self.assertEqual(headers['x-amz-content-sha256'], sha256(payload).hexdigest().encode())
        self.assertNotIn('x-amz-trailer', headers)
        self.assertNotIn(b'aws-chunked', headers.get('content-encoding', b''))

    @override_settings(STORAGES=media_storages(S3_ENV))
    def test_avatar_serializer_emits_signed_url_without_changing_file_name(self):
        user = User(username='synthetic', avatar='users/avatars/synthetic.png')
        data = UserPublicSerializer(user).data
        self.assertIn('X-Amz-Signature=', data['avatar'])
        self.assertEqual(user.avatar.name, 'users/avatars/synthetic.png')
        self.assertNotIn('phone', data)


@override_settings(MEDIA_STORAGE='s3', STORAGES=media_storages(S3_ENV))
class EditorLinks(SimpleTestCase):
    def test_saved_editor_link_resolves_to_a_fresh_signed_url(self):
        storage = EditorMediaStorage()
        url = storage.url('ckeditor/2026/image.png')
        self.assertTrue(url.startswith('/api/media/editor/'))
        self.assertNotIn('X-Amz', url)
        with patch('config.media_storage.default_storage.url',
                   return_value='https://example.invalid/fresh-signed-image') as sign:
            response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://example.invalid/fresh-signed-image')
        self.assertIn('no-store', response['Cache-Control'])
        sign.assert_called_once_with('ckeditor/2026/image.png')

    def test_tampered_links_and_other_prefixes_never_sign_objects(self):
        names = ('kventas/pdf/private.pdf', 'ckeditor/../kventas/private.pdf',
                 '/ckeditor/image.png', 'ckeditor//image.png')
        with patch('config.media_storage.default_storage.url') as sign:
            for name in names:
                token = signing.dumps(name, salt=EDITOR_LINK_SALT)
                self.assertEqual(self.client.get(reverse('editor-media', args=[token])).status_code, 404)
            self.assertEqual(self.client.get(reverse('editor-media', args=['tampered'])).status_code, 404)
            sign.assert_not_called()

    @override_settings(MEDIA_STORAGE='local')
    def test_editor_redirect_disabled_for_local_storage(self):
        token = signing.dumps('ckeditor/image.png', salt=EDITOR_LINK_SALT)
        self.assertEqual(self.client.get(reverse('editor-media', args=[token])).status_code, 404)


@override_settings(MEDIA_STORAGE='s3')
class MediaCopy(SimpleTestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.name = 'users/avatars/synthetic.png'
        path = self.root / self.name
        path.parent.mkdir(parents=True)
        path.write_bytes(b'synthetic-image')
        self.destination = InMemoryStorage()
        self.patch = patch('apps.users.management.commands.copy_media_to_s3.default_storage',
                           self.destination)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def run_copy(self, apply=False):
        output = StringIO()
        call_command('copy_media_to_s3', source=str(self.root), apply=apply, stdout=output)
        return output.getvalue()

    def test_dry_run_does_not_write_and_apply_is_verified_and_idempotent(self):
        self.assertIn('1 pending', self.run_copy())
        self.assertFalse(self.destination.exists(self.name))
        self.assertIn('1 copied and verified', self.run_copy(apply=True))
        self.assertIn('1 identical', self.run_copy(apply=True))
        self.assertEqual((self.root / self.name).read_bytes(), b'synthetic-image')

    def test_existing_different_object_is_never_overwritten(self):
        self.destination.save(self.name, ContentFile(b'original'))
        with self.assertRaisesMessage(CommandError, 'Nothing overwritten'):
            self.run_copy(apply=True)
        self.assertEqual(self.destination.open(self.name).read(), b'original')

    def test_wrong_source_rejected_before_any_upload(self):
        (self.root / '.env').write_text('synthetic-only')
        with self.assertRaisesMessage(CommandError, 'Unexpected media prefix'):
            self.run_copy(apply=True)
        self.assertFalse(self.destination.exists(self.name))

    def test_failed_verification_keeps_local_original(self):
        original_save = self.destination.save

        def corrupt_save(name, content):
            return original_save(name, ContentFile(b'corrupted'))

        with patch.object(self.destination, 'save', side_effect=corrupt_save):
            with self.assertRaisesMessage(CommandError, 'Verification failed'):
                self.run_copy(apply=True)
        self.assertEqual((self.root / self.name).read_bytes(), b'synthetic-image')
