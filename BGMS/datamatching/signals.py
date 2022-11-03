from django.contrib.auth.signals import user_logged_out
from django.db import connection
from django.dispatch import receiver

from datamatching.models import DataMatchingUser

@receiver(user_logged_out)
def checkout_memorial(sender, request, user, **kwargs):
    """
    Checkout the user from his in-use memorial.
    """
    current_schema = connection.schema_name
    #bugfix for error on logging out of main admin portal
    if current_schema!='public':
        DataMatchingUser.objects.get(id=user.id).set_memorial_viewed()