# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
import django.utils.timezone
import django.core.validators
import main.validators
import main.models
import datetime
from django.conf import settings
import tenant_schemas.postgresql_backend.base
import uuid


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# main.migrations.0035_auto_20170129_1318
# ***Old function, no need anymore due is to migrate data when spliting geometries into new django-ag-geometries package***
# from django.db import migrations, connection

# def migrate_featuregroups_featurecodes(apps, schema_editor):
#     FeatureCode = apps.get_model("main", "FeatureCode")
#     FeatureGroup = apps.get_model("main", "FeatureGroup")
#     gFeatureCode = apps.get_model("geometriespublic", "FeatureCode")
#     gFeatureGroup = apps.get_model("geometriespublic", "FeatureGroup")

#     if connection.schema_name == 'public':
#         for fc in FeatureCode.objects.all():
#             gFeatureCode.objects.create(id=fc.id, feature_type=fc.feature_type, type=fc.type, display_name=fc.display_name, min_resolution=fc.min_resolution, max_resolution=fc.max_resolution, show_in_toolbar=fc.show_in_toolbar, hierarchy=fc.hierarchy)

# main.migrations.0037_auto_20170129_1714
# ***Old function, no need anymore due is to migrate data when spliting geometries into new django-ag-geometries package***
# main.migrations.0022_auto_20160712_1427
#TODO: include this new load data for populating the burialofficial type.
from django.core.management import call_command

def pupulate_featurecode_featuregroup(apps, schema_editor):
    call_command('loaddata', 'burialofficialtype.json')

# main.migrations.0031_auto_20160920_1434
# ***Old function, no need anymore due is to migrate data when spliting geometries into new django-ag-geometries package***
# main.migrations.0018_auto_20160622_1007
# ***Old function, no need anymore due is to migrate data when spliting geometries into new django-ag-geometries package***
# main.migrations.0036_auto_20170129_1334
# ***Old function, no need anymore due is to migrate data when spliting geometries into new django-ag-geometries package***
# main.migrations.0006_auto_20150902_1027
# main.migrations.0015_auto_20160601_1500
# ***Old function, no need anymore due is to migrate data when spliting geometries into new django-ag-geometries package***
# FeatureGroup = apps.get_model("main", "FeatureGroup")
# if connection.schema_name == 'public':
#     basefc = FeatureGroup.objects.get(group_code="base")
#     if basefc:
#         basefc.display_name = 'Map'
#         basefc.save()
#     basefc = FeatureGroup.objects.get(group_code="aerial")
#     if basefc:
#         basefc.display_name = 'Aerial'
#         basefc.save()
# main.migrations.0002_auto_20150826_1450
# ***Old function, moved to geometries public in django-ag-geometries package refactored***
# def create_feature_code(apps, schema_editor):
#     NewFeatureCode = apps.get_model("main", "FeatureCode")
#     if connection.schema_name == 'public':
#         if not NewFeatureCode.objects.all().exists():
#             feature_names = [{'type':'war_grave', 'display_string':'War Grave'}, 
#                              {'type':'war_memorial', 'display_string':'War Memorial'}, 
#                              {'type':'pavestone', 'display_string':'Pavestone'}, 
#                              {'type':'plaque', 'display_string':'Plaque'},
#                              {'type':'statue', 'display_string':'Statue'}, 
#                              {'type':'table_tomb', 'display_string':'Table Tomb'}, 
#                              {'type':'window', 'display_string':'Window'}, 
#                              {'type':'gravestone', 'display_string':'Gravestone'}, 
#                              {'type':'plot', 'display_string':'Plot'}, 
#                              {'type':'bound_plot', 'display_string':'Bound Plot'}, 
#                              {'type':'tree', 'display_string':'Tree'}, 
#                              {'type':'bush', 'display_string':'Bush/Shrub'}, 
#                              {'type':'tree_canopy', 'display_string':'Tree Canopy'}, 
#                              {'type':'manhole', 'display_string':'Manhole'}, 
#                              {'type':'gully', 'display_string':'Gully'}, 
#                              {'type':'inspection_cover', 'display_string':'Inspection Cover'}, 
#                              {'type':'utility_pole', 'display_string':'Utility Pole'}, 
#                              {'type':'wall', 'display_string':'Wall'}, 
#                              {'type':'hedge', 'display_string':'Hedge'}, 
#                              {'type':'fence', 'display_string':'Fence'}, 
#                              {'type':'gate', 'display_string':'Gate'}, 
#                              {'type':'path', 'display_string':'Path'}, 
#                              {'type':'bridge', 'display_string':'Bridge'}, 
#                              {'type':'road', 'display_string':'Road'}, 
#                              {'type':'car_park', 'display_string':'Car Park'}, 
#                              {'type':'grass', 'display_string':'Grass'}, 
#                              {'type':'water', 'display_string':'Water'}, 
#                              {'type':'recreation', 'display_string':'Recreation'}, 
#                              {'type':'planting', 'display_string':'Planting'}, 
#                              {'type':'woodland', 'display_string':'Woodland'}, 
#                              {'type':'building', 'display_string':'Building'}, 
#                              {'type':'steps', 'display_string':'Steps'}, 
#                              {'type':'tank', 'display_string':'Tank'}, 
#                              {'type':'mausoleum', 'display_string':'Mausoleum'}, 
#                              {'type':'bench', 'display_string':'Bench'}, 
#                              {'type':'sign', 'display_string':'Sign'}, 
#                              {'type':'bollard', 'display_string':'Bollard'},
#                              {'type':'bin', 'display_string':'Bin'}, 
#                              {'type':'lamppost', 'display_string':'Lamppost'}, 
#                              {'type':'diocese', 'display_string':'Diocese'}, 
#                              {'type':'archdeaconry', 'display_string':'Archdeaconry'}, 
#                              {'type':'deanery', 'display_string':'Deanery'}, 
#                              {'type':'parish', 'display_string':'Parish'}, 
#                              {'type':'ward', 'display_string':'Ward'}, 
#                              {'type':'section', 'display_string':'Section'}]
#             for name in feature_names:
#                 NewFeatureCode.objects.create(feature_type=name['type'], display_name=name['display_string'])

