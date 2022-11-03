import csv
import os
import sys
import traceback

from django.core.management.base import BaseCommand
from django.db import transaction, connection
from django.db.models import Q

from bgsite.models import Section, GravePlot
from django.contrib.auth.models import Group

''' Removes leading and trailing spaces from section names for Highgate '''

''' Run using : 'python manage.py tenant_command remove_leading_trailing_spaces_from_sections --schema=highgate' '''

class Command(BaseCommand):
  def handle(self, *args, **options):

    try:
        sections = Section.objects.filter(Q(section_name__startswith=" ") | Q(section_name__endswith=" "))
        
        for section in sections:
            # change to section without spaces
            section_name_no_spaces = section.section_name.strip()
            new_section,created = Section.objects.get_or_create(section_name=section_name_no_spaces)
            graveplots = GravePlot.objects.filter(section=section).update(section=new_section)
            
            # delete section with spaces which should be no longer in use
            section.delete()

    except Exception as e:
        print(traceback.format_exc())