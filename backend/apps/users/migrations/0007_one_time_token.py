import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('users', '0006_telegram_link_token')]

    operations = [
        migrations.RenameModel(old_name='TelegramLinkToken', new_name='OneTimeToken'),
        migrations.AlterField(
            model_name='onetimetoken', name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='onetimetoken', name='action',
            field=models.CharField(max_length=32, choices=[('telegram_link', 'Link Telegram'), ('password_change', 'Change password')], default='telegram_link'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='onetimetoken',
            constraint=models.UniqueConstraint(fields=('user', 'action'), name='unique_user_token_action'),
        ),
    ]
