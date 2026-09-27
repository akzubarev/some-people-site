"""Disposable, synthetic browser-test stack. No application environment is loaded."""
from .security_test_settings import *  # noqa: F403

DATABASES = {'default': {**DATABASES['default'], 'HOST': 'browser-db'}}  # noqa: F405
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'host.docker.internal', 'browser-api']
REST_FRAMEWORK = {**REST_FRAMEWORK, 'DEFAULT_THROTTLE_RATES': {'anon': '1000/minute', 'user': '1000/minute'}}  # noqa: F405
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
MEDIA_ROOT = '/tmp/browser-test-media'
