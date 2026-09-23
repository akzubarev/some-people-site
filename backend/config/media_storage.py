"""Durable image links for HTML saved by CKEditor."""
from pathlib import PurePosixPath

from django.conf import settings
from django.core import signing
from django.core.files.storage import default_storage
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe
from storages.backends.s3 import S3Storage


EDITOR_LINK_SALT = 'some-people.editor-media'


def valid_editor_name(name):
    return (isinstance(name, str) and name.startswith('ckeditor/')
            and not any(part in ('', '.', '..') for part in name.split('/'))
            and '\\' not in name and not PurePosixPath(name).is_absolute())


class EditorMediaStorage(S3Storage):
    """Save shareable editor images in S3 without persisting expiring S3 URLs."""

    def __init__(self, **kwargs):
        super().__init__(**{**settings.STORAGES['default']['OPTIONS'], **kwargs})

    def url(self, name, parameters=None, expire=None, http_method=None):
        if not valid_editor_name(name):
            raise ValueError('Editor media must be inside ckeditor/.')
        token = signing.dumps(name, salt=EDITOR_LINK_SALT)
        return reverse('editor-media', kwargs={'token': token})


@require_safe
@never_cache
def editor_media(request, token):
    # This durable bearer link is issued only by the staff-only editor uploader.
    # It never accepts arbitrary object names or exposes character documents.
    if settings.MEDIA_STORAGE != 's3':
        raise Http404
    try:
        name = signing.loads(token, salt=EDITOR_LINK_SALT)
    except signing.BadSignature:
        raise Http404
    if not valid_editor_name(name):
        raise Http404
    response = HttpResponseRedirect(default_storage.url(name))
    response['Referrer-Policy'] = 'no-referrer'
    return response
