from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('notifications', '0003_mailing'), ('games', '0010_game_alias_unique')]
    operations = [
        migrations.AddField('notification', 'attempts', models.PositiveIntegerField(default=0)),
        migrations.AddField('notification', 'last_attempt_at', models.DateTimeField(blank=True, null=True)),
        migrations.AddField('notification', 'last_error', models.CharField(blank=True, default='', max_length=80)),
        migrations.AddField('mailing', 'game', models.ForeignKey(blank=True, null=True,
            on_delete=django.db.models.deletion.PROTECT, related_name='mailings', to='games.game')),
        migrations.AddField('mailing', 'applications', models.ManyToManyField(blank=True,
            related_name='mailings', to='games.application')),
        migrations.AddField('mailing', 'confirmed_at', models.DateTimeField(blank=True, null=True)),
        migrations.AddField('mailing', 'confirmation_key', models.UUIDField(blank=True, null=True, unique=True)),
    ]
