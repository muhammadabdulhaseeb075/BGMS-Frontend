'''
Created on 22 Jun 2016

@author: achickermane
'''

from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from dataentry.models import DataEntryUser, Table
from django.db import connection
from main.models import BurialGroundSite, BurialOfficialType
from django.db.models.signals import post_save, post_delete

@receiver(user_logged_out)
def checkout_image(sender, request, user, **kwargs):
    """
    Checkout the user from his in-use images.
    """
    current_schema = connection.schema_name
    #bugfix for error on logging out of main admin portal
    if current_schema!='public':
        DataEntryUser.objects.get(id=user.id).set_image_viewed()


@receiver(post_delete, sender=BurialOfficialType)
@receiver(post_save, sender=BurialOfficialType)
def update_columns(sender, **kwargs):
    """
    Update many-to-many columns on adding a new burial official type.
    """
    old_schema = connection.schema_name
    print(old_schema)
    sites = BurialGroundSite.objects.all()
    for site in sites:
        if site.schema_name!='public':
            connection.schema_name = site.schema_name
            print(connection.schema_name)
            Table.objects.get(modelname='Burial').update_columns()
    connection.schema_name = old_schema
    print(connection.schema_name)
