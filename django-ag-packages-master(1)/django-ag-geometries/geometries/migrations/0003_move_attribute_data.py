# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

import datetime


""" Moves existing attributes for all features to new structure """
def move_attributes(apps, schema_editor):

    if connection.schema_name != 'public':
        
        TopoPolygons = apps.get_model("geometries", "TopoPolygons")
        TopoPolylines = apps.get_model("geometries", "TopoPolylines")
        TopoPoints = apps.get_model("geometries", "TopoPoints")
        
        move_attributes_for_features(apps, TopoPolygons.objects.filter(attributes__isnull=False).all())
        move_attributes_for_features(apps, TopoPolylines.objects.filter(attributes__isnull=False).all())
        move_attributes_for_features(apps, TopoPoints.objects.filter(attributes__isnull=False).all())

def move_attributes_for_features(apps, features):
    
    FeatureAttributes = apps.get_model("geometries", "FeatureAttributes")
    ContentType = apps.get_model('contenttypes', 'ContentType')
    PublicAttribute = apps.get_model("geometriespublic", "PublicAttribute")
    
    try:
        Type = apps.get_model("geometriespublic", "AttributeType")
    except:
        Type = apps.get_model("geometriespublic", "FieldType")

    for feature in features:
        for attribute in feature.attributes.all():
            """ these attributes are now permanent columns """
            if attribute.attribute_name=='created_us' and attribute.attribute_value:
                feature.created_by = attribute.attribute_value
            elif attribute.attribute_name=='created_da' and attribute.attribute_value:
                feature.created_date = datetime.datetime.strptime(attribute.attribute_value, "%Y-%m-%d").date()
            elif attribute.attribute_name=='last_edite' and attribute.attribute_value:
                feature.last_edit_by = attribute.attribute_value
            elif attribute.attribute_name=='last_edi_1' and attribute.attribute_value:
                feature.last_edit_date = datetime.datetime.strptime(attribute.attribute_value, "%Y-%m-%d").date()
            elif attribute.attribute_name=='MAP_ACCURA' and attribute.attribute_value:
                feature.map_accura = attribute.attribute_value.lower() in ['yes', 'y', 'true']
            elif attribute.attribute_name=='SOURCE_ID' and attribute.attribute_value:
                feature.source_id = attribute.attribute_value
            elif attribute.attribute_name=='LABEL' and attribute.attribute_value:
                """ this attribute is now a public attribute """
                newattribute,created = PublicAttribute.objects.get_or_create(name="Label", type=Type.objects.get(name="char"))
                newattribute.feature_codes.add(feature.layer.feature_code)
                content_type = ContentType.objects.get(app_label='geometriespublic', model='publicattribute')
                new_feature_attributes = FeatureAttributes.objects.create(content_type=content_type, object_id=newattribute.id, char_value=attribute.attribute_value)
                feature.feature_attributes.add(new_feature_attributes)

            # remove attribute as it's successfully migrated
            feature.attributes.remove(attribute)
            
            feature.save()

class Migration(migrations.Migration):

    dependencies = [
        ('geometries', '0002_auto_20190409_1639'),
        ('geometriespublic', '0002_auto_20190409_1639'),
    ]

    operations = [
        migrations.RunPython(
            code=move_attributes,
            reverse_code=None,
            atomic=True,
        ),
    ]
