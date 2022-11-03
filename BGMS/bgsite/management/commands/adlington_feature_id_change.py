import csv
import os
import sys
import traceback

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from bgsite.models import Memorial
from geometries.models import TopoPolygons, LayerCache

''' Run using : 'python manage.py tenant_command adlington_feature_id_change --schema=adlington' '''

def progressBar(value, endvalue, feature_id, bar_length=80):

  percent = float(value) / endvalue
  arrow = '-' * int(round(percent * bar_length)-1) + '>'
  spaces = ' ' * (bar_length - len(arrow))

  sys.stdout.write("\rPercent: [{0}] {1}% Feature ID: {2}".format(arrow + spaces, int(round(percent * 100)), feature_id))
  sys.stdout.flush()

class Command(BaseCommand):
  def handle(self, *args, **options):

    # delete cache to prevent excessive cache updates during this script
    LayerCache.objects.all().delete()
    print("Layer Cache deleted")

    try:
      with transaction.atomic():
        
        header = None

        file_path = './bgsite/management/commands/adlington_new_memorials_feature_ids.csv'

        with open(os.path.normpath(file_path), newline='') as csvfile:
          reader = csv.reader(csvfile, dialect='excel', delimiter=',')
          row_count = sum(1 for row in reader)
          # back to start of csv file
          csvfile.seek(0)

          row_number = 0
          
          for row in reader:
            row_number += 1

            if not row:
              # i.e. blank row
              continue
            
            if not header:
              header = row
            else:
              rowDict = dict(zip(header, row))
              
              if rowDict.get('topopolygon_id'):
                try:
                  memorial = Memorial.objects.get(topopolygon_id=rowDict.get('topopolygon_id'))
                  memorial.feature_id = rowDict.get('feature_id')
                  memorial.topopolygon.feature_id = rowDict.get('feature_id')
                  memorial.topopolygon.save()
                  memorial.save()
                except Exception as e:
                  try:
                    topopolygon = TopoPolygons.objects.get(id=rowDict.get('topopolygon_id'))
                    topopolygon.feature_id = rowDict.get('feature_id')
                    topopolygon.save()
                  except:
                    raise(Exception('TopoPolygon_id: ' + rowDict.get('topopolygon_id') + ' not found.'))

              progressBar(row_number, row_count, rowDict.get('feature_id'))

    except Exception as e:
      print('\n')
      print(traceback.format_exc())