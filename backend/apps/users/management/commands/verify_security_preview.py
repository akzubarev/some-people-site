"""Verify a restored local preview without printing account data."""
import json

from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.games.models import Application, Game, Group
from apps.games.visibility import public_characters, visible_group_ids
from apps.users.models import User
from apps.users.telegram_link import issue_link, consume_link


class Command(BaseCommand):
    help = 'Check the dedicated security_preview DB; never usable against production.'

    def handle(self, *args, **options):
        if not getattr(settings, 'SECURITY_PREVIEW', False) or settings.DATABASES['default']['NAME'] != 'security_preview':
            raise CommandError('Only the isolated security preview is supported.')
        counts = { 'users': User.objects.count(), 'games': Game.objects.count(),
                   'groups': Group.objects.count(), 'applications': Application.objects.count() }
        # Restored credentials must not become usable on a second running service.
        Token.objects.all().delete()
        Session.objects.all().delete()
        local_users = []
        for suffix in ['a', 'b', 'staff']:
            user, _ = User.objects.get_or_create(username=f'security-preview-{suffix}', defaults={
                'email': f'security-preview-{suffix}@example.invalid',
                'first_name': 'Security', 'last_name': 'Preview',
            })
            user.set_password('local-preview-only-change-me')
            user.is_staff = suffix == 'staff'
            user.save()
            local_users.append(user)
        client = APIClient(HTTP_HOST='localhost')
        public_fields = {'username', 'first_name', 'last_name', 'avatar', 'vk', 'telegram'}

        def check_players(data):
            if isinstance(data, dict):
                if data.get('player'):
                    assert set(data['player']) == public_fields
                for value in data.values():
                    check_players(value)
            elif isinstance(data, list):
                for value in data:
                    check_players(value)

        def group_ids(data):
            found = set()
            for group in data:
                found.add(group['id'])
                found.update(group_ids(group['subgroups']))
            return found

        role_counts = {}
        for game in Game.objects.all():
            for endpoint in ['groups', 'characters', 'tags']:
                cache.clear()
                response = client.get(f'/api/games/{endpoint}/', {'game_alias': game.alias})
                assert response.status_code == (200 if game.open_character_list else 404)
                if response.status_code == 200:
                    check_players(response.data)
                    if endpoint == 'groups':
                        assert group_ids(response.data) <= visible_group_ids(game.pk)
                    if endpoint == 'characters':
                        assert {c['id'] for c in response.data} == set(public_characters(game.pk).values_list('pk', flat=True))
                        role_counts[game.alias] = len(response.data)
        assert client.get('/api/users/').status_code == 404
        client.force_authenticate(local_users[2])
        for game in Game.objects.filter(open_character_list=False):
            cache.clear()
            response = client.get('/api/games/groups/', {'game_alias': game.alias})
            assert response.status_code == 200
            assert group_ids(response.data) <= visible_group_ids(game.pk)
            check_players(response.data)
            role_counts[game.alias + '_staff_preview'] = public_characters(game.pk).count()
        client.force_authenticate(None)
        cache.clear()
        assert client.get('/api/applications/').status_code == 401
        checked_owners = 0
        for user in User.objects.filter(applications__isnull=False).distinct()[:3]:
            client.force_authenticate(user)
            cache.clear()
            response = client.get('/api/applications/')
            assert response.status_code == 200
            assert {app['id'] for app in response.data} == set(user.applications.values_list('pk', flat=True))
            foreign = Application.objects.exclude(user=user).first()
            if foreign:
                assert client.get(f'/api/applications/{foreign.pk}/').status_code == 404
                assert client.get('/api/applications/get/', {'game_alias': foreign.game.alias, 'user_id': foreign.user_id}).status_code == 400
            checked_owners += 1
        with transaction.atomic():
            code = issue_link(local_users[0])
            consume_link(code, 999999999991, 'synthetic_preview')
            try:
                consume_link(code, 999999999992, 'synthetic_preview')
                raise AssertionError('Replay succeeded')
            except ValueError:
                pass
            transaction.set_rollback(True)
        client.force_authenticate(None)
        cache.clear()
        login = client.post('/api/token/login/', {'login_field': local_users[0].username,
                                                 'password': 'local-preview-only-change-me'})
        assert login.status_code == 200
        client.credentials(HTTP_AUTHORIZATION='Token ' + login.data['auth_token'])
        assert client.get('/api/users/me/').data['id'] == local_users[0].pk
        assert client.post('/api/token/logout/').status_code == 204
        assert client.get('/api/users/me/').status_code == 401
        self.stdout.write(json.dumps({'restored_counts': counts, 'visible_roles': role_counts,
                                     'owners_checked': checked_owners, 'security_checks': 'passed'}))
