import csv
import os
import sys

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from bgsite.models import Burial
from main.models import BurialGroundSite

''' Adds a defined layer to each site that doesn't already have it '''

''' Run using : 'python manage.py select_from_all_sites' '''

class Command(BaseCommand):
  def handle(self, *args, **options):

    try:
        sites = BurialGroundSite.objects.exclude(schema_name='public')
        
        for site in sites:

            connection.schema_name = site.schema_name

            burials = Burial.objects.exclude(situation__isnull = True).exclude(situation = '')
            
            if burials.exists():
                for burial in burials:
                    print(site.schema_name + ' - ' + str(burial.id))

    except Exception as e:
      print('\n')
      print(e)