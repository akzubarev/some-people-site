"""Copy local media without deleting originals or changing database file names."""
from hashlib import sha256
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError


MEDIA_PREFIXES = ('users/avatars/', 'characters/images/', 'groups/images/',
                  'mailing/images/', 'kventas/pdf/', 'ckeditor/')


def digest(stream):
    result = sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b''):
        result.update(chunk)
    return result.hexdigest()


class Command(BaseCommand):
    help = 'Dry-run local-to-S3 media copy; --apply uploads and verifies each file.'

    def add_arguments(self, parser):
        parser.add_argument('--source', default=settings.MEDIA_ROOT)
        parser.add_argument('--apply', action='store_true')

    def handle(self, *args, **options):
        if settings.MEDIA_STORAGE != 's3':
            raise CommandError('Configure MEDIA_STORAGE=s3 for the destination first.')
        source = Path(options['source'])
        if source.is_symlink() or not source.is_dir():
            raise CommandError('Source must be an existing, non-symlink media directory.')
        source = source.resolve()
        files = []
        for path in sorted(source.rglob('*')):
            if path.is_symlink():
                raise CommandError('Media source contains a symlink; no copy started.')
            if path.is_file():
                name = path.relative_to(source).as_posix()
                if not name.startswith(MEDIA_PREFIXES):
                    raise CommandError('Unexpected media prefix; check the source directory.')
                files.append((path, name))

        copied = identical = pending = 0
        for path, name in files:
            with path.open('rb') as stream:
                local_hash = digest(stream)
            if default_storage.exists(name):
                with default_storage.open(name, 'rb') as stream:
                    remote_hash = digest(stream)
                if local_hash != remote_hash:
                    raise CommandError(f'Destination differs: {name}. Nothing overwritten.')
                identical += 1
                continue
            if not options['apply']:
                pending += 1
                continue
            with path.open('rb') as stream:
                saved = default_storage.save(name, File(stream))
            if saved != name:
                raise CommandError(f'Destination changed during copy: {name}; inspect {saved}.')
            with default_storage.open(name, 'rb') as stream:
                if digest(stream) != local_hash:
                    raise CommandError(f'Verification failed: {name}. Original retained.')
            copied += 1

        mode = 'APPLY' if options['apply'] else 'DRY RUN'
        self.stdout.write(
            f'{mode}: {len(files)} files, {identical} identical, '
            f'{copied} copied and verified, {pending} pending. Originals retained.')