# main.migrations.0007_auto_20151203_1404
# main.migrations.0001_squashed_0034_auto_20150805_1425
# main.migrations.0017_auto_20160609_1433
# ***Old function, no need anymore due is to migrate data when spliting geometries into new django-ag-geometries package***
# main.migrations.0021_auto_20160715_0910
# ***Old function, no need anymore due is to migrate data when spliting geometries into new django-ag-geometries package***
# main.migrations.0021_auto_20160712_1139
# main.migrations.0033_auto_20161006_1000
# ***Old function, no need anymore due is to migrate data when spliting geometries into new django-ag-geometries package***
# main.migrations.0013_auto_20160422_1210
#TODO: needs to be included in the reset migration
def create_image_state(apps, schema_editor):
    ImageState = apps.get_model("main", "ImageState")
    if connection.schema_name == 'public':
        ImageState.objects.update_or_create(image_state="unprocessed")
        ImageState.objects.update_or_create(image_state="processing")
        ImageState.objects.update_or_create(image_state="processed")

# main.migrations.0028_auto_20160809_0830
#TODO: need to be included in the reset migration
def populate_reserve_plot_states(apps, schema_editor):
    ReservePlotState = apps.get_model("main", "ReservePlotState")

    if connection.schema_name == 'public':
        ReservePlotState.objects.create(state='reserved')
        ReservePlotState.objects.create(state='deleted')
        ReservePlotState.objects.create(state='buried')



