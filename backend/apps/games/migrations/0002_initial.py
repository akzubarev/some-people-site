# Generated by Django 5.1.1 on 2024-11-10 13:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('games', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL, verbose_name='Игрок'),
        ),
        migrations.AddField(
            model_name='answer',
            name='application',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='games.application', verbose_name='Заявка'),
        ),
        migrations.AddField(
            model_name='character',
            name='master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='characters', to=settings.AUTH_USER_MODEL, verbose_name='Мастер'),
        ),
        migrations.AddField(
            model_name='application',
            name='character',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='applications', to='games.character', verbose_name='Персонаж'),
        ),
        migrations.AddField(
            model_name='application',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='games.game', verbose_name='Игра'),
        ),
        migrations.AddField(
            model_name='group',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='games.game', verbose_name='Игра'),
        ),
        migrations.AddField(
            model_name='group',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subgroups', to='games.group', verbose_name='Родительская фракция'),
        ),
        migrations.AddField(
            model_name='character',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='characters', to='games.group', verbose_name='Фракция'),
        ),
        migrations.AddField(
            model_name='question',
            name='games',
            field=models.ManyToManyField(related_name='questions', to='games.game', verbose_name='Игра'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='games.question', verbose_name='Вопрос'),
        ),
        migrations.AddField(
            model_name='character',
            name='tags',
            field=models.ManyToManyField(related_name='characters', to='games.tag', verbose_name='Тэги'),
        ),
    ]
