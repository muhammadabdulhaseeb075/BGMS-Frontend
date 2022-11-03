# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, connection
import datetime
import tenant_schemas.postgresql_backend.base
import django.core.validators
import django.utils.timezone
from django.conf import settings


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# main.migrations.0032_auto_20150729_1554
# main.migrations.0026_auto_20150721_1234


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    
def move_users(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.

    cursor = connection.cursor()
    cursor.execute("""SELECT 1
        FROM   information_schema.tables 
        WHERE  table_schema = 'public'
        AND    table_name = 'auth_user'""")
    if cursor.fetchone() is not None:
        cursor.execute("SELECT * FROM auth_user")
        rows = dictfetchall(cursor)
        BGUser = apps.get_model("main", "BGUser")
        if not BGUser.objects.all().exists():
            for person in rows:
                BGUser = apps.get_model("main", "BGUser")
                bguser = BGUser(username=person['username'], email=person['email'], password=person['password'], 
                                first_name=person['first_name'], last_name=person['last_name'], 
                                last_login=person['last_login'], date_joined=person['date_joined'], 
                                is_superuser=person['is_superuser'], is_active=person['is_active'])
                bguser.save()
                
def move_site_details(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.

    BurialGroundSite = apps.get_model("main", "BurialGroundSite")
    burialgroundsites = BurialGroundSite.objects.all()
    SiteDetails = apps.get_model("main", "SiteDetails")
    if not SiteDetails.objects.all().exists():
        for site in burialgroundsites:
            if site.schema_name != 'public':
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM {0}.bgsite_sitedetails".format(site.schema_name))
                rows = dictfetchall(cursor)
                if len(rows) >0:
                    row = rows[0]
                    details = SiteDetails.objects.create(address_id=row['address_id'], default_srid=row['default_srid'],
                                                         name=row['name'], latitude=row['latitude'],
                                                         longitude=row['longitude'], zoom_level=row['zoom_level'],
                                                         url=row['url'], layer=row['layer'], matrixSet=row['matrixSet'],
                                                         style=row['style'], extent=row['extent'], resolutions=row['resolutions'],
                                                         matrixIds=row['matrixIds'])
                    site.site_details = details
                    site.save()
                    

class Migration(migrations.Migration):

#     replaces = [('main', '0001_initial'), ('main', '0002_auto_20150311_1158'), ('main', '0003_auto_20150311_1218'), ('main', '0004_auto_20150324_0959'), ('main', '0005_auto_20150324_1017'), ('main', '0006_auto_20150324_1017'), ('main', '0007_burialgroundsite_aws_media_bucket'), ('main', '0008_nicknames'), ('main', '0009_siteuser_user_group'), ('main', '0013_bguser_tenantsiteuser'), ('main', '0010_auto_20150713_1504'), ('main', '0011_auto_20150713_1527'), ('main', '0012_auto_20150713_1535'), ('main', '0014_delete_tenantsiteuser'), ('main', '0015_auto_20150720_0835'), ('main', '0016_bguser'), ('main', '0017_auto_20150720_0921'), ('main', '0018_remove_bguser_is_staff'), ('main', '0019_bguser_site_groups'), ('main', '0020_auto_20150720_1048'), ('main', '0021_auto_20150720_1347'), ('main', '0022_tenantsiteuser'), ('main', '0023_auto_20150720_1458'), ('main', '0024_delete_tenantuser'), ('main', '0025_tenantuser'), ('main', '0026_auto_20150721_1234'), ('main', '0027_registereduser'), ('main', '0028_auto_20150723_0951'), ('main', '0029_auto_20150723_1004'), ('main', '0030_auto_20150728_1000'), ('main', '0031_auto_20150729_1530'), ('main', '0032_auto_20150729_1554'), ('main', '0033_auto_20150804_1501'), ('main', '0034_auto_20150805_1425')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BGUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=75, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', verbose_name='groups', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', verbose_name='user permissions', to='auth.Permission', help_text='Specific permissions for this user.')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_line', models.CharField(max_length=100)),
                ('second_line', models.CharField(null=True, max_length=50)),
                ('third_line', models.CharField(null=True, max_length=50)),
                ('fourth_line', models.CharField(null=True, max_length=50)),
                ('fifth_line', models.CharField(null=True, max_length=50)),
                ('city', models.CharField(null=True, max_length=50)),
                ('county', models.CharField(null=True, max_length=50)),
                ('postcode', models.CharField(null=True, max_length=10)),
                ('country', models.CharField(null=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BurialGroundSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_url', models.CharField(unique=True, max_length=128)),
                ('schema_name', models.CharField(validators=[tenant_schemas.postgresql_backend.base._check_schema_name], unique=True, max_length=63)),
                ('name', models.CharField(max_length=100)),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BurialOfficialType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('official_type', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('description', models.CharField(max_length=35)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_state', models.CharField(unique=True, max_length=15)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_type', models.CharField(default='memorial', unique=True, max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Parish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parish', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('religion', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='burialgroundsite',
            name='aws_media_bucket',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Nicknames',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=20)),
                ('actual_name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('burialgroundsite', models.ForeignKey(to='main.BurialGroundSite', on_delete=models.CASCADE)),
                ('group', models.ForeignKey(to='auth.Group', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='burialgroundsite',
            name='aws_media_bucket',
            field=models.CharField(max_length=100, help_text='Endpoint of the AWS S3 media bucket.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='burialgroundsite',
            name='created_on',
            field=models.DateField(auto_now_add=True, help_text='Date the site is added'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bguser',
            name='email',
            field=models.EmailField(unique=True, max_length=75, verbose_name='email address'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='bguser',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='bguser',
            name='site_groups',
            field=models.ManyToManyField(to='main.SiteGroup'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='bguser',
            options={},
        ),
        migrations.AddField(
            model_name='bguser',
            name='is_admin',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bguser',
            name='email',
            field=models.EmailField(help_text='Required.', unique=True, max_length=75, verbose_name='email address'),
            preserve_default=True,
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
        migrations.RunPython(
            code=move_users,
            reverse_code=None,
            atomic=True,
        ),
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isMailVerified', models.BooleanField(default=False)),
                ('activation_key', models.CharField(blank=True, max_length=40)),
                ('key_expires', models.DateTimeField(default=datetime.date(2015, 7, 29))),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='bguser',
            name='username',
            field=models.CharField(blank=True, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], verbose_name='username', max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bguser',
            name='username',
            field=models.CharField(unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], verbose_name='username', null=True, max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='SiteDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_srid', models.IntegerField(null=True)),
                ('name', models.CharField(max_length=20)),
                ('latitude', models.FloatField(help_text='Latitude for the Site center coordinates')),
                ('longitude', models.FloatField(help_text='Longitude for the Site center coordinates')),
                ('zoom_level', models.IntegerField(help_text='Zoom level to start with: Usually it is set accordingly to the site size in order to cover all the site in the first load')),
                ('url', models.CharField(null=True, max_length=300)),
                ('layer', models.CharField(null=True, max_length=20)),
                ('matrixSet', models.CharField(null=True, max_length=20)),
                ('style', models.CharField(null=True, max_length=10)),
                ('extent', models.CharField(null=True, max_length=300, help_text='Extend for the tile grid')),
                ('resolutions', models.CharField(null=True, max_length=300, help_text='The resolution to be use for the projection EPSG:27700 (British projection) with the corresponding scale is:: resolutions: [2,799.9999999999995, 1,399.9999999999998, 699.9999999999999, 349.99999999999994, 280, 140, 70, 27.999999999999996, 13.999999999999998, 6.999999999999999, 2.8, 1.4, 0.7, 0.28, 0.14, 0.07, 0.028] Scale (m):  1:10,000,000         1:5,000,000          1:2,500,000       1:1,250,000         1:1,000,000      1:500,000      1:250,000      1:100,000    1:50,000    1:25,000   1:10,000     1:5,000    1:2,500     1:1,000   1:500     1:250    1:100')),
                ('matrixIds', models.CharField(null=True, max_length=200, help_text='Vector that contains Ids for resolutions, therefore the lenght of this vector have to be equal to resolutions')),
                ('address', models.OneToOneField(null=True, to='main.Address')),
            ],
            options={
            },
            bases=(models.Model,),
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
            field=models.OneToOneField(null=True, to='main.SiteDetails', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.RunPython(
            code=move_site_details,
            reverse_code=None,
            atomic=True,
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 8, 4)),
            preserve_default=True,
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
            preserve_default=True,
        ),
    ]
