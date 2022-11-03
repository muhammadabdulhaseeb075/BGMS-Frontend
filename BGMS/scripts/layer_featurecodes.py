from main.models import BurialGroundSite
from django.db import connection
from django.conf import settings
from geometries.models import Layer
from geometriespublic.models import FeatureCode

def run():
    bgss = BurialGroundSite.objects.exclude(schema_name='public')
    for bgs in bgss:
        connection.schema_name = bgs.schema_name
        for lyr in Layer.objects.all():
            lyr.feature_code = FeatureCode.objects.get(id=lyr.feature_code_idfk)
            lyr.save()

    print("Script finished successfully!")