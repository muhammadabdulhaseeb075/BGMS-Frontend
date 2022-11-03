# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def populate_featurecode_reserved_plot(apps, schema_editor):
    FeatureCode = apps.get_model("main", "FeatureCode")
    FeatureGroup = apps.get_model("main", "FeatureGroup")
    Layer = apps.get_model("geometries", "Layer")

    if connection.schema_name != 'public':
        name = {'feature_type':'reserved_plot','display_name':'Reserved','type':'vector','min_resolution':0,'max_resolution':0.5,'show_in_toolbar':True}
        fc, created = FeatureCode.objects.update_or_create(feature_type=name['feature_type'], defaults={'display_name':name['display_name'],'type':name['type'],'min_resolution':name['min_resolution'],'max_resolution':name['max_resolution'], 'show_in_toolbar':name['show_in_toolbar']})
        g = FeatureGroup.objects.get(group_code='plots')
        g.feature_codes.add(fc)
        g.save()

        Layer.objects.update_or_create(feature_code=fc, defaults={'initial_visibility':True, 'display_name':fc.display_name, 'show_in_toolbar':fc.show_in_toolbar})

class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0031_auto_20160714_0945'),
    ]

    operations = [
        migrations.RunPython(
            code=populate_featurecode_reserved_plot,
            reverse_code=None,
        )
    ]
