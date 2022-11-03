import os
from django.db import connection
from uwsgidecorators import *
import copy
import datetime
import traceback
from django.utils import timezone

# minute, hour, day, month, weekday
# @cron(40, 2, -1, -1, -1)
@cron(42, 14, -1, -1, -1)
def delete_non_verified_users(num):
    '''
    Delete users that didnt verify their email account after 48 hours
    '''

    from main.models import BGUser

    end_date = datetime.datetime.now()
    print('delete_non_verified_users: ' + str(end_date))
    print(num)
    BGUser.objects.filter(registereduser__key_expires__lte=end_date,registereduser__isMailVerified=False).delete()
    print('delete_non_verified_users: FIN')


@cron(40, 9, -1, -1, -1)
def reset_actioned_requests(num):
    # If an "Actioned" request has a date_update attribute which is in the
    # past by more than PASSWORD_RESET_TIMEOUT_DAYS days, make that request
    # "Open" again.
    from main.models import UserPasswordRequests
    from django.conf import settings

    time = timezone.now()

    print("reset_actioned_requests: (at %s, SIGNAL=%r)" % (str(time), num))

    for task in UserPasswordRequests.objects.filter(status="Actioned"):
        age = (time - task.date_update).days
        if age >= settings.PASSWORD_RESET_TIMEOUT_DAYS:
            # This is now outdated. Set status back to "Open".
            task.set_status("Open")
            print("Task for user %s is too old. Reset." % task.user.email)

    print("reset_actioned_requests: FIN")

@cron(0, 3, -1, -1, -1)
def refresh_layer_cache(num):

    from geometries.models import LayerCache, Layer
    from geometries.views import getLayer
    from main.models import BurialGroundSite
    from mapmanagement.views import getMemorials, getGraveplot

    sites = BurialGroundSite.objects.exclude(schema_name='public')

    print('refresh_layer_cache: ' + str(datetime.datetime.now()))

    for site in sites:
        connection.schema_name = site.schema_name

        try:
            # get list of layer ids
            layer_objs = LayerCache.objects.all()

            if layer_objs.exists():

                layer_ids = copy.copy(layer_objs.values_list('layer_id', flat=True))

                # remove the current cache
                LayerCache.objects.all().delete()

                for layer_id in layer_ids:
                    layer = Layer.objects.get(id=str(layer_id))
                    feature_type = layer.feature_code.feature_type

                    # reload the cache for this layer
                    if layer.feature_code.feature_groups.filter(group_code='memorials').exists() or feature_type == 'cluster':
                        getMemorials(feature_type)
                    elif feature_type == 'plot' or feature_type == 'available_plot':
                        getGraveplot(feature_type)
                    else:
                        getLayer(feature_type, True)

                print(site.schema_name + ": refreshed layer cache")

        except Exception as e:
            print("Error refreshing %s layer cache for site %s." % (feature_type, site.schema_name))
            print(traceback.format_exc())