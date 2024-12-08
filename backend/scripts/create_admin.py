"""Script for creating admin user."""
import os
import sys

import django

from apps.users.models import User

if __name__ == '__main__':
    sys.path[0] = '/app/'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    User.objects.create_superuser(
        username=os.getenv('DJANGO_SUPERUSER_USERNAME'),
        first_name='admin', last_name='admin',
        email=os.getenv('DJANGO_SUPERUSER_EMAIL'),
        password=os.getenv('DJANGO_SUPERUSER_PASSWORD'),
    )
