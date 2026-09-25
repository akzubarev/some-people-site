"""Isolated dump-backed preview; never loads production environment values."""
from django.conf import global_settings

from .frontend_test_settings import *  # noqa: F403

# Restored accounts use the normal Django hashers, not the synthetic suite's MD5 shortcut.
PASSWORD_HASHERS = [
    *global_settings.PASSWORD_HASHERS,
    # Accounts created by earlier previews can sign in and upgrade to the default hasher.
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
