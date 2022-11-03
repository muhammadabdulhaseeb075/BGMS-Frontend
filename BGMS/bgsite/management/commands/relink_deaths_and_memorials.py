import csv
import os
import sys
import traceback

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from bgsite.models import Death, Memorial, GravePlot

''' Run using : 'python manage.py tenant_command relink_deaths_and_memorials --schema=highgate' '''

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

        file_path = './bgsite/management/commands/highgate_linked_death_data.csv'

        with open(os.path.normpath(file_path), newline='') as csvfile:
        
            reader = csv.DictReader(csvfile)
            rows = list(reader)

            row_count = len(rows)
            
            for row_number, row in enumerate(rows):
                
                try:
                    death = Death.objects.get(person_id=row['death_id'])
                    death.memorials.add(Memorial.objects.get(topopolygon_id=row['memorial_topopolygon_id']))
                except:
                    pass

                progressBar(row_number+1, row_count)

    except Exception as e:
      print('\n')
      print(traceback.format_exc())