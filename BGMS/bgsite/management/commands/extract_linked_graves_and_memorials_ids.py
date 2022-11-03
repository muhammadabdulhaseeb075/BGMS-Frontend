import csv
import os
import sys
import traceback

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from bgsite.models import MemorialGraveplot

''' Run using : 'python manage.py tenant_command extract_linked_graves_and_memorials_ids --schema=highgate' '''

'''** Note: if using this again, it will need modified as grave_number is now in GraveRef table **'''

def progressBar(value, endvalue, bar_length=80):

  percent = float(value) / endvalue
  arrow = '-' * int(round(percent * bar_length)-1) + '>'
  spaces = ' ' * (bar_length - len(arrow))

  sys.stdout.write("\rPercent: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
  sys.stdout.flush()

class Command(BaseCommand):
  def handle(self, *args, **options):

    try:
      with transaction.atomic():
      
        mgs = MemorialGraveplot.objects.all()
        row_count = mgs.count()
        row_number = 0
        
        fieldnames = ['memorial_topopolygon_id', 'grave_number']

        file_path = './bgsite/management/commands/highgate_linked_data.csv'

        with open(os.path.normpath(file_path), 'w', newline='') as csvfile:
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for mg in mgs:
            
                row_number += 1
                
                writer.writerow({'memorial_topopolygon_id': mg.memorial.topopolygon_id, 'grave_number': mg.graveplot.grave_number})

                progressBar(row_number, row_count)

    except Exception as e:
      print('\n')
      print(traceback.format_exc())