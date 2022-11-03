from main.models import BurialGroundSite
from bgsite.models import Burial, GravePlot
from django.db import connection
from django.db import transaction

def run():
    """
    Move consecrated field from Burial to GravePlot
    """
    bgss = BurialGroundSite.objects.exclude(schema_name='public')
    
    try:
        with transaction.atomic():
            for bgs in bgss:
                connection.schema_name = bgs.schema_name
                print("Running Schema: " + bgs.schema_name)
                
                graves = GravePlot.objects.all()
                
                for grave in graves:
                    if grave.consecrated is None:
                        burials = Burial.objects.filter(graveplot = grave)
                        
                        for burial in burials:
                            if not grave.consecrated:
                                if burial.consecrated:
                                    grave.consecrated = True
                                    grave.save()
                                    break
                                elif burial.consecrated == False:
                                    # set to false but keep looking for consecrated
                                    grave.consecrated = False
                                    grave.save()
                
                Burial.objects.all().update(consecrated=None)
                        
    except Exception as e:
        print(e)