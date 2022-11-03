from main.models import BurialGroundSite, ImageType
from django.db import connection
from filemanager.models import File
import boto
from django.conf import settings
from geometries.models import TopoPolygons

def run():
    connection.schema_name = "public"
    ImageType.objects.update_or_create(image_type='pdf')

    # d79cc9d6-76fe-4a4a-9681-94f3395c3f77  local
    # d79cc9d6-76fe-4a4a-9681-94f3395c3f77  demosite

    files_urls = [{'filename': 'd79cc9d6-76fe-4a4a-9681-94f3395c3f77-building.pdf', 'file_type':'pdf', 'name':'Building plans', 'feature_uuid':'d79cc9d6-76fe-4a4a-9681-94f3395c3f77','schema_name': 'demosite'}, {'filename': 'd79cc9d6-76fe-4a4a-9681-94f3395c3f77-floor.pdf', 'file_type':'pdf', 'name':'Floor plans', 'feature_uuid':'d79cc9d6-76fe-4a4a-9681-94f3395c3f77','schema_name': 'demosite'},
    {'filename': '65dedc7e-9e8f-4f7e-8889-d911ed9a50f2-building.pdf', 'file_type':'pdf', 'name':'Building plans', 'feature_uuid':'65dedc7e-9e8f-4f7e-8889-d911ed9a50f2','schema_name': 'dalstondemo'}, {'filename': '65dedc7e-9e8f-4f7e-8889-d911ed9a50f2-floor.pdf', 'file_type':'pdf', 'name':'Floor plans', 'feature_uuid':'65dedc7e-9e8f-4f7e-8889-d911ed9a50f2','schema_name': 'dalstondemo'},
    {'filename': 'd79cc9d6-76fe-4a4a-9681-94f3395c3f77-building.pdf', 'file_type':'pdf', 'name':'Building plans', 'feature_uuid':'d79cc9d6-76fe-4a4a-9681-94f3395c3f77','schema_name': 'caldbeckdemo'}, {'filename': 'd79cc9d6-76fe-4a4a-9681-94f3395c3f77-floor.pdf', 'file_type':'pdf', 'name':'Floor plans', 'feature_uuid':'d79cc9d6-76fe-4a4a-9681-94f3395c3f77','schema_name': 'caldbeckdemo'}]
    # files_urls = [{'filename': 'd79cc9d6-76fe-4a4a-9681-94f3395c3f77.pdf', 'file_type':'pdf', 'name':'Building plans', 'feature_uuid':'d79c09d6-76fe-4a4a-9681-94f3395c3f77','schema_name': 'caldbeck'}, {'filename': 'd79cc9d6-76fe-4a4a-9681-94f3395c3f77.pdf', 'file_type':'pdf', 'name':'Floor plans', 'feature_uuid':'d79cc9d6-76fe-4a4a-9681-94f3395c3f77','schema_name': 'caldbeck'},
    # {'filename': 'd79cc9d6-76fe-4a4a-9681-94f3395c3f77-building.pdf', 'file_type':'pdf', 'name':'Building plans', 'feature_uuid':'d79cc9d6-76fe-4a4a-9681-94f3395c3f77','schema_name': 'caldbeck'}, {'filename': 'd79cc9d6-76fe-4a4a-9681-94f3395c3f77-floor.pdf', 'file_type':'pdf', 'name':'Floor plans', 'feature_uuid':'d79cc9d6-76fe-4a4a-9681-94f3395c3f77','schema_name': 'caldbeck'}]


    if len(files_urls) != 0:
        bgss = BurialGroundSite.objects.exclude(schema_name='public')
        for bgs in bgss:
            connection.schema_name = bgs.schema_name
            print("Creating 'files' folder for " + bgs.schema_name)
            #create folder structure media bucket
            conn = boto.connect_s3()
            bucket = conn.get_bucket(settings.AWS_MEDIA_BUCKET_NAME)
            k = bucket.new_key(bgs.schema_name +'/files/')
            k.set_contents_from_string('')
        
        for fu in files_urls:
            if len(BurialGroundSite.objects.filter(schema_name=fu['schema_name'])) > 0:
                connection.schema_name = fu['schema_name']
                if len(TopoPolygons.objects.filter(id=fu['feature_uuid'])) > 0:
                    tp = TopoPolygons.objects.get(id=fu['feature_uuid'])
                else:
                    tp = None
                f = File.objects.get_or_create(url="".join([fu['schema_name'],'/files/',fu['filename']]),file_type=ImageType.objects.get(image_type=fu['file_type']),name=fu['name'], topopolygon=tp)

                print('file added: '+fu['filename'])

    print("Script finished successfully!")