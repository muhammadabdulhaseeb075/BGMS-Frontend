import csv
import os
import sys
import traceback

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from bgsite.models import Death

''' Run using : 'python manage.py tenant_command extract_and_delete_linked_deaths_and_memorials_ids --schema=highgate' '''

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
      
        deaths = Death.objects.exclude(memorials=None)
        row_count = deaths.count()
        row_number = 0
        
        fieldnames = ['memorial_topopolygon_id', 'death_id']

        file_path = './bgsite/management/commands/highgate_linked_death_data.csv'

        with open(os.path.normpath(file_path), 'w', newline='') as csvfile:
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for death in deaths:
            
                row_number += 1
                
                for memorial in death.memorials.all():
                
                    writer.writerow({'memorial_topopolygon_id': memorial.topopolygon_id, 'death_id': death.person_id})
                    
                    # remove relationship
                    death.memorials.remove(memorial)

                progressBar(row_number, row_count)

    except Exception as e:
      print('\n')
      print(traceback.format_exc())