# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


def populate_feature_codes(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    FeatureCode = apps.get_model("main", "FeatureCode")
    FeatureGroup = apps.get_model("main", "FeatureGroup")
    # add feature code of available_plot, reserved plot, site_boundary if it doesn't exist
    if not FeatureCode.objects.filter(feature_type='available_plot').exists():
        FeatureCode.objects.create(feature_type='available_plot', display_name='Available Plot', min_resolution=0, max_resolution=0.5, type='vector', show_in_toolbar=True)
    FeatureCode.objects.get_or_create(feature_type='reserved_plot', display_name='Reserved Plot', min_resolution=0, max_resolution=0.5, type='vector', show_in_toolbar=True)
    FeatureCode.objects.get_or_create(feature_type='site_boundary', display_name='Site Boundary', min_resolution=0, max_resolution=1600, type='vector', show_in_toolbar=True)
    FeatureCode.objects.get_or_create(feature_type='cluster', display_name='Cluster', min_resolution=0.5, max_resolution=1600, type='cluster', show_in_toolbar=False)
    # create feature groups if they don't exist
    if not FeatureGroup.objects.all().exists():
        
        group = FeatureGroup.objects.create(group_code='vegetation', display_name='Vegetation', 
            switch_on_off=True, initial_visibility=False, hierarchy=12)
        group.feature_codes.add(FeatureCode.objects.get(feature_type='tree'))
        FeatureCode.objects.filter(feature_type='tree').update(min_resolution=0, max_resolution=25, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='bush'))
        FeatureCode.objects.filter(feature_type='bush').update(min_resolution=0, max_resolution=1, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='tree_canopy'))
        FeatureCode.objects.filter(feature_type='tree_canopy').update(min_resolution=0, max_resolution=25, type='vector')
        
        group = FeatureGroup.objects.create(group_code='memorial_cluster', display_name='memorial_cluster', 
            switch_on_off=True, initial_visibility=True, hierarchy=11)
        group.feature_codes.add(FeatureCode.objects.get(feature_type='cluster'))
        FeatureCode.objects.filter(feature_type='cluster').update(min_resolution=0.5, max_resolution=1600, type='cluster', show_in_toolbar=False)
        
        group = FeatureGroup.objects.create(group_code='memorials', display_name='Memorials', 
            switch_on_off=True, initial_visibility=True, hierarchy=10)
        group.feature_codes.add(FeatureCode.objects.get(feature_type='bench'))
        FeatureCode.objects.filter(feature_type='bench').update(min_resolution=0, max_resolution=0.5, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='war_grave'))
        FeatureCode.objects.filter(feature_type='war_grave').update(min_resolution=0, max_resolution=0.5, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='war_memorial'))
        FeatureCode.objects.filter(feature_type='war_memorial').update(min_resolution=0, max_resolution=0.5, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='pavestone'))
        FeatureCode.objects.filter(feature_type='pavestone').update(min_resolution=0, max_resolution=0.5, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='plaque'))
        FeatureCode.objects.filter(feature_type='plaque').update(min_resolution=0, max_resolution=0.5, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='statue'))
        FeatureCode.objects.filter(feature_type='statue').update(min_resolution=0, max_resolution=0.5, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='table_tomb'))
        FeatureCode.objects.filter(feature_type='table_tomb').update(min_resolution=0, max_resolution=0.5, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='window'))
        FeatureCode.objects.filter(feature_type='window').update(min_resolution=0, max_resolution=0.5, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='gravestone'))
        FeatureCode.objects.filter(feature_type='gravestone').update(min_resolution=0, max_resolution=0.5, type='vector')
        
        group = FeatureGroup.objects.create(group_code='plots', display_name='Plots', 
            switch_on_off=True, initial_visibility=True, hierarchy=9)
        group.feature_codes.add(FeatureCode.objects.get(feature_type='plot'))
        FeatureCode.objects.filter(feature_type='plot').update(min_resolution=0, max_resolution=0.5, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='bound_plot'))
        FeatureCode.objects.filter(feature_type='bound_plot').update(min_resolution=0, max_resolution=0.5, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='available_plot'))
        FeatureCode.objects.filter(feature_type='available_plot').update(min_resolution=0, max_resolution=0.5, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='reserved_plot'))
        FeatureCode.objects.filter(feature_type='reserved_plot').update(min_resolution=0, max_resolution=0.5, type='vector')
        
        group = FeatureGroup.objects.create(group_code='aerial', display_name='Map', 
            switch_on_off=True, initial_visibility=True, hierarchy=8)
        group.feature_codes.add(FeatureCode.objects.get_or_create(feature_type='aerial', display_name='Aerial', min_resolution=0, max_resolution=1600, show_in_toolbar=True)[0])
        FeatureCode.objects.filter(feature_type='aerial').update(min_resolution=0, max_resolution=1600, type='raster', show_in_toolbar=True)
        
        group = FeatureGroup.objects.create(group_code='furniture', display_name='Furniture', 
            switch_on_off=True, initial_visibility=False, hierarchy=7)
        group.feature_codes.add(FeatureCode.objects.get(feature_type='bench'))
        FeatureCode.objects.filter(feature_type='bench').update(min_resolution=0, max_resolution=0.25, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='sign'))
        FeatureCode.objects.filter(feature_type='sign').update(min_resolution=0, max_resolution=0.25, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='bollard'))
        FeatureCode.objects.filter(feature_type='bollard').update(min_resolution=0, max_resolution=0.25, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='bin'))
        FeatureCode.objects.filter(feature_type='bin').update(min_resolution=0, max_resolution=0.25, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='lamppost'))
        FeatureCode.objects.filter(feature_type='lamppost').update(min_resolution=0, max_resolution=0.25, type='vector')
        
        group = FeatureGroup.objects.create(group_code='utilities', display_name='Utilities', 
            switch_on_off=True, initial_visibility=False, hierarchy=6)
        group.feature_codes.add(FeatureCode.objects.get(feature_type='manhole'))
        FeatureCode.objects.filter(feature_type='manhole').update(min_resolution=0, max_resolution=0.25, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='gully'))
        FeatureCode.objects.filter(feature_type='gully').update(min_resolution=0, max_resolution=0.25, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='inspection_cover'))
        FeatureCode.objects.filter(feature_type='inspection_cover').update(min_resolution=0, max_resolution=0.25, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='utility_pole'))
        FeatureCode.objects.filter(feature_type='utility_pole').update(min_resolution=0, max_resolution=0.25, type='vector')
        
        group = FeatureGroup.objects.create(group_code='divides', display_name='Divides', 
            switch_on_off=True, initial_visibility=False, hierarchy=5)
        group.feature_codes.add(FeatureCode.objects.get(feature_type='wall'))
        FeatureCode.objects.filter(feature_type='wall').update(min_resolution=0, max_resolution=0.25, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='hedge'))
        FeatureCode.objects.filter(feature_type='hedge').update(min_resolution=0, max_resolution=0.25, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='fence'))
        FeatureCode.objects.filter(feature_type='fence').update(min_resolution=0, max_resolution=0.25, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='gate'))
        FeatureCode.objects.filter(feature_type='gate').update(min_resolution=0, max_resolution=0.25, type='vector')
        
        group = FeatureGroup.objects.create(group_code='buildings', display_name='Building', 
            switch_on_off=False, initial_visibility=False, hierarchy=4)
        group.feature_codes.add(FeatureCode.objects.get(feature_type='building'))
        FeatureCode.objects.filter(feature_type='building').update(min_resolution=0, max_resolution=100, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='steps'))
        FeatureCode.objects.filter(feature_type='steps').update(min_resolution=0, max_resolution=100, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='tank'))
        FeatureCode.objects.filter(feature_type='tank').update(min_resolution=0, max_resolution=100, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='mausoleum'))
        FeatureCode.objects.filter(feature_type='mausoleum').update(min_resolution=0, max_resolution=100, type='vector') 
        
        group = FeatureGroup.objects.create(group_code='thoroughfares', display_name='Thoroughfare', 
            switch_on_off=False, initial_visibility=False, hierarchy=3)
        group.feature_codes.add(FeatureCode.objects.get(feature_type='path'))
        FeatureCode.objects.filter(feature_type='path').update(min_resolution=0, max_resolution=100, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='bridge'))
        FeatureCode.objects.filter(feature_type='bridge').update(min_resolution=0, max_resolution=100, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='road'))
        FeatureCode.objects.filter(feature_type='road').update(min_resolution=0, max_resolution=100, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='car_park'))
        FeatureCode.objects.filter(feature_type='car_park').update(min_resolution=0, max_resolution=100, type='vector')
        
        group = FeatureGroup.objects.create(group_code='natural_surfaces', display_name='Natural Surface', 
            switch_on_off=False, initial_visibility=False, hierarchy=2)
        group.feature_codes.add(FeatureCode.objects.get(feature_type='grass'))
        FeatureCode.objects.filter(feature_type='grass').update(min_resolution=0, max_resolution=100, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='water'))
        FeatureCode.objects.filter(feature_type='water').update(min_resolution=0, max_resolution=100, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='recreation'))
        FeatureCode.objects.filter(feature_type='recreation').update(min_resolution=0, max_resolution=100, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='planting'))
        FeatureCode.objects.filter(feature_type='planting').update(min_resolution=0, max_resolution=100, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='woodland'))
        FeatureCode.objects.filter(feature_type='woodland').update(min_resolution=0, max_resolution=100, type='vector')
        
        group = FeatureGroup.objects.create(group_code='administration', display_name='Administration', 
            switch_on_off=False, initial_visibility=False, hierarchy=1)
        group.feature_codes.add(FeatureCode.objects.get(feature_type='diocese'))
        FeatureCode.objects.filter(feature_type='diocese').update(min_resolution=0, max_resolution=1600, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='archdeaconry'))
        FeatureCode.objects.filter(feature_type='archdeaconry').update(min_resolution=0, max_resolution=1600, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='deanery'))
        FeatureCode.objects.filter(feature_type='deanery').update(min_resolution=0, max_resolution=1600, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='parish'))
        FeatureCode.objects.filter(feature_type='parish').update(min_resolution=0, max_resolution=1600, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='site_boundary'))
        FeatureCode.objects.filter(feature_type='site_boundary').update(min_resolution=0, max_resolution=1600, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='ward'))
        FeatureCode.objects.filter(feature_type='ward').update(min_resolution=0, max_resolution=1600, type='vector')
        group.feature_codes.add(FeatureCode.objects.get(feature_type='section'))
        FeatureCode.objects.filter(feature_type='section').update(min_resolution=0, max_resolution=1600, type='vector')
        
        group = FeatureGroup.objects.create(group_code='base', display_name='base', 
            switch_on_off=False, initial_visibility=True, hierarchy=0)
        group.feature_codes.add(FeatureCode.objects.get_or_create(feature_type='base', display_name='Base', min_resolution=0, max_resolution=1600, show_in_toolbar=False)[0])
        FeatureCode.objects.filter(feature_type='base').update(min_resolution=0, max_resolution=1600, type='raster', show_in_toolbar=False)
        

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150909_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('group_code', models.CharField(max_length=20)),
                ('display_name', models.CharField(max_length=20)),
                ('hierarchy', models.IntegerField()),
                ('initial_visibility', models.BooleanField(default=False)),
                ('switch_on_off', models.BooleanField(default=True)),
                ('feature_codes', models.ManyToManyField(to='main.FeatureCode')),
            ],
            options={
            },
            bases=(models.Model,),
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
            field=models.CharField(max_length=20, default=''),
            preserve_default=False,
        ),
        migrations.RunPython(
            code=populate_feature_codes,
            reverse_code=None,
            atomic=True,
        ),
        migrations.RemoveField(
            model_name='burialgroundsite',
            name='aws_media_bucket',
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='key_expires',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
