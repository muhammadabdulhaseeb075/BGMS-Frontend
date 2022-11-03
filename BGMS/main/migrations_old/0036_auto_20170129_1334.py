# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, connection

def migrate_featuregroups_featurecodes(apps, schema_editor):
    FeatureCode = apps.get_model("main", "FeatureCode")
    FeatureGroup = apps.get_model("main", "FeatureGroup")
    gFeatureCode = apps.get_model("geometriespublic", "FeatureCode")
    gFeatureGroup = apps.get_model("geometriespublic", "FeatureGroup")

    if connection.schema_name == 'public':
        for fg in FeatureGroup.objects.all():
            gfg = gFeatureGroup(id=fg.id, group_code=fg.group_code, display_name=fg.display_name, switch_on_off=fg.switch_on_off, initial_visibility=fg.initial_visibility, hierarchy=fg.hierarchy)
            gfg.save()
            for fg_fc in fg.feature_codes.all():
                gfg.feature_codes.add(gFeatureCode.objects.get(id=fg_fc.id))
            

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_auto_20170129_1318'),
    ]

    operations = [
        migrations.RunPython(
            code=migrate_featuregroups_featurecodes,
            reverse_code=None,
        )
    ]
