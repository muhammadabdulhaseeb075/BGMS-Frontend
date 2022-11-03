# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, connection
import datetime


def create_feature_code(apps, schema_editor):
    NewFeatureCode = apps.get_model("main", "FeatureCode")
    if connection.schema_name == 'public':
        if not NewFeatureCode.objects.all().exists():
            feature_names = [{'type':'war_grave', 'display_string':'War Grave'}, 
                             {'type':'war_memorial', 'display_string':'War Memorial'}, 
                             {'type':'pavestone', 'display_string':'Pavestone'}, 
                             {'type':'plaque', 'display_string':'Plaque'},
                             {'type':'statue', 'display_string':'Statue'}, 
                             {'type':'table_tomb', 'display_string':'Table Tomb'}, 
                             {'type':'window', 'display_string':'Window'}, 
                             {'type':'gravestone', 'display_string':'Gravestone'}, 
                             {'type':'plot', 'display_string':'Plot'}, 
                             {'type':'bound_plot', 'display_string':'Bound Plot'}, 
                             {'type':'tree', 'display_string':'Tree'}, 
                             {'type':'bush', 'display_string':'Bush/Shrub'}, 
                             {'type':'tree_canopy', 'display_string':'Tree Canopy'}, 
                             {'type':'manhole', 'display_string':'Manhole'}, 
                             {'type':'gully', 'display_string':'Gully'}, 
                             {'type':'inspection_cover', 'display_string':'Inspection Cover'}, 
                             {'type':'utility_pole', 'display_string':'Utility Pole'}, 
                             {'type':'wall', 'display_string':'Wall'}, 
                             {'type':'hedge', 'display_string':'Hedge'}, 
                             {'type':'fence', 'display_string':'Fence'}, 
                             {'type':'gate', 'display_string':'Gate'}, 
                             {'type':'path', 'display_string':'Path'}, 
                             {'type':'bridge', 'display_string':'Bridge'}, 
                             {'type':'road', 'display_string':'Road'}, 
                             {'type':'car_park', 'display_string':'Car Park'}, 
                             {'type':'grass', 'display_string':'Grass'}, 
                             {'type':'water', 'display_string':'Water'}, 
                             {'type':'recreation', 'display_string':'Recreation'}, 
                             {'type':'planting', 'display_string':'Planting'}, 
                             {'type':'woodland', 'display_string':'Woodland'}, 
                             {'type':'building', 'display_string':'Building'}, 
                             {'type':'steps', 'display_string':'Steps'}, 
                             {'type':'tank', 'display_string':'Tank'}, 
                             {'type':'mausoleum', 'display_string':'Mausoleum'}, 
                             {'type':'bench', 'display_string':'Bench'}, 
                             {'type':'sign', 'display_string':'Sign'}, 
                             {'type':'bollard', 'display_string':'Bollard'},
                             {'type':'bin', 'display_string':'Bin'}, 
                             {'type':'lamppost', 'display_string':'Lamppost'}, 
                             {'type':'diocese', 'display_string':'Diocese'}, 
                             {'type':'archdeaconry', 'display_string':'Archdeaconry'}, 
                             {'type':'deanery', 'display_string':'Deanery'}, 
                             {'type':'parish', 'display_string':'Parish'}, 
                             {'type':'ward', 'display_string':'Ward'}, 
                             {'type':'section', 'display_string':'Section'}]
            for name in feature_names:
                NewFeatureCode.objects.create(feature_type=name['type'], display_name=name['display_string'])
                
                
def undo_move_feature_code(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_squashed_0034_auto_20150805_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('feature_type', models.CharField(max_length=20)),
                ('display_name', models.CharField(max_length=20))
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(
            code=create_feature_code,
            reverse_code=undo_move_feature_code,
            atomic=True,
        ),
        migrations.CreateModel(
            name='Surveyor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('surveyor_name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='imagetype',
            name='image_type',
            field=models.CharField(unique=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='registereduser',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 8, 26)),
            preserve_default=True,
        ),
    ]
