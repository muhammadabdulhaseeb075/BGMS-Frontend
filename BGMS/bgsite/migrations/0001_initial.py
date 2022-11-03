# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
import bgsite.models
import django.utils.timezone
import uuid
from django.conf import settings
import main.validators
import django.db.models.deletion

def populate_sitegroups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    SiteGroup = apps.get_model("main", "SiteGroup")
    BurialGroundSite = apps.get_model("main", "BurialGroundSite")
    # import pdb; pdb.set_trace()
    # if connection.schema_name == 'public':
    bgs = BurialGroundSite.objects.latest('created_on')
    # for bgs in bgss:
    if bgs.schema_name != 'public':
        groups = Group.objects.filter(name__in=['User', 'SiteUser', 'SiteMember', 'DataMatcher', 'SiteWarden', 'DataEntry', 'MemorialPhotographer', 'SiteAdmin'])
        for group in groups:
            SiteGroup.objects.update_or_create(group=group, burialgroundsite=bgs)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geometriespublic', '0001_initial'),
        ('main', '0001_initial'),
        ('geometries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('first_line', models.CharField(max_length=100, validators=[main.validators.bleach_validator], blank=True)),
                ('second_line', models.CharField(max_length=100, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('town', models.CharField(max_length=50, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('county', models.CharField(max_length=50, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('postcode', models.CharField(max_length=10, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('country', models.CharField(max_length=50, validators=[main.validators.bleach_validator], null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Burial',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('burial_number', models.CharField(max_length=10, validators=[main.validators.bleach_validator], null=True, help_text='Serial number of the entry in physical book', blank=True)),
                ('burial_date', models.DateField(db_index=True, editable=False, null=True)),
                ('impossible_date', models.BooleanField(default=False, editable=False)),
                ('impossible_date_day', models.IntegerField(verbose_name='Day of Burial', null=True, blank=True)),
                ('impossible_date_month', models.IntegerField(verbose_name='Month of Burial', null=True, blank=True)),
                ('impossible_date_year', models.IntegerField(verbose_name='Year of Burial', null=True, blank=True)),
                ('consecrated', models.NullBooleanField(verbose_name='In consecrated ground', default=True)),
                ('cremation_certificate_no', models.CharField(verbose_name='Cremation Certificate No.', max_length=35, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('interred', models.NullBooleanField(verbose_name='Interred', default=False)),
                ('depth', models.CharField(verbose_name='Depth of grave', max_length=15, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('depth_units', models.CharField(verbose_name='Depth Units(ft/m/cm)', max_length=15, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('burial_remarks', models.CharField(verbose_name='Additional Info not elsewhere specified', max_length=200, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('requires_investigation', models.BooleanField(verbose_name='Needs checking', default=False)),
                ('user_remarks', models.CharField(verbose_name='Comments', max_length=200, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('situation', models.CharField(verbose_name='Grave Location', max_length=50, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('grave_number', models.CharField(verbose_name='Grave Number', max_length=20, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('place_from_which_brought', models.CharField(verbose_name='Place/Parish from which brought', max_length=100, validators=[main.validators.bleach_validator], null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Burial_Official',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('official_type', models.CharField(max_length=50, null=True)),
                ('burial', models.ForeignKey(to='bgsite.Burial', on_delete=models.CASCADE)),
                ('burial_official_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.BurialOfficialType', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GravePlot',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('description', models.CharField(max_length=300, null=True, validators=[main.validators.bleach_validator])),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('feature_id', models.CharField(max_length=10, null=True)),
                ('grave_number', models.CharField(max_length=20, null=True, validators=[main.validators.bleach_validator])),
                ('width', models.FloatField(default=1.5, null=True)),
                ('memorial_feature_id', models.CharField(max_length=10, null=True)),
                ('topopolygon', models.OneToOneField(editable=False, to='geometries.TopoPolygons', null=True, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('url', models.ImageField(max_length=200, upload_to=bgsite.models.user_uploaded_image_path)),
                ('metadata', models.CharField(max_length=100, null=True, validators=[main.validators.bleach_validator])),
            ],
        ),
        migrations.CreateModel(
            name='Memorial',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('description', models.CharField(max_length=300, null=True, validators=[main.validators.bleach_validator])),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('feature_id', models.CharField(max_length=10, null=True)),
                ('user_generated', models.BooleanField(default=False)),
                ('inscription', models.CharField(max_length=400, null=True, validators=[main.validators.bleach_validator])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MemorialGraveplot',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('graveplot', models.ForeignKey(to='bgsite.GravePlot', on_delete=models.CASCADE)),
                ('memorial', models.ForeignKey(to='bgsite.Memorial', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Official',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('title', models.CharField(verbose_name='Title', max_length=100, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('first_names', models.CharField(verbose_name='First names', max_length=200, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('last_name', models.CharField(verbose_name='Last name', max_length=35, null=True, blank=True, db_index=True, validators=[main.validators.bleach_validator])),
                ('used_on', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('title', models.CharField(verbose_name='Title', max_length=30, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('first_names', models.CharField(verbose_name='First names', max_length=200, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('birth_name', models.CharField(verbose_name='Birth name', max_length=200, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('other_names', models.CharField(verbose_name='Nicknames', max_length=100, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('last_name', models.CharField(verbose_name='Last name', max_length=35, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('birth_date', models.DateField(editable=False, null=True)),
                ('impossible_date', models.BooleanField(default=False, help_text='If true means the others impossible_date fields have the non real date entered in the registry for the person', editable=False)),
                ('impossible_date_day', models.IntegerField(verbose_name='Day of Birth', null=True, blank=True)),
                ('impossible_date_month', models.IntegerField(verbose_name='Month of Birth', null=True, blank=True)),
                ('impossible_date_year', models.IntegerField(verbose_name='Year of Birth', null=True, blank=True)),
                ('gender', models.CharField(verbose_name='Gender', max_length=10, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('description', models.CharField(verbose_name='Description of Person', max_length=200, validators=[main.validators.bleach_validator], null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profession',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('profession', models.CharField(max_length=50, validators=[main.validators.bleach_validator], blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('top_left_bottom_right', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='UserRequest',
            fields=[
                ('id', models.UUIDField(db_index=True, primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
                ('comments', models.CharField(max_length=200, validators=[main.validators.bleach_validator])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Death',
            fields=[
                ('person', models.OneToOneField(primary_key=True, help_text='One-to-One relationship', serialize=False, to='bgsite.Person', editable=False, on_delete=models.CASCADE)),
                ('age_years', models.PositiveIntegerField(verbose_name='Age(years)', db_index=True, null=True, blank=True)),
                ('age_months', models.PositiveIntegerField(verbose_name='Age(months)', null=True, blank=True)),
                ('age_weeks', models.PositiveIntegerField(verbose_name='Age(weeks)', null=True, blank=True)),
                ('age_days', models.PositiveIntegerField(verbose_name='Age(days)', null=True, blank=True)),
                ('age_hours', models.PositiveIntegerField(verbose_name='Age(hours)', null=True, blank=True)),
                ('death_date', models.DateField(db_index=True, editable=False, null=True)),
                ('impossible_date', models.BooleanField(default=False, editable=False)),
                ('impossible_date_day', models.IntegerField(verbose_name='Day of Death', null=True, blank=True)),
                ('impossible_date_month', models.IntegerField(verbose_name='Month of Death', null=True, blank=True)),
                ('impossible_date_year', models.IntegerField(verbose_name='Year of death', null=True, blank=True)),
                ('death_year', models.CharField(max_length=6, validators=[main.validators.bleach_validator], null=True, blank=True, editable=False, help_text='Optional. Temp daeth_year as char to record death date off headstone')),
                ('death_cause', models.CharField(verbose_name='Cause of death', max_length=250, validators=[main.validators.bleach_validator], null=True, blank=True)),
                ('address', models.ForeignKey(verbose_name='Place of Death', null=True, blank=True, to='bgsite.Address', help_text='Optional. Death have one related Address', on_delete=models.CASCADE)),
                ('event', models.CharField(verbose_name='War/Event related to Death', max_length=250, null=True, blank=True, help_text='Optional. Death have one related Event')),
            ],
        ),
        migrations.CreateModel(
            name='ReservedPlot',
            fields=[
                ('person', models.OneToOneField(primary_key=True, serialize=False, to='bgsite.Person', on_delete=models.CASCADE)),
                ('date', models.DateTimeField(auto_now=True)),
                ('notes', models.CharField(max_length=200, null=True, validators=[main.validators.bleach_validator])),
                ('grave_plot', models.ForeignKey(null=True, blank=True, to='bgsite.GravePlot', on_delete=models.CASCADE)),
                ('origin', models.ForeignKey(null=True, blank=True, to='geometriespublic.FeatureCode', on_delete=models.CASCADE)),
                ('state', models.ForeignKey(to='main.ReservePlotState', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('image', models.OneToOneField(primary_key=True, serialize=False, to='bgsite.Image', on_delete=models.CASCADE)),
                ('url', models.ImageField(upload_to=bgsite.models.user_uploaded_thumbnail_path)),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='image',
            field=models.ForeignKey(to='bgsite.Image', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='tag',
            name='person',
            field=models.ForeignKey(to='bgsite.Person', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='person',
            name='profession',
            field=models.ForeignKey(verbose_name='Profession', null=True, blank=True, to='bgsite.Profession', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='person',
            name='residence_address',
            field=models.ForeignKey(verbose_name='Residence Address', null=True, blank=True, to='bgsite.Address', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='memorial',
            name='graveplot_memorials',
            field=models.ManyToManyField(to='bgsite.GravePlot', through='bgsite.MemorialGraveplot'),
        ),
        migrations.AddField(
            model_name='memorial',
            name='images',
            field=models.ManyToManyField(to='bgsite.Image'),
        ),
        migrations.AddField(
            model_name='memorial',
            name='topopolygon',
            field=models.OneToOneField(editable=False, to='geometries.TopoPolygons', null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='image',
            name='image_state',
            field=models.ForeignKey(to='main.ImageState', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='image',
            name='image_type',
            field=models.ForeignKey(to='main.ImageType', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='burial_official',
            name='official',
            field=models.ForeignKey(to='bgsite.Official', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='burial',
            name='burial_officials',
            field=models.ManyToManyField(verbose_name='Burial Official', to='bgsite.Official', through='bgsite.Burial_Official', blank=True),
        ),
        migrations.AddField(
            model_name='burial',
            name='burial_record_image',
            field=models.ForeignKey(null=True, blank=True, to='bgsite.Image', editable=False, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='burial',
            name='graveplot',
            field=models.ForeignKey(null=True, to='bgsite.GravePlot', editable=False, help_text='Multiple people buried in same plot eg. family members but only one graveplot per burial record', on_delete=models.CASCADE),
        ),
        migrations.CreateModel(
            name='BurialImage',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('bgsite.image',),
        ),
        migrations.AddField(
            model_name='death',
            name='memorials',
            field=models.ManyToManyField(to='bgsite.Memorial', help_text='Many-to-Many relationship', editable=False),
        ),
        migrations.AddField(
            model_name='death',
            name='parish',
            field=models.CharField(verbose_name='Parish', max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='death',
            name='religion',
            field=models.CharField(verbose_name='Religion', max_length=250, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='burial',
            name='death',
            field=models.ForeignKey(help_text='Same Death person can be buried multiple times', to='bgsite.Death', editable=False, on_delete=models.CASCADE),
        ),
        migrations.RunPython(
            code=populate_sitegroups,
        ),
    ]
