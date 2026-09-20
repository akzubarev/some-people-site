"""Optional OCI S3 media configuration; local development stays filesystem-based."""
from urllib.parse import urlsplit

from django.core.exceptions import ImproperlyConfigured


def media_storages(environ):
    backend = environ.get('MEDIA_STORAGE', 'local')
    storages = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    }
    if backend == 'local':
        return storages
    if backend != 's3':
        raise ImproperlyConfigured('MEDIA_STORAGE must be local or s3.')

    required = ('MEDIA_S3_ENDPOINT_URL', 'MEDIA_S3_REGION', 'MEDIA_S3_BUCKET',
                'MEDIA_S3_ACCESS_KEY_ID', 'MEDIA_S3_SECRET_ACCESS_KEY')
    missing = [name for name in required if not environ.get(name, '').strip()]
    if missing:
        raise ImproperlyConfigured('Missing media storage settings: ' + ', '.join(missing))
    endpoint = urlsplit(environ['MEDIA_S3_ENDPOINT_URL'])
    if (endpoint.scheme != 'https' or not endpoint.hostname or endpoint.username
            or endpoint.password or endpoint.query or endpoint.fragment
            or endpoint.path not in ('', '/')):
        raise ImproperlyConfigured('MEDIA_S3_ENDPOINT_URL must be an HTTPS service endpoint.')
    location = environ.get('MEDIA_S3_PREFIX', '').strip('/')
    if '\\' in location or (location and any(part in ('.', '..', '') for part in location.split('/'))):
        raise ImproperlyConfigured('MEDIA_S3_PREFIX must be a relative object prefix.')
    try:
        expires = int(environ.get('MEDIA_S3_URL_TTL', '3600'))
        if not 60 <= expires <= 604800:
            raise ValueError
    except ValueError:
        raise ImproperlyConfigured('MEDIA_S3_URL_TTL must be between 60 and 604800 seconds.')

    storages['default'] = {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'endpoint_url': environ['MEDIA_S3_ENDPOINT_URL'].rstrip('/'),
            'region_name': environ['MEDIA_S3_REGION'],
            'bucket_name': environ['MEDIA_S3_BUCKET'],
            'access_key': environ['MEDIA_S3_ACCESS_KEY_ID'],
            'secret_key': environ['MEDIA_S3_SECRET_ACCESS_KEY'],
            'location': location,
            'addressing_style': 'path',
            'signature_version': 's3v4',
            # OCI uses bucket policies, not object ACLs.
            'default_acl': None,
            'querystring_auth': True,
            'querystring_expire': expires,
            'file_overwrite': False,
            'custom_domain': None,
            'max_memory_size': 5 * 1024 * 1024,
        },
    }
    return storages
