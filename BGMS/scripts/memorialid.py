from main.models import BurialGroundSite
from bgsite.models import Memorial
from django.db import connection

def run():
    bgss = BurialGroundSite.objects.exclude(schema_name='public')
    for bgs in bgss:
        connection.schema_name = bgs.schema_name
        print("Running Schema: " + bgs.schema_name)
        mems = Memorial.objects.filter(feature_id=None)
        print(mems.count())
        for mem in mems:
            mem.save()