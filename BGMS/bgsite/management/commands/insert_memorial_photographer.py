import csv
import os
import sys

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from main.models import SiteGroup, BurialGroundSite
from django.contrib.auth.models import Group

''' Adds MemorialPhotographer auth group and adds group to each site '''

''' Run using : 'python manage.py insert_memorial_photographer' '''

class Command(BaseCommand):
  def handle(self, *args, **options):

    try:
        group,created = Group.objects.get_or_create(name='MemorialPhotographer')
        sites = BurialGroundSite.objects.all()
        
        for site in sites:
            if site.site_details_id:
                SiteGroup.objects.get_or_create(burialgroundsite=site, group=group)

    except Exception as e:
      print('\n')
      print(e)