"""Short-lived public payloads, invalidated per game after committed writes."""
from hashlib import sha256
from uuid import uuid4

from django.conf import settings
from django.core.cache import cache
from django.db import connections, transaction
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver

from apps.games.models import Application, Character, Game, Group, Tag
from apps.users.models import User

TTL = 60
PREFIX = 'public-games:v1'
PUBLIC_USER_FIELDS = {
    'username', 'first_name', 'last_name', 'avatar', 'vk', 'telegram_username',
    'vk_public', 'tg_public',
}


def cached_payload(scope, variant, build):
    # Never publish uncommitted data to a cache shared by other requests.
    if connections['default'].in_atomic_block:
        return build()
    version = cache.get_or_set(f'{PREFIX}:version:{scope}', lambda: uuid4().hex, timeout=None)
    digest = sha256(variant.encode()).hexdigest()
    key = f'{PREFIX}:{scope}:{version}:{digest}'
    value = cache.get(key)
    if value is None:
        value = build()
        # Leave time to load images even with the shortest supported S3 URL lifetime.
        signed_url_ttl = settings.STORAGES['default'].get('OPTIONS', {}).get('querystring_expire', TTL * 2)
        cache.set(key, value, min(TTL, max(1, signed_url_ttl // 2)))
    return value


def invalidate_games(game_ids, using='default'):
    """Bulk import/update callers must invoke this too: QuerySet.update skips signals."""
    scopes = {str(pk) for pk in game_ids if pk is not None}
    if not scopes:
        return
    scopes.add('index')

    def invalidate():
        # A request building an old version cannot repopulate the new namespace.
        cache.set_many({f'{PREFIX}:version:{scope}': uuid4().hex for scope in scopes}, timeout=None)

    transaction.on_commit(invalidate, using=using)


def character_games(characters):
    return {pk for pair in characters.values_list('group__game_id', 'family__game_id')
            for pk in pair if pk is not None}


def affected_games(instance):
    if isinstance(instance, Game):
        return {instance.pk} if instance.pk else set()
    if isinstance(instance, Group):
        related = character_games(Character.objects.filter(group=instance) | Character.objects.filter(family=instance)) if instance.pk else set()
        children = set(instance.subgroups.values_list('game_id', flat=True)) if instance.pk else set()
        return {instance.game_id} | related | children
    if isinstance(instance, Character):
        return set(Group.objects.filter(pk__in=[instance.group_id, instance.family_id])
                   .values_list('game_id', flat=True))
    if isinstance(instance, Tag):
        return character_games(instance.characters.all()) if instance.pk else set()
    if isinstance(instance, Application):
        return {instance.game_id} | character_games(Character.objects.filter(pk=instance.character_id))
    if isinstance(instance, User) and instance.pk:
        return character_games(Character.objects.filter(application__user=instance))
    return set()


WATCHED = (Game, Group, Character, Tag, Application, User)


@receiver(pre_save)
def remember_previous_games(sender, instance, raw=False, update_fields=None, **kwargs):
    if sender not in WATCHED or raw:
        return
    previous = sender.objects.filter(pk=instance.pk).first() if instance.pk else None
    skip = isinstance(instance, User) and (
        update_fields is not None and not PUBLIC_USER_FIELDS.intersection(update_fields)
        or previous is not None and all(getattr(previous, field) == getattr(instance, field)
                                        for field in PUBLIC_USER_FIELDS)
    )
    instance._skip_public_cache = skip
    instance._previous_public_games = affected_games(previous) if previous and not skip else set()


@receiver(post_save)
def invalidate_saved(sender, instance, raw=False, using='default', **kwargs):
    if sender in WATCHED and not raw and not getattr(instance, '_skip_public_cache', False):
        invalidate_games(affected_games(instance) | getattr(instance, '_previous_public_games', set()), using)


@receiver(pre_delete)
def remember_deleted_games(sender, instance, **kwargs):
    if sender in WATCHED:
        instance._previous_public_games = affected_games(instance)


@receiver(post_delete)
def invalidate_deleted(sender, instance, using='default', **kwargs):
    if sender in WATCHED:
        invalidate_games(getattr(instance, '_previous_public_games', set()), using)


@receiver(m2m_changed, sender=Character.tags.through)
def invalidate_tag_membership(instance, action, using='default', **kwargs):
    if action.startswith('pre_'):
        instance._previous_tag_games = affected_games(instance)
    elif action.startswith('post_'):
        invalidate_games(affected_games(instance) | getattr(instance, '_previous_tag_games', set()), using)
