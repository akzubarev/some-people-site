"""Synthetic PostgreSQL test environment. Never connects to the application DB."""
from unittest.mock import patch
import os

os.environ['GOOGLE_API_KEY'] = 'synthetic-tests-only'

# Existing project settings use dotenv; tests must not load a developer's secrets.
with patch('dotenv.load_dotenv'), patch.dict(os.environ, {'MEDIA_STORAGE': 'local'}):
    from .settings import *  # noqa: F403

SECRET_KEY = 'synthetic-security-tests-only'
DEBUG = False
ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'security_tests', 'USER': 'security_tests',
    'PASSWORD': 'synthetic-tests-only', 'HOST': 'security-db', 'PORT': '5432',
}}
CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
LOGGING = {}
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
MEDIA_ROOT = '/tmp/security-test-media'
