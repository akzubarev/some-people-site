# Generated by Django 5.0 on 2023-12-25 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0013_alter_character_options_alter_faction_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='faction',
            name='alias',
            field=models.CharField(default='admin', max_length=100, verbose_name='Алиас'),
            preserve_default=False,
        ),
    ]