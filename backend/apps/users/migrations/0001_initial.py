# Generated by Django 4.2.6 on 2023-10-24 11:11

import apps.users.models.merchant
import apps.users.models.user
from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import django_ltree.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='updated at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email')),
                ('first_name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='name')),
                ('last_name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='surname')),
                ('username', models.CharField(max_length=15, unique=True, verbose_name='username')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='tgavatars/pictures/', verbose_name='picture')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, protocol='IPv4', verbose_name='Client IP address')),
                ('country', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Country')),
                ('country_iso', models.CharField(blank=True, default=None, max_length=5, null=True, verbose_name='Country ISO code')),
                ('city', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='City')),
                ('lat', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Latitude')),
                ('long', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Longitude')),
                ('staking_active', models.BooleanField(default=True)),
                ('location_frozen', models.BooleanField(default=False)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, default=None, max_length=128, null=True, region=None)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='admin')),
                ('email_active', models.BooleanField(default=False)),
                ('instagram', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='instagram')),
                ('locale', models.CharField(choices=[('ru', 'Russian'), ('en', 'English'), ('it', 'Italian'), ('ro', 'Romanian'), ('hu', 'Hungarian'), ('de', 'German'), ('uk', 'Ukrainian'), ('fr', 'French'), ('si', 'Slovenian'), ('es', 'Spanish'), ('tr', 'Turkish'), ('pt', 'Portuguese'), ('cs', 'Czech')], default='en', max_length=2, verbose_name='locale')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', apps.users.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Matrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='updated at')),
                ('path', django_ltree.fields.PathField(blank=True, null=True)),
                ('lvl', models.SmallIntegerField(blank=True, default=0)),
                ('gl', models.BooleanField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name': 'Матричный пользователь',
                'verbose_name_plural': 'Матричные пользователи',
            },
        ),
        migrations.CreateModel(
            name='MatrixRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('refer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matrix_request_referals', to='users.matrix', verbose_name='refer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matrix_request_refers', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Заявка в матрицу',
                'verbose_name_plural': 'Заявки в матрицу',
            },
        ),
        migrations.AddField(
            model_name='matrix',
            name='matrix_request',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='clone', to='users.matrixrequest', verbose_name='request'),
        ),
        migrations.AddField(
            model_name='matrix',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matrix_clones', to='users.matrix', verbose_name='clone'),
        ),
        migrations.AddField(
            model_name='matrix',
            name='refer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matrix_referals', to='users.matrix', verbose_name='refer'),
        ),
        migrations.AddField(
            model_name='matrix',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matrix_refers', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.CreateModel(
            name='Linear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='updated at')),
                ('path', django_ltree.fields.PathField(blank=True, null=True)),
                ('refer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='linear_referals', to=settings.AUTH_USER_MODEL, verbose_name='refer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='linear_refer', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'linear tree',
                'verbose_name_plural': 'linear tree users',
            },
        ),
        migrations.CreateModel(
            name='ActionRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='updated at')),
                ('otp', models.CharField(blank=True, max_length=6)),
                ('expired_at', models.DateTimeField(verbose_name='expired at')),
                ('key', models.CharField(default='', max_length=30, verbose_name='key')),
                ('data', models.JSONField(blank=True, default=dict)),
                ('confirmed', models.BooleanField(blank=True, default=False)),
                ('is_used', models.BooleanField(blank=True, default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='updated at')),
                ('num', models.IntegerField(choices=[(0, 'START'), (10, 'PARTNER'), (20, 'BOSS'), (30, 'OLIGARCH')], default=0, verbose_name='num')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='qualification', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'abstract': False,
                'indexes': [django.contrib.postgres.indexes.BrinIndex(fields=['created_at'], name='users_quali_created_f330b6_brin')],
            },
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='updated at')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('promo_link', models.CharField(default=apps.users.models.merchant.gen_api_token, editable=False, max_length=20, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email')),
                ('first_name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='name')),
                ('last_name', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='surname')),
                ('country', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Country')),
                ('country_iso', models.CharField(blank=True, default=None, max_length=5, null=True, verbose_name='Country ISO code')),
                ('city', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='City')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, default=None, max_length=128, null=True, region=None)),
                ('address', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='address')),
                ('company', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='company')),
                ('website', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='website')),
                ('instagram', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='instagram')),
                ('telegram', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='telegram')),
                ('twitter', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='twitter')),
                ('facebook', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='facebook')),
                ('youtube', models.CharField(blank=True, default=None, max_length=250, null=True, verbose_name='youtube')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='merchants', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'abstract': False,
                'indexes': [django.contrib.postgres.indexes.BrinIndex(fields=['created_at'], name='users_merch_created_189b4a_brin')],
            },
        ),
        migrations.AddIndex(
            model_name='matrixrequest',
            index=models.Index(fields=['refer_id'], name='users_matri_refer_i_7df19b_idx'),
        ),
        migrations.AddIndex(
            model_name='matrixrequest',
            index=models.Index(fields=['user_id'], name='users_matri_user_id_8bd098_idx'),
        ),
        migrations.AddIndex(
            model_name='matrix',
            index=models.Index(fields=['id'], name='users_matri_id_b1db84_idx'),
        ),
        migrations.AddIndex(
            model_name='matrix',
            index=models.Index(fields=['uuid'], name='users_matri_uuid_a25fe6_idx'),
        ),
        migrations.AddIndex(
            model_name='matrix',
            index=models.Index(fields=['refer_id'], name='users_matri_refer_i_0a5a15_idx'),
        ),
        migrations.AddIndex(
            model_name='matrix',
            index=models.Index(fields=['user_id'], name='users_matri_user_id_4480db_idx'),
        ),
        migrations.AddIndex(
            model_name='matrix',
            index=models.Index(fields=['lvl'], name='users_matri_lvl_a3032b_idx'),
        ),
        migrations.AddIndex(
            model_name='matrix',
            index=django.contrib.postgres.indexes.GistIndex(fields=['path'], name='users_matri_path_f2fe45_gist'),
        ),
        migrations.AddIndex(
            model_name='linear',
            index=models.Index(fields=['refer_id'], name='users_linea_refer_i_6fd945_idx'),
        ),
        migrations.AddIndex(
            model_name='linear',
            index=django.contrib.postgres.indexes.GistIndex(fields=['path'], name='users_linea_path_5540d9_gist'),
        ),
        migrations.AddIndex(
            model_name='actionrequest',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['created_at'], name='users_actio_created_d659d8_brin'),
        ),
    ]