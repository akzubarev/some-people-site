"""Local-only, restored-dump preview. Never use this module for deployment."""
import os
from unittest.mock import patch

os.environ['GOOGLE_API_KEY'] = 'synthetic-preview-only'
with patch('dotenv.load_dotenv'):
    from .settings import *  # noqa: F403

SECURITY_PREVIEW = True
SECRET_KEY = 'local-security-preview-only'
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'preview-api']
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'security_preview', 'USER': 'postgres',
    'PASSWORD': 'local-preview-only', 'HOST': 'preview-db', 'PORT': '5432',
}}
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
LOGGING = {}
MEDIA_ROOT = '/preview-media'
STATIC_ROOT = '/preview-static'
# The preview stack has no bot and its backend network has no outbound access.
