import sys
import traceback
import calendar

from django.core.management.base import BaseCommand

from bgsite.models import GraveOwner
from BGMS.utils import date_elements_to_full_date

''' GraveOwner - populates active_owner field and removes ownership_order '''

''' Run using : 'python manage.py tenant_command highgate_ownership_order_to_active_owner --schema=highgate' '''

class Command(BaseCommand):
  def handle(self, *args, **options):

    try:
        owners = GraveOwner.objects.filter(ownership_order__isnull=False).order_by('deed_id','ownership_order')
        total = owners.count()
        count = 0
        
        for owner in owners:
            # find owner of same deed with higher ownership order
            next_owners = GraveOwner.objects.filter(deed_id=owner.deed_id, ownership_order=owner.ownership_order+1)
            
            if next_owners.exists():
                owner.active_owner = False
                
                next_owner = next_owners[0]
                
                # create 'to' date which is day before the next owners 'from' date
                if next_owner.owner_from_date_day and next_owner.owner_from_date_month and next_owner.owner_from_date_year:

                    to_day = next_owner.owner_from_date_day
                    to_month = next_owner.owner_from_date_month
                    to_year = next_owner.owner_from_date_year

                    if (not owner.owner_from_date_day == to_day) and (not owner.owner_from_date_month == to_month) and (not owner.owner_from_date_year == to_year):
                        if next_owner.owner_from_date_day == 1:
                            if next_owner.owner_from_date_month == 1:
                                to_month = 12
                                to_year = next_owner.owner_from_date_year - 1
                            else:
                                to_month = next_owner.owner_from_date_month - 1
                            
                            if (to_month == 1 or to_month == 3 or to_month == 5 or to_month == 7 or to_month == 8 or to_month == 10 or to_month == 12):
                                to_day = 31
                            elif (to_month == 4 or to_month == 6 or to_month == 9 or to_month == 11):
                                to_day = 30
                            elif to_month == 2 and calendar.isleap(int(to_year)):
                                to_day = 29
                            elif to_month == 2 and not calendar.isleap(int(to_year)):
                                to_day = 28
                        else:
                            to_day = next_owner.owner_from_date_day - 1

                    to_full_date,to_impossible_date = date_elements_to_full_date(to_day, to_month, to_year)

                    owner.owner_to_date = to_full_date
                    owner.impossible_owner_to_date = to_impossible_date
                    owner.owner_to_date_day = to_day
                    owner.owner_to_date_month = to_month
                    owner.owner_to_date_year = to_year

            else:
                owner.active_owner = True
            
            # remove ownership_order data
            #owner.ownership_order = None
            
            owner.save()
            
            count+=1
            print ('Owner ' + str(count) + ' of ' + str(total))

    except Exception as e:
        print(traceback.format_exc())