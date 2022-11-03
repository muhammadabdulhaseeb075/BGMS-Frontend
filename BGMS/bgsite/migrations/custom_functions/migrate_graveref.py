from django.db import connection

'''** Note: if using this again, it will need modified as grave_number is now in GraveRef table **'''


def migrate_graveref(apps, schema_editor):

    if connection.schema_name != 'public':
        
        GravePlot = apps.get_model("bgsite", "GravePlot")
        GraveRef = apps.get_model("bgsite", "GraveRef")
        Burial = apps.get_model("bgsite", "Burial")
        
        graveplots = GravePlot.objects.all()
        
        for grave in graveplots:
        
            if grave.grave_number == '':
                grave.grave_number = None
        
            if grave.grave_number or grave.section:
            
                grave_ref = None

                if not grave.grave_number:
                    grave_ref_no_grave_number = GraveRef.objects.filter(grave_number=None, section=grave.section, subsection=grave.subsection)

                    if grave_ref_no_grave_number.exists() and hasattr(grave_ref_no_grave_number[0], 'graveref_graveplot'):
                        # if grave ref exists and is assigned to a graveplot already, create a new one
                        grave_ref = GraveRef.objects.create(grave_number=None, section=grave.section, subsection=grave.subsection)
                
                if not grave_ref:
                    grave_ref = GraveRef.objects.get_or_create(grave_number=grave.grave_number, section=grave.section, subsection=grave.subsection)[0]

                grave.graveref = grave_ref
                grave.save()
        
        burials = Burial.objects.exclude(grave_number__isnull=True).exclude(grave_number='')
        
        for burial in burials:
            if burial.grave_number:
                graveRef = GraveRef.objects.get_or_create(grave_number=burial.grave_number, section=None, subsection=None)[0]
                burial.graveref = graveRef
                burial.save()

def reverse_migrate_graveref(apps, schema_editor):

    if connection.schema_name != 'public':
        
        GraveRef = apps.get_model("bgsite", "GraveRef")
        
        GraveRef.objects.all().delete()