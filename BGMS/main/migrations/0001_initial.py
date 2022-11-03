# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
import tenant_schemas.postgresql_backend.base
import django.utils.timezone
import main.models
import uuid
import main.validators
import django.core.validators
from django.conf import settings
from django.core.management import call_command


def populate_reserve_plot_states(apps, schema_editor):
    ReservePlotState = apps.get_model("main", "ReservePlotState")
    if connection.schema_name == 'public':
        ReservePlotState.objects.create(state='reserved')
        ReservePlotState.objects.create(state='deleted')
        ReservePlotState.objects.create(state='buried')


def create_image_state(apps, schema_editor):
    ImageState = apps.get_model("main", "ImageState")
    if connection.schema_name == 'public':
        ImageState.objects.update_or_create(image_state="unprocessed")
        ImageState.objects.update_or_create(image_state="processing")
        ImageState.objects.update_or_create(image_state="processed")


def pupulate_image_type(apps, schema_editor):
    if connection.schema_name == 'public':
        call_command('loaddata', 'imagetype.json')

def populate_main_burialgroundsite(apps, schema_editor):
    BurialGroundSite = apps.get_model("main", "BurialGroundSite")
    if connection.schema_name == 'public':
        BurialGroundSite(domain_url='127.0.0.1', schema_name='public', name='Public').save()



class Migration(migrations.Migration):

    dependencies = [
        # ('auth', '0006_require_contenttypes_0002'),
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BGUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, null=True, verbose_name='username', unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], error_messages={'unique': 'User with this username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(verbose_name='first name', blank=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', blank=True, max_length=30)),
                ('email', models.EmailField(unique=True, error_messages={'unique': 'User with this email already exists.'}, help_text='Required.', max_length=254, verbose_name='email address')),
                ('_is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(to='auth.Group', blank=True, related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_query_name='user', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', main.models.BGUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('first_line', models.CharField(max_length=100)),
                ('town', models.CharField(null=True, max_length=50)),
                ('county', models.CharField(null=True, max_length=50)),
                ('postcode', models.CharField(null=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='BurialGroundSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('domain_url', models.CharField(unique=True, max_length=128)),
                ('schema_name', models.CharField(unique=True, max_length=63, validators=[tenant_schemas.postgresql_backend.base._check_schema_name])),
                ('name', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Date the site is added')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BurialOfficialType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, db_index=True, editable=False, primary_key=True, serialize=False)),
                ('official_type', models.CharField(max_length=50, validators=[main.validators.bleach_validator])),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(null=True, max_length=35, blank=True, validators=[main.validators.bleach_validator])),
                ('description', models.CharField(null=True, max_length=35, blank=True, validators=[main.validators.bleach_validator])),
            ],
        ),
        migrations.CreateModel(
            name='FeatureCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('feature_type', models.CharField(db_index=True, max_length=20, validators=[main.validators.bleach_validator])),
                ('type', models.CharField(max_length=20, validators=[main.validators.bleach_validator])),
                ('display_name', models.CharField(max_length=20, validators=[main.validators.bleach_validator])),
                ('min_resolution', models.FloatField()),
                ('max_resolution', models.FloatField()),
                ('show_in_toolbar', models.BooleanField()),
                ('hierarchy', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FeatureGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('group_code', models.CharField(max_length=20, validators=[main.validators.bleach_validator])),
                ('display_name', models.CharField(max_length=20, validators=[main.validators.bleach_validator])),
                ('switch_on_off', models.BooleanField(default=True)),
                ('initial_visibility', models.BooleanField(default=False)),
                ('hierarchy', models.IntegerField()),
                ('feature_codes', models.ManyToManyField(to='main.FeatureCode')),
            ],
        ),
        migrations.CreateModel(
            name='ImageState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('image_state', models.CharField(unique=True, max_length=15, validators=[main.validators.bleach_validator])),
            ],
        ),
        migrations.CreateModel(
            name='ImageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('image_type', models.CharField(unique=True, max_length=20, validators=[main.validators.bleach_validator])),
            ],
        ),
        migrations.CreateModel(
            name='Nicknames',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nickname', models.CharField(max_length=20, validators=[main.validators.bleach_validator])),
                ('actual_name', models.CharField(max_length=30, validators=[main.validators.bleach_validator])),
            ],
        ),
        migrations.CreateModel(
            name='Parish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('parish', models.CharField(null=True, max_length=50, blank=True, validators=[main.validators.bleach_validator])),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('isMailVerified', models.BooleanField(default=False)),
                ('activation_key', models.CharField(max_length=40, blank=True)),
                ('key_expires', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('religion', models.CharField(null=True, max_length=50, blank=True, validators=[main.validators.bleach_validator])),
            ],
        ),
        migrations.CreateModel(
            name='ReservePlotState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('state', models.CharField(unique=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SiteDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('url', models.CharField(null=True, max_length=300)),
                ('layer', models.CharField(max_length=20, null=True, help_text='WMTS Layer name / Schema name', verbose_name='Schema name')),
                ('matrixSet', models.CharField(null=True, max_length=20)),
                ('extent', models.CharField(null=True, help_text='Extend for the tile grid', max_length=300)),
                ('aerial', models.BooleanField(default=True, verbose_name='Aerial?')),
                ('address', models.ForeignKey(null=True, to='main.Address', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'Site Details',
            },
        ),
        migrations.CreateModel(
            name='SiteGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('burialgroundsite', models.ForeignKey(to='main.BurialGroundSite', on_delete=models.CASCADE)),
                ('group', models.ForeignKey(to='auth.Group', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Surveyor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('surveyor_name', models.CharField(max_length=100, validators=[main.validators.bleach_validator])),
            ],
        ),
        migrations.AddField(
            model_name='burialgroundsite',
            name='site_details',
            field=models.OneToOneField(null=True, to='main.SiteDetails', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='bguser',
            name='site_groups',
            field=models.ManyToManyField(to='main.SiteGroup', blank=True),
        ),
        migrations.AddField(
            model_name='bguser',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', blank=True, related_name='user_set', help_text='Specific permissions for this user.', related_query_name='user', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='DataEntryUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('main.bguser',),
            managers=[
                ('objects', main.models.BGUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DataMatchingUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('main.bguser',),
            managers=[
                ('objects', main.models.BGUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SiteGroupSite',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('main.sitegroup',),
        ),
        migrations.CreateModel(
            name='TenantUser',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name': 'Site User',
                'verbose_name_plural': 'Site Users',
            },
            bases=('main.bguser',),
        ),
        migrations.RunPython(
            code=populate_reserve_plot_states,
        ),
        migrations.RunPython(
            code=create_image_state,
        ),
        migrations.RunPython(
            code=pupulate_image_type,
        ),
        migrations.RunPython(
            code=populate_main_burialgroundsite,
        ),
    ]