class Migration(migrations.Migration):

    replaces = [('main', '0001_squashed_0034_auto_20150805_1425'), ('main', '0002_auto_20150826_1450'), ('main', '0003_auto_20150817_1612'), ('main', '0004_auto_20150817_1643'), ('main', '0005_auto_20150909_0943'), ('main', '0006_auto_20150902_1027'), ('main', '0007_auto_20151203_1404'), ('main', '0007_auto_20151201_1512'), ('main', '0008_merge'), ('main', '0009_dataentryuser'), ('main', '0010_newdatamatchinguser'), ('main', '0011_auto_20160321_1639'), ('main', '0010_auto_20160331_0947'), ('main', '0012_merge'), ('main', '0013_auto_20160422_1210'), ('main', '0014_burialimage'), ('main', '0015_delete_burialimage'), ('main', '0015_auto_20160601_1500'), ('main', '0016_merge'), ('main', '0017_auto_20160609_1433'), ('main', '0018_auto_20160622_1007'), ('main', '0019_auto_20160623_1351'), ('main', '0020_burialofficialtype'), ('main', '0021_auto_20160712_1139'), ('main', '0022_auto_20160712_1427'), ('main', '0021_auto_20160715_0910'), ('main', '0023_merge'), ('main', '0024_auto_20160715_1620'), ('main', '0025_auto_20160718_1433'), ('main', '0026_auto_20160718_1618'), ('main', '0027_reserveplotstate'), ('main', '0028_auto_20160809_0830'), ('main', '0029_auto_20160823_1110'), ('main', '0030_auto_20160919_1437'), ('main', '0031_auto_20160920_1434'), ('main', '0032_featurecode_hierarchy'), ('main', '0033_auto_20161006_1000'), ('main', '0034_auto_20161212_1634'), ('main', '0035_auto_20170129_1318'), ('main', '0036_auto_20170129_1334'), ('main', '0037_auto_20170129_1714')]

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BGUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(verbose_name='first name', blank=True, max_length=30)),
                ('last_name', models.CharField(verbose_name='last name', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='email address', max_length=75, unique=True)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups', related_query_name='user', blank=True, related_name='user_set', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', verbose_name='user permissions', related_query_name='user', blank=True, related_name='user_set', to='auth.Permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('first_line', models.CharField(max_length=100)),
                ('second_line', models.CharField(max_length=50, null=True)),
                ('third_line', models.CharField(max_length=50, null=True)),
                ('fourth_line', models.CharField(max_length=50, null=True)),
                ('fifth_line', models.CharField(max_length=50, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('county', models.CharField(max_length=50, null=True)),
                ('postcode', models.CharField(max_length=10, null=True)),
                ('country', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BurialGroundSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('domain_url', models.CharField(max_length=128, unique=True)),
                ('schema_name', models.CharField(max_length=63, unique=True, validators=[tenant_schemas.postgresql_backend.base._check_schema_name])),
                ('name', models.CharField(max_length=100)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('aws_media_bucket', models.CharField(default='', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BurialOfficialType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('official_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=35)),
                ('description', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='ImageState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('image_state', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('image_type', models.CharField(default='memorial', max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('parish', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('profession', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('religion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Nicknames',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nickname', models.CharField(max_length=20)),
                ('actual_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SiteGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('burialgroundsite', models.ForeignKey(to='main.BurialGroundSite', on_delete=models.CASCADE)),
                ('group', models.ForeignKey(to='auth.Group', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterField(
            model_name='burialgroundsite',
            name='aws_media_bucket',
            field=models.CharField(help_text='Endpoint of the AWS S3 media bucket.', max_length=100),
        ),
        migrations.AlterField(
            model_name='burialgroundsite',
            name='created_on',
            field=models.DateField(help_text='Date the site is added', auto_now_add=True),
        ),
        migrations.AddField(
            model_name='bguser',
            name='site_groups',
            field=models.ManyToManyField(to='main.SiteGroup'),
        ),
        migrations.AlterModelOptions(
            name='bguser',
            options={},
        ),
        migrations.AddField(
            model_name='bguser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bguser',
            name='email',
            field=models.EmailField(help_text='Required.', verbose_name='email address', max_length=75, unique=True),
        ),
        migrations.CreateModel(
            name='TenantUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('main.bguser',),
        ),
        migrations.RemoveField(
            model_name='bguser',
            name='is_admin',
        ),
        # migrations.RunPython(
        #     code=main.migrations.0001_squashed_0034_auto_20150805_1425.move_users,
        # ),
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('isMailVerified', models.BooleanField(default=False)),
                ('activation_key', models.CharField(blank=True, max_length=40)),
                ('key_expires', models.DateTimeField(default=datetime.date(2015, 7, 29))),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.AlterField(
            model_name='bguser',
            name='username',
            field=models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], blank=True),
        ),
        migrations.AlterField(
            model_name='bguser',
            name='username',
            field=models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], null=True),
        ),
        migrations.CreateModel(
            name='SiteDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('default_srid', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=20)),
                ('latitude', models.FloatField(help_text='Latitude for the Site center coordinates')),
                ('longitude', models.FloatField(help_text='Longitude for the Site center coordinates')),
                ('zoom_level', models.IntegerField(help_text='Zoom level to start with: Usually it is set accordingly to the site size in order to cover all the site in the first load')),
                ('url', models.CharField(max_length=300, null=True)),
                ('layer', models.CharField(max_length=20, null=True)),
                ('matrixSet', models.CharField(max_length=20, null=True)),
                ('style', models.CharField(max_length=10, null=True)),
                ('extent', models.CharField(help_text='Extend for the tile grid', max_length=300, null=True)),
                ('resolutions', models.CharField(help_text='The resolution to be use for the projection EPSG:27700 (British projection) with the corresponding scale is:: resolutions: [2,799.9999999999995, 1,399.9999999999998, 699.9999999999999, 349.99999999999994, 280, 140, 70, 27.999999999999996, 13.999999999999998, 6.999999999999999, 2.8, 1.4, 0.7, 0.28, 0.14, 0.07, 0.028] Scale (m):  1:10,000,000         1:5,000,000          1:2,500,000       1:1,250,000         1:1,000,000      1:500,000      1:250,000      1:100,000    1:50,000    1:25,000   1:10,000     1:5,000    1:2,500     1:1,000   1:500     1:250    1:100', max_length=300, null=True)),
                ('matrixIds', models.CharField(help_text='Vector that contains Ids for resolutions, therefore the lenght of this vector have to be equal to resolutions', max_length=200, null=True)),
                ('address', models.OneToOneField(to='main.Address', null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='BurialOfficialType',
        ),
        migrations.DeleteModel(
            name='Profession',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='city',
            new_name='town',
        ),
        migrations.RemoveField(
            model_name='address',
            name='country',
        ),
        migrations.RemoveField(
            model_name='address',
            name='fifth_line',
        ),
        migrations.RemoveField(
            model_name='address',
            name='fourth_line',
        ),
        migrations.RemoveField(
            model_name='address',
            name='second_line',
        ),
        migrations.RemoveField(
            model_name='address',
            name='third_line',
        ),
        migrations.AddField(
            model_name='burialgroundsite',
            name='site_details',
            field=models.OneToOneField(to='main.SiteDetails', null=True),
        ),
        # migrations.RunPython(
        #     code=main.migrations.0001_squashed_0034_auto_20150805_1425.move_site_details,
        # ),
        migrations.AlterField(
            model_name='registereduser',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 8, 4)),
        ),
        migrations.AlterModelOptions(
            name='sitedetails',
            options={'verbose_name_plural': 'Site Details'},
        ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='name',
        ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='zoom_level',
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='key_expires',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='FeatureCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('feature_type', models.CharField(max_length=20)),
                ('display_name', models.CharField(max_length=20)),
            ],
        ),
        # migrations.RunPython(
        #     code=main.migrations.0002_auto_20150826_1450.create_feature_code,
        #     reverse_code=main.migrations.0002_auto_20150826_1450.undo_move_feature_code,
        # ),
        migrations.CreateModel(
            name='Surveyor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('surveyor_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='imagetype',
            name='image_type',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 8, 26)),
        ),
        migrations.AlterModelManagers(
            name='bguser',
            managers=[
                ('objects', main.models.BGUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='bguser',
            name='email',
            field=models.EmailField(help_text='Required.', verbose_name='email address', max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='bguser',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', related_query_name='user', blank=True, related_name='user_set', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='bguser',
            name='last_login',
            field=models.DateTimeField(verbose_name='last login', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='imagetype',
            name='image_type',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='sitedetails',
            name='address',
            field=models.ForeignKey(to='main.Address', null=True),
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='key_expires',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='FeatureGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('group_code', models.CharField(max_length=20)),
                ('display_name', models.CharField(max_length=20)),
                ('hierarchy', models.IntegerField()),
                ('initial_visibility', models.BooleanField(default=False)),
                ('switch_on_off', models.BooleanField(default=True)),
                ('feature_codes', models.ManyToManyField(to='main.FeatureCode')),
            ],
        ),
        migrations.AddField(
            model_name='featurecode',
            name='show_in_toolbar',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='featurecode',
            name='max_resolution',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='featurecode',
            name='min_resolution',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='featurecode',
            name='type',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        # migrations.RunPython(
        #     code=main.migrations.0006_auto_20150902_1027.populate_feature_codes,
        # ),
        migrations.RemoveField(
            model_name='burialgroundsite',
            name='aws_media_bucket',
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='key_expires',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        # migrations.RunPython(
        #     code=main.migrations.0007_auto_20151203_1404.create_layers,
        # ),
        migrations.AlterField(
            model_name='featurecode',
            name='feature_type',
            field=models.CharField(max_length=20, db_index=True),
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
            name='NewDataMatchingUser',
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
        migrations.DeleteModel(
            name='NewDataMatchingUser',
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
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=35),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(blank=True, max_length=35),
        ),
        migrations.AlterField(
            model_name='parish',
            name='parish',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='religion',
            name='religion',
            field=models.CharField(blank=True, max_length=50),
        ),
        # migrations.RunPython(
        #     code=main.migrations.0013_auto_20160422_1210.create_image_state,
        # ),
        # migrations.RunPython(
        #     code=main.migrations.0015_auto_20160601_1500.change_displayname_featuregroup,
        # ),
        # migrations.RunPython(
        #     code=main.migrations.0017_auto_20160609_1433.populate_featurecode_featuregroup,
        # ),
        # migrations.RunPython(
        #     code=main.migrations.0018_auto_20160622_1007.populate_featurecode_featuregroup,
        # ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=35, validators=[main.validators.bleach_validator], null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(blank=True, max_length=35, validators=[main.validators.bleach_validator], null=True),
        ),
        migrations.AlterField(
            model_name='featurecode',
            name='display_name',
            field=models.CharField(max_length=20, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='featurecode',
            name='feature_type',
            field=models.CharField(max_length=20, db_index=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='featurecode',
            name='type',
            field=models.CharField(max_length=20, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='featuregroup',
            name='display_name',
            field=models.CharField(max_length=20, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='featuregroup',
            name='group_code',
            field=models.CharField(max_length=20, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='imagestate',
            name='image_state',
            field=models.CharField(max_length=15, unique=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='imagetype',
            name='image_type',
            field=models.CharField(max_length=20, unique=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='nicknames',
            name='actual_name',
            field=models.CharField(max_length=30, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='nicknames',
            name='nickname',
            field=models.CharField(max_length=20, validators=[main.validators.bleach_validator]),
        ),
        migrations.AlterField(
            model_name='parish',
            name='parish',
            field=models.CharField(blank=True, max_length=50, validators=[main.validators.bleach_validator], null=True),
        ),
        migrations.AlterField(
            model_name='religion',
            name='religion',
            field=models.CharField(blank=True, max_length=50, validators=[main.validators.bleach_validator], null=True),
        ),
        migrations.AlterField(
            model_name='surveyor',
            name='surveyor_name',
            field=models.CharField(max_length=100, validators=[main.validators.bleach_validator]),
        ),
        migrations.CreateModel(
            name='BurialOfficialType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, db_index=True, serialize=False, primary_key=True, editable=False)),
                ('official_type', models.CharField(max_length=50, validators=[main.validators.bleach_validator])),
            ],
        ),
        # migrations.RunPython(
        #     code=main.migrations.0021_auto_20160712_1139.update_burial_officials,
        #     reverse_code=main.migrations.0021_auto_20160712_1139.undo_update_burial_officials,
        # ),
        # migrations.RunPython(
        #     code=main.migrations.0022_auto_20160712_1427.delete_burial_officials,
        #     reverse_code=main.migrations.0022_auto_20160712_1427.undo_delete_burial_officials,
        # ),
        # migrations.RunPython(
        #     code=main.migrations.0021_auto_20160715_0910.switch_initial_visibility_for_new_sites,
        # ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='default_srid',
        ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='matrixIds',
        ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='resolutions',
        ),
        migrations.RemoveField(
            model_name='sitedetails',
            name='style',
        ),
        migrations.AddField(
            model_name='sitedetails',
            name='aerial',
            field=models.BooleanField(default=True, verbose_name='Aerial?'),
        ),
        migrations.AlterField(
            model_name='sitedetails',
            name='layer',
            field=models.CharField(help_text='Only one word in lowercase', verbose_name='Schema Name', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='sitedetails',
            name='layer',
            field=models.CharField(help_text='WMTS Layer name / Schema name', verbose_name='Schema name', max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='ReservePlotState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('state', models.CharField(max_length=20, unique=True)),
            ],
        ),
        # migrations.RunPython(
        #     code=main.migrations.0028_auto_20160809_0830.populate_reserve_plot_states,
        # ),
        migrations.AlterModelOptions(
            name='bguser',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterModelOptions(
            name='tenantuser',
            options={'verbose_name': 'Site User', 'verbose_name_plural': 'Site Users'},
        ),
        migrations.AlterField(
            model_name='bguser',
            name='email',
            field=models.EmailField(help_text='Required.', verbose_name='email address', max_length=254, unique=True, error_messages={'unique': 'User with this email already exists.'}),
        ),
        migrations.AlterField(
            model_name='bguser',
            name='site_groups',
            field=models.ManyToManyField(blank=True, to='main.SiteGroup'),
        ),
        migrations.AlterField(
            model_name='bguser',
            name='username',
            field=models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], error_messages={'unique': 'User with this username already exists.'}, null=True),
        ),
        migrations.AlterField(
            model_name='burialgroundsite',
            name='created_on',
            field=models.DateTimeField(help_text='Date the site is added', auto_now_add=True),
        ),
        # migrations.RunPython(
        #     code=main.migrations.0031_auto_20160920_1434.update_wall_hedge_resolutions,
        # ),
        migrations.AddField(
            model_name='featurecode',
            name='hierarchy',
            field=models.IntegerField(default=0),
        ),
        # migrations.RunPython(
        #     code=main.migrations.0033_auto_20161006_1000.populate_featurecode_hierarchy,
        # ),
        migrations.CreateModel(
            name='SiteGroupSite',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('main.sitegroup',),
        ),
        migrations.AddField(
            model_name='bguser',
            name='_is_staff',
            field=models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status'),
        ),
        # migrations.RunPython(
        #     code=main.migrations.0035_auto_20170129_1318.migrate_featuregroups_featurecodes,
        # ),
        # migrations.RunPython(
        #     code=main.migrations.0036_auto_20170129_1334.migrate_featuregroups_featurecodes,
        # ),
        # migrations.RunPython(
        #     code=main.migrations.0037_auto_20170129_1714.move_featurecodes_fk,
        # ),
    ]
