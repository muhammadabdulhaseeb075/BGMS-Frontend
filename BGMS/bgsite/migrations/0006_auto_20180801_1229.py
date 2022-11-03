# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('main', '0002_currency_relationshiptype'),
        ('bgsite', '0005_auto_20180404_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.TextField(validators=[main.validators.bleach_validator], max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('record_count', models.IntegerField(blank=True, null=True)),
                ('status', models.TextField(validators=[main.validators.bleach_validator], max_length=20)),
                ('report', models.TextField(blank=True, null=True, validators=[main.validators.bleach_validator])),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='FeaturesRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_1_object_id', models.UUIDField()),
                ('feature_2_object_id', models.UUIDField()),
                ('feature_1_content_type', models.ForeignKey(related_name='feature_1_relationship', to='contenttypes.ContentType', on_delete=models.CASCADE)),
                ('feature_2_content_type', models.ForeignKey(related_name='feature_2_relationship', to='contenttypes.ContentType', on_delete=models.CASCADE)),
                ('relationship', models.ForeignKey(to='main.RelationshipType', null=True, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='GraveplotState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.TextField(validators=[main.validators.bleach_validator], max_length=20, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='GraveplotStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(validators=[main.validators.bleach_validator], max_length=20, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='GraveplotType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(validators=[main.validators.bleach_validator], max_length=20, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=30, null=True, validators=[main.validators.bleach_validator], verbose_name='Title')),
                ('first_names', models.CharField(blank=True, max_length=200, null=True, validators=[main.validators.bleach_validator], verbose_name='First names')),
                ('last_name', models.CharField(blank=True, max_length=35, null=True, validators=[main.validators.bleach_validator], verbose_name='Last name')),
                ('owner_date', models.DateField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=400, null=True, validators=[main.validators.bleach_validator])),
                ('address', models.ForeignKey(to='bgsite.Address', blank=True, null=True, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.TextField(validators=[main.validators.bleach_validator], max_length=20, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subsection_name', models.TextField(validators=[main.validators.bleach_validator], max_length=20, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('section', models.ForeignKey(to='bgsite.Section', null=True, on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='burial',
            name='cremated',
            field=models.NullBooleanField(verbose_name='Cremated'),
        ),
        migrations.AddField(
            model_name='burial',
            name='cremation_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='burial',
            name='depth_position',
            field=models.IntegerField(blank=True, null=True, verbose_name='Depth position of grave'),
        ),
        migrations.AddField(
            model_name='burial',
            name='impossible_order_date',
            field=models.BooleanField(editable=False, default=False),
        ),
        migrations.AddField(
            model_name='burial',
            name='impossible_order_date_day',
            field=models.IntegerField(blank=True, null=True, verbose_name='Day of order'),
        ),
        migrations.AddField(
            model_name='burial',
            name='impossible_order_date_month',
            field=models.IntegerField(blank=True, null=True, verbose_name='Month of order'),
        ),
        migrations.AddField(
            model_name='burial',
            name='impossible_order_date_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Year of order'),
        ),
        migrations.AddField(
            model_name='burial',
            name='order_date',
            field=models.DateField(editable=False, null=True, db_index=True),
        ),
        migrations.AddField(
            model_name='burial',
            name='register',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[main.validators.bleach_validator], verbose_name='Register recording burial name/code'),
        ),
        migrations.AddField(
            model_name='burial',
            name='registration_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Registration Number'),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='consecrated',
            field=models.NullBooleanField(verbose_name='Consecrated ground'),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='cost_currency',
            field=models.ForeignKey(to='main.Currency', blank=True, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='cost_subunit',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='cost_subunit2',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='cost_unit',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='depth',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='impossible_date',
            field=models.BooleanField(editable=False, default=False),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='impossible_date_day',
            field=models.IntegerField(blank=True, null=True, verbose_name='Day of Burial'),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='impossible_date_month',
            field=models.IntegerField(blank=True, null=True, verbose_name='Month of Burial'),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='impossible_date_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Year of Burial'),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='length',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='memorial_comment',
            field=models.CharField(blank=True, max_length=400, null=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='perpetual',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='purchase_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='remarks',
            field=models.CharField(blank=True, max_length=400, null=True, validators=[main.validators.bleach_validator]),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='size_units',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[main.validators.bleach_validator], default='m'),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='tenure_years',
            field=models.IntegerField(blank=True, null=True, verbose_name='Tenure in years'),
        ),
        migrations.AlterField(
            model_name='graveplot',
            name='width',
            field=models.FloatField(blank=True, null=True, default=1.5),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='data_upload',
            field=models.ForeignKey(verbose_name='Data Upload', to='bgsite.DataUpload', help_text='The data upload from which this record was created.', blank=True, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='section',
            field=models.ForeignKey(verbose_name='Section', to='bgsite.Section', help_text='Section containing the plot.', blank=True, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='state',
            field=models.ForeignKey(verbose_name='Graveplot State', to='bgsite.GraveplotState', help_text='E.g. occupied, empty, full.', blank=True, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='status',
            field=models.ForeignKey(verbose_name='Graveplot Status', to='bgsite.GraveplotStatus', help_text='E.g. private, common, invalid.', blank=True, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='subsection',
            field=models.ForeignKey(verbose_name='Subsection', to='bgsite.Subsection', help_text='Subsection containing the plot.', blank=True, null=True, on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='graveplot',
            unique_together=set([('grave_number', 'section', 'subsection')]),
        ),
        migrations.AddField(
            model_name='graveplot',
            name='type',
            field=models.ForeignKey(verbose_name='Graveplot Type', to='bgsite.GraveplotType', help_text='E.g. earthen grave, brick grave.', blank=True, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='memorial',
            name='data_upload',
            field=models.ForeignKey(verbose_name='Data Upload', to='bgsite.DataUpload', help_text='The data upload from which this record was created.', blank=True, null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='person',
            name='data_upload',
            field=models.ForeignKey(verbose_name='Data Upload', to='bgsite.DataUpload', help_text='The data upload from which this record was created.', blank=True, null=True, on_delete=models.CASCADE),
        ),
    ]
