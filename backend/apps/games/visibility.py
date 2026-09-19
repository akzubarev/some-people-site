"""Public role visibility, including hidden ancestors and family membership."""
from django.db.models import Q

from .models import Character, Group


def visible_group_ids(game_id):
    rows = list(Group.objects.filter(game_id=game_id).values('id', 'parent_id', 'hidden'))
    children = {}
    for row in rows:
        children.setdefault(row['parent_id'], []).append(row)
    visible = set()
    pending = list(children.get(None, []))
    while pending:
        row = pending.pop()
        if row['hidden'] or row['id'] in visible:
            continue
        visible.add(row['id'])
        pending.extend(children.get(row['id'], []))
    # Broken cross-game parents and cycles are excluded rather than exposed.
    return visible


def public_characters(game_id, group_ids=None):
    ids = visible_group_ids(game_id) if group_ids is None else group_ids
    return Character.objects.filter(group_id__in=ids).filter(
        Q(family__isnull=True) | Q(family_id__in=ids)
    )
