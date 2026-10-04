from django.db import migrations, models
from django.db.models.functions import Lower


class Migration(migrations.Migration):
    dependencies = [('games', '0009_alter_character_liked_by')]
    operations = [migrations.AddConstraint(
        model_name='game',
        constraint=models.UniqueConstraint(Lower('alias'), name='game_alias_unique_ci'),
    )]
