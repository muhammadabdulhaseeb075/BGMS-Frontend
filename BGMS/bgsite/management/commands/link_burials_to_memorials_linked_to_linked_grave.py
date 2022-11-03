import csv
import os
import sys
import traceback

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from bgsite.models import Death, Memorial, GravePlot

''' Run using : 'python manage.py tenant_command link_burials_to_memorials_linked_to_linked_grave --schema=chorley' '''

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
      
        memorials = Memorial.objects.all()

        row_count = memorials.count()
        row_number = 0
        
        for memorial in memorials:
            
            for grave in memorial.graveplot_memorials.all():
                for burial in grave.burials.all():
                    burial.death.memorials.add(memorial)

            row_number += 1
            progressBar(row_number, row_count)

    except Exception as e:
      print('\n')
      print(traceback.format_exc())