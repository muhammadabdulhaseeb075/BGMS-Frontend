import csv
import os
import sys

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from geometries.models import Layer
from main.models import BurialGroundSite

''' Adds a defined layer to each site that doesn't already have it '''

''' Run using : 'python manage.py insert_layer' '''

class Command(BaseCommand):
  def handle(self, *args, **options):

    try:
        sites = BurialGroundSite.objects.exclude(schema_name='public')
        feature_code_id = 78
        
        for site in sites:

            connection.schema_name = site.schema_name

            layer = Layer.objects.filter(feature_code_id=feature_code_id)
            
            if not layer.exists():
                Layer.objects.create(feature_code_id=feature_code_id, display_name='Plans', show_in_toolbar=False, initial_visibility=False, max_resolution=1600, min_resolution=0)

    except Exception as e:
      print('\n')
      print(e)