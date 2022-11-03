# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection

def delete_burial_officials(apps, schema_editor):
    # if connection.schema_name == 'public':
    #     cursor = connection.cursor()
    #     drop_official_type_query = """
    #         DELETE from main_burialofficialtype as d
    #         WHERE (official_type='Ceremony Performed By') OR
    #         (official_type='Ceremony Performed by') OR
    #         (official_type='Certificate Given By') OR
    #         (official_type='certificate issued by');
    #         """
    #     cursor.execute(drop_official_type_query)
    pass

def undo_delete_burial_officials(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        # ('main', '0021_auto_20160712_1139'),
    ]

    operations = [
        migrations.RunPython(
            code=delete_burial_officials,
            reverse_code=undo_delete_burial_officials,
            atomic=True,
        ),
    ]
