"""Only called by the disposable browser-test Compose stack."""
from django.conf import settings
from apps.games.models import Game, Group, Character, Question

if settings.SETTINGS_MODULE != 'config.frontend_test_settings':
    raise RuntimeError('Synthetic browser fixtures require frontend_test_settings.')

for alias, title in [('whales', 'Киты'), ('frostpunk', 'Frostpunk')]:
    game, _ = Game.objects.get_or_create(alias=alias, defaults={
        'title': title, 'open_applications': True, 'open_character_list': True,
        'short_description': 'Какие-то люди делают игры', 'location': 'Тестовый полигон',
    })
    group, _ = Group.objects.get_or_create(game=game, name='Администрация')
    Character.objects.get_or_create(group=group, alias='engineer', defaults={
        'name': 'Инженер', 'description': 'История персонажа',
    })
    hidden, _ = Group.objects.get_or_create(game=game, name='Hidden group', defaults={'hidden': True})
    Character.objects.get_or_create(group=hidden, alias='hidden', defaults={'name': 'Hidden character'})
    for order, kind in enumerate(['line', 'paragraph', 'single_choice', 'multiple_choice',
                                   'scale', 'matrix', 'matrix_checkbox'], 1):
        question, _ = Question.objects.get_or_create(title=alias + ' ' + kind, defaults={
            'type': kind, 'order': order,
            'choices': [['A', 'B'], ['One', 'Two']] if kind.startswith('matrix') else ['A', 'B'],
        })
        question.games.add(game)
