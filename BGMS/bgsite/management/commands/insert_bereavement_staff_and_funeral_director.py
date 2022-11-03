import csv
import os
import sys

from django.core.management.base import BaseCommand
from django.db import transaction, connection

from main.models import SiteGroup, BurialGroundSite
from django.contrib.auth.models import Group

''' Adds BereavementStaff and FuneralDirector auth groups '''

''' Run using : 'python manage.py insert_bereavement_staff_and_funeral_director' '''

class Command(BaseCommand):
    def handle(self, *args, **options):

        try:
            Group.objects.get_or_create(name='BereavementStaff')
            Group.objects.get_or_create(name='FuneralDirector')

        except Exception as e:
            print('\n')
            print(e)