# Generated by Django 5.1.1 on 2024-12-07 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_character_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='name_eng',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя (Англ)'),
        ),
    ]
