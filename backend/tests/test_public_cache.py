"""Public cache behavior with real transaction commits and synthetic records."""
from unittest.mock import patch
from django.core.cache import cache
from django.db import transaction
from django.test import TransactionTestCase, override_settings
from rest_framework.test import APIClient

from apps.games.models import Application, Character, Game, Group, Tag
from apps.games.public_cache import cached_payload, invalidate_games
from apps.games.serializers import GroupSerializer
from apps.users.models import User


class PublicCacheTests(TransactionTestCase):
    def setUp(self):
        cache.clear()
        self.game = Game.objects.create(title='Cache game', alias='cache', open_character_list=True)
        self.group = Group.objects.create(name='Visible', game=self.game)
        self.character = Character.objects.create(name='Engineer', alias='engineer', group=self.group)
        self.user = User.objects.create_user('cache-player', 'cache@example.invalid', 'password', vk='visible-vk')
        self.application = Application.objects.create(user=self.user, game=self.game,
            character=self.character, status=Application.Status.CONFIRMED)
        self.client = APIClient()

    def get(self, action='groups', alias='cache', **params):
        response = self.client.get(f'/api/games/{action}/', {'game_alias': alias, **params})
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response['Cache-Control'], 'no-store')
        return response.data

    def test_hit_skips_serialization_and_does_not_share_private_fields(self):
        data = self.get()
        with patch.object(GroupSerializer, 'to_representation', side_effect=AssertionError('cache miss')):
            self.assertEqual(self.get(), data)
        player = data[0]['characters'][0]['player']
        self.assertEqual(player['vk'], 'visible-vk')
        self.assertNotIn('phone', player)
        self.assertNotIn('email', player)

    def test_hiding_parent_invalidates_groups_characters_tags_and_counts(self):
        child = Group.objects.create(name='Child', game=self.game, parent=self.group)
        self.character.group = child
        self.character.save()
        tag = Tag.objects.create(name='Tag', color='red')
        self.character.tags.add(tag)
        for action in ('groups', 'characters', 'tags'):
            self.assertTrue(self.get(action))
        self.assertEqual(self.client.get('/api/games/').data[0]['player_count'], 1)
        self.group.hidden = True
        self.group.save()
        for action in ('groups', 'characters', 'tags'):
            self.assertEqual(self.get(action), [])
        self.assertEqual(self.client.get('/api/games/').data[0]['player_count'], 0)

    def test_publication_checked_before_staff_warmed_payload(self):
        self.game.open_character_list = False
        self.game.save()
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(self.user)
        self.assertTrue(self.get())
        self.client.force_authenticate(None)
        for action in ('groups', 'characters', 'tags'):
            self.assertEqual(self.client.get(f'/api/games/{action}/', {'game_alias': 'cache'}).status_code, 404)

    def test_consent_profile_assignment_and_deletion_invalidate_players(self):
        self.assertEqual(self.get()[0]['characters'][0]['player']['vk'], 'visible-vk')
        self.user.vk_public = False
        self.user.username = 'changed'
        self.user.save()
        player = self.get()[0]['characters'][0]['player']
        self.assertIsNone(player['vk'])
        self.assertEqual(player['username'], 'changed')
        self.application.status = Application.Status.PENDING
        self.application.save()
        self.assertIsNone(self.get()[0]['characters'][0]['player'])
        self.application.status = Application.Status.CONFIRMED
        self.application.save()
        self.assertIsNotNone(self.get()[0]['characters'][0]['player'])
        self.user.delete()
        self.assertIsNone(self.get()[0]['characters'][0]['player'])

    def test_tag_add_remove_reverse_clear_and_rename(self):
        tag = Tag.objects.create(name='Old', color='red')
        self.assertEqual(self.get('tags'), [])
        self.character.tags.add(tag)
        self.assertEqual(self.get('tags')[0]['name'], 'Old')
        tag.name = 'New'
        tag.save()
        self.assertEqual(self.get('tags')[0]['name'], 'New')
        tag.characters.clear()
        self.assertEqual(self.get('tags'), [])
        tag.characters.add(self.character)
        self.assertEqual(self.get('characters')[0]['tags'][0]['name'], 'New')
        self.character.tags.remove(tag)
        self.assertEqual(self.get('characters')[0]['tags'], [])

    def test_filters_and_games_are_separate(self):
        self.assertEqual(self.get('characters', search='missing'), [])
        self.assertEqual(len(self.get('characters', search='Engineer')), 1)
        self.assertEqual(self.get('characters', tag='absent'), [])
        other = Game.objects.create(title='Other', alias='other', open_character_list=True)
        Group.objects.create(name='Other group', game=other)
        self.get(alias='other')
        self.group.name = 'Changed'
        self.group.save()
        with patch.object(GroupSerializer, 'to_representation', side_effect=AssertionError('unrelated eviction')):
            self.assertEqual(self.get(alias='other')[0]['name'], 'Other group')
        self.assertEqual(self.get()[0]['name'], 'Changed')

    def test_moving_group_invalidates_old_and_new_games(self):
        other = Game.objects.create(title='Other', alias='other', open_character_list=True)
        self.get()
        self.get(alias='other')
        self.group.game = other
        self.group.save()
        self.assertEqual(self.get(), [])
        self.assertEqual(self.get(alias='other')[0]['name'], 'Visible')

    def test_rollback_preserves_cache_and_never_publishes_uncommitted_data(self):
        self.get()
        with self.assertRaises(ValueError):
            with transaction.atomic():
                self.group.name = 'Uncommitted'
                self.group.save()
                self.assertEqual(self.get()[0]['name'], 'Uncommitted')
                raise ValueError('rollback')
        with patch.object(GroupSerializer, 'to_representation', side_effect=AssertionError('rollback evicted cache')):
            self.assertEqual(self.get()[0]['name'], 'Visible')
        with transaction.atomic():
            self.group.name = 'Committed'
            self.group.save()
        self.assertEqual(self.get()[0]['name'], 'Committed')

    def test_old_builder_cannot_repopulate_invalidated_version(self):
        def build_old():
            invalidate_games({self.game.pk})
            return ['old']
        cached_payload(self.game.pk, 'race', build_old)
        self.assertEqual(cached_payload(self.game.pk, 'race', lambda: ['new']), ['new'])

    def test_private_activity_does_not_flush_public_cache(self):
        self.get()
        self.user.set_password('different-password')
        self.user.save(update_fields=['password'])
        self.character.liked_by.add(self.user)
        with patch.object(GroupSerializer, 'to_representation', side_effect=AssertionError('unrelated eviction')):
            self.get()

    @override_settings(STORAGES={'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage',
                                            'OPTIONS': {'querystring_expire': 60}}})
    def test_payload_expires_before_short_lived_signed_images(self):
        with patch.object(cache, 'set', wraps=cache.set) as write:
            cached_payload(self.game.pk, 'short-url', lambda: ['image'])
        self.assertEqual(write.call_args.args[2], 30)

    def test_browsing_does_not_consume_login_quota(self):
        for _ in range(65):
            self.get()
            self.assertEqual(self.client.get('/api/session/').status_code, 200)
        response = self.client.post('/api/session/', {'login_field': 'cache-player', 'password': 'wrong'})
        self.assertEqual(response.status_code, 400)
