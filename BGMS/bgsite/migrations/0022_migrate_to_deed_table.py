# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models, connection
from django.db.models import Q
import main.validators


def move_deed(apps, schema_editor):

    if connection.schema_name != 'public':
        
        GravePlot = apps.get_model("bgsite", "GravePlot")
        GraveDeed = apps.get_model("bgsite", "GraveDeed")
        
        # get all graveplots that contain deed information
        graveplot_with_deed = GravePlot.objects.filter(Q(cost_currency__isnull=False) | Q(cost_unit__isnull=False) | Q(cost_subunit__isnull=False)
        | Q(cost_subunit2__isnull=False) | Q(purchase_date__isnull=False) | Q(impossible_date_day__isnull=False) | Q(impossible_date_month__isnull=False)
        | Q(impossible_date_year__isnull=False) | Q(tenure_years__isnull=False))
        
        for graveplot in graveplot_with_deed:
            try:
                # create deed record
                deed,created = GraveDeed.objects.get_or_create(graveplot=graveplot)
                
                # populate deed record using field from graveplot
                deed.cost_currency = graveplot.cost_currency
                deed.cost_unit = graveplot.cost_unit
                deed.cost_subunit = graveplot.cost_subunit
                deed.cost_subunit2 = graveplot.cost_subunit2
                deed.purchase_date = graveplot.purchase_date
                deed.impossible_purchase_date = graveplot.impossible_date
                deed.purchase_date_day = graveplot.impossible_date_day
                deed.purchase_date_month = graveplot.impossible_date_month
                deed.purchase_date_year = graveplot.impossible_date_year
                deed.tenure_years = graveplot.tenure_years
                    
                deed.save()
            except:
                continue

class Migration(migrations.Migration):

    dependencies = [
        ('bgsite', '0021_auto_20190221_1138'),
    ]

    operations = [
        migrations.RunPython(
            code=move_deed,
            reverse_code=None,
            atomic=True,
        ),
    ]
