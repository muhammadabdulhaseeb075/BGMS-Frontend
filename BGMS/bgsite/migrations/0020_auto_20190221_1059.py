# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion
import bgsite.models
import main.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_merge'),
        ('bgsite', '0019_auto_20190208_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraveDeed',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('deed_url', models.FileField(upload_to=bgsite.models.user_uploaded_deed_path, max_length=200)),
                ('deed_number', models.IntegerField(null=True, unique=True)),
                ('cost_unit', models.IntegerField(null=True, blank=True)),
                ('cost_subunit', models.IntegerField(null=True, blank=True)),
                ('cost_subunit2', models.FloatField(null=True, blank=True)),
                ('purchase_date', models.DateField(null=True, blank=True)),
                ('impossible_date', models.BooleanField(editable=False, default=False)),
                ('impossible_date_day', models.IntegerField(null=True, verbose_name='Day of Purchase', blank=True)),
                ('impossible_date_month', models.IntegerField(null=True, verbose_name='Month of Purchase', blank=True)),
                ('impossible_date_year', models.IntegerField(null=True, verbose_name='Year of Purchase', blank=True)),
                ('tenure_years', models.IntegerField(null=True, verbose_name='Tenure in years', blank=True)),
                ('remarks', models.CharField(null=True, blank=True, max_length=400, validators=[main.validators.bleach_validator])),
                ('date', models.DateTimeField(null=True, auto_now_add=True)),
                ('cost_currency', models.ForeignKey(null=True, blank=True, to='main.Currency', on_delete=models.CASCADE)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('graveplot', models.ForeignKey(to='bgsite.GravePlot', related_name='graveplot_deeds', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='GraveOwner',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('ownership_order', models.IntegerField(default=1)),
                ('active_owner', models.BooleanField(default=True)),
                ('owner_date', models.DateField(null=True, blank=True)),
                ('impossible_owner_date', models.BooleanField(editable=False, default=False)),
                ('owner_date_day', models.IntegerField(null=True, verbose_name='Day of Ownership', blank=True)),
                ('owner_date_month', models.IntegerField(null=True, verbose_name='Month of Ownership', blank=True)),
                ('owner_date_year', models.IntegerField(null=True, verbose_name='Year of Ownership', blank=True)),
                ('deed', models.ForeignKey(to='bgsite.GraveDeed', related_name='grave_owners', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='owner',
            name='company_name',
            field=models.CharField(null=True, verbose_name='Company name', blank=True, max_length=200, validators=[main.validators.bleach_validator]),
        ),
        migrations.AddField(
            model_name='owner',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='owner',
            name='date',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='dataupload',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='graveplotstate',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='graveplotstatus',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='graveplottype',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='section',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subsection',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userrequest',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='graveowner',
            name='owner',
            field=models.ForeignKey(to='bgsite.Owner', related_name='grave_owners', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='gravedeed',
            name='owners',
            field=models.ManyToManyField(through='bgsite.GraveOwner', to='bgsite.Owner', related_name='grave_deeds'),
        ),
    ]
