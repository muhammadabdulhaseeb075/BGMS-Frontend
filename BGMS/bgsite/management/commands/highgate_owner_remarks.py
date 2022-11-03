import csv
import os
import sys
import traceback

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from bgsite.models import GraveOwner
from main.models import PublicPerson, Company

''' Run using : 'python manage.py tenant_command highgate_owner_remarks --schema=highgate' '''

'''** Note: if using this again, it will need modified as grave_number is now in GraveRef table **'''

def progressBar(value, endvalue, grave_number, bar_length=80):

  percent = float(value) / endvalue
  arrow = '-' * int(round(percent * bar_length)-1) + '>'
  spaces = ' ' * (bar_length - len(arrow))

  sys.stdout.write("\rPercent: [{0}] {1}% Grave Number: {2}".format(arrow + spaces, int(round(percent * 100)), grave_number))
  sys.stdout.flush()

class Command(BaseCommand):
  def handle(self, *args, **options):

    try:
      with transaction.atomic():
        
        header = None

        file_path = './bgsite/management/commands/highgate_owners.csv'

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
              continue
            else:
              rowDict = dict(zip(header, row))
            
            day = rowDict.get('day') if rowDict.get('day') else 0
            month = rowDict.get('month') if rowDict.get('month') else 0
              
            graveowners = GraveOwner.objects.filter(deed__graveplot__grave_number=rowDict.get('grave'), 
              owner_from_date_day=day, owner_from_date_month=month, owner_from_date_year=rowDict.get('year'))
          
            found = False
           
            for owner in graveowners:
              try:
                person = PublicPerson.objects.get(id=owner.object_id)
                name = person.first_names
              except:
                company = Company.objects.get(id=owner.object_id)
                name = company.name
            
              if name in rowDict.get('name'):
                owner.remarks = rowDict.get('remarks')
                owner.save()
                found = True

            if not found:
              print(' - ')
              print(day)
              print(month)
              raise(Exception('Cannot find graveowner for row number: ' + str(row_number) + '. Graveowners.count: ' + str(graveowners.count())))

            progressBar(row_number, row_count, rowDict.get('grave'))

    except Exception as e:
      print('\n')
      print(traceback.format_exc())