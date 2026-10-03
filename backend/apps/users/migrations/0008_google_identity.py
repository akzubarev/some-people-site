"""Case-insensitive account email uniqueness and Google identities."""
from django.conf import settings
from django.db import migrations, models
from django.db.models.functions import Lower
import django.db.models.deletion


def check_email_collisions(apps, schema_editor):
    User = apps.get_model('users', 'User')
    duplicates = (User.objects.using(schema_editor.connection.alias).annotate(normalized=Lower('email'))
                  .values('normalized').annotate(count=models.Count('pk')).filter(count__gt=1))
    if duplicates.exists():
        raise RuntimeError('Resolve case-insensitive duplicate account emails before applying this migration.')


class Migration(migrations.Migration):
    dependencies = [('users', '0007_one_time_token')]
    operations = [
        migrations.RunPython(check_email_collisions, migrations.RunPython.noop),
        migrations.AddConstraint(model_name='user', constraint=models.UniqueConstraint(Lower('email'), name='unique_user_email_ci')),
        migrations.CreateModel(name='GoogleIdentity', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('subject', models.CharField(max_length=255, unique=True)),
            ('email', models.EmailField(max_length=255)),
            ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='google_identity', to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name='GoogleChallenge', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('digest', models.CharField(max_length=64, unique=True)),
            ('browser_digest', models.CharField(max_length=64)),
            ('purpose', models.CharField(choices=[('signin', 'Sign in'), ('link', 'Link')], max_length=8)),
            ('expires_at', models.DateTimeField()),
            ('consumed_at', models.DateTimeField(null=True)),
            ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        ]),
    ]
