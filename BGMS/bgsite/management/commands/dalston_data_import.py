import csv
import os
import sys

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from bgsite.models import Burial, Section, Subsection, GravePlot

''' Run using : 'python manage.py tenant_command dalston_data_import --schema=dalston' '''

'''** Note: if using this again, it will need modified as grave_number is now in GraveRef table **'''

def progressBar(value, endvalue, burial_number, bar_length=80):

  percent = float(value) / endvalue
  arrow = '-' * int(round(percent * bar_length)-1) + '>'
  spaces = ' ' * (bar_length - len(arrow))

  sys.stdout.write("\rPercent: [{0}] {1}% BN: {2}".format(arrow + spaces, int(round(percent * 100)), burial_number))
  sys.stdout.flush()

class Command(BaseCommand):
  def handle(self, *args, **options):

    try:
      with transaction.atomic():
        
        header = None

        #file_path = '//AG-FS01/AGI/Technical/Data/Dalston/records.csv'
        file_path = 'C:/Users/psimpson/Documents/BGMS/Dalston/records.csv'

        with open(os.path.normpath(file_path), newline='') as csvfile:
          reader = csv.reader(csvfile, dialect='excel', delimiter=',')
          row_count = sum(1 for row in reader)
          # back to start of csv file
          csvfile.seek(0)

          burials_with_modified_grave = 0
          burials_with_created_grave = 0
          burials_with_no_grave = 0
          row_number = 0
          burials_do_not_exist = []
          duplicate_graveplot = []
          
          for row in reader:
            row_number += 1

            if not row:
              # i.e. blank row
              continue
            
            if not header:
              header = row
            else:
              rowDict = dict(zip(header, row))

              burial_record_qs = Burial.objects.extra(where=["REPLACE(burial_number,' ','') = '" + rowDict.get('burialregisterentryno') + "'"]).select_related('graveplot')

              if rowDict.get('burialregisterentryno') == '':
                continue
              elif len(burial_record_qs) > 0:

                burial_record = burial_record_qs[0]

                burial_record.register = rowDict.get('book_no')
                burial_record.register_page = rowDict.get('page_no')
                burial_record.registration_number = rowDict.get('burialregisterentryno')

                # get section and subsection objects
                section = None
                subsection = None

                if rowDict.get('ward'):
                  try:
                    section = Section.objects.get(section_name=rowDict.get('ward'))
                  except:
                    section = Section.objects.create(section_name=rowDict.get('ward'), created_by_id=4)

                  # subsection can only exist if section also exists
                  if rowDict.get('section'):
                    try:
                      subsection = Subsection.objects.get(subsection_name=rowDict.get('section'), section=section)
                    except:
                      subsection = Subsection.objects.create(subsection_name=rowDict.get('section'), section=section, created_by_id=4)

                if not rowDict.get('grave'):
                  ''' Burial does not have grave number, hence we don't need to do anything '''
                  burials_with_no_grave += 1

                elif burial_record.graveplot:
                  ''' Burial has a graveplot. Edit it. '''
                  graveplot_record = burial_record.graveplot
                  graveplot_record.grave_number = rowDict.get('grave')

                  if rowDict.get('ward'):
                    graveplot_record.section = section

                    # subsection can only exist if section also exists
                    if rowDict.get('section'):
                      graveplot_record.subsection = subsection

                  try:
                    with transaction.atomic():
                      graveplot_record.save()
                      burials_with_modified_grave += 1
                  except:
                    duplicate_graveplot.append("Burial linked to a graveplot with a duplicate grave_number/section/subsection. id: " + rowDict.get('id') + " burialregisterentryno: " + rowDict.get('burialregisterentryno'))

                else:
                  ''' Burial does not have a graveplot. Search for existing or create one (with no geometry). '''

                  graveplot_record,created = GravePlot.objects.get_or_create(
                      grave_number=rowDict.get('grave'), section=section, subsection=subsection)
                  
                  if created:
                    burials_with_created_grave += 1
                  else:
                    burials_with_modified_grave += 1
                    
                  #link to burial record
                  burial_record.graveplot = graveplot_record
                  
                burial_record.save()
                
                # add consecrated data if needed
                if rowDict.get('inconsecratedground') and not graveplot_record.consecrated is None:
                  if rowDict.get('inconsecratedground') == 'y':
                    graveplot_record.consecrated = True
                  elif rowDict.get('inconsecratedground') == 'n':
                    graveplot_record.consecrated = False
                  graveplot_record.save()

              else:
                burials_do_not_exist.append("Burial does not exist. id: " + rowDict.get('id') + " burialregisterentryno: " + rowDict.get('burialregisterentryno'))
            
              progressBar(row_number, row_count, rowDict.get('burialregisterentryno'))
          
          # print list of burials that were not found in database
          if len(burials_do_not_exist) > 0:
            print('\n')

            for burial in burials_do_not_exist:
              print(burial)
            print('Total: ' + str(len(burials_do_not_exist)))
          
          # print list of burials with duplicate graveplots
          if len(duplicate_graveplot) > 0:
            print('\n')

            for burial in duplicate_graveplot:
              print(burial)
            print('Total: ' + str(len(duplicate_graveplot)))

          print('\nBurials with modified grave: ' + str(burials_with_modified_grave))
          print('Burials with created grave: ' + str(burials_with_created_grave))
          print('Burials with no linked grave: ' + str(burials_with_no_grave))

          raise Exception('Changes not commited')

    except Exception as e:
      print('\n')
      print(e)