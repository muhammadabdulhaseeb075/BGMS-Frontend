from django_ses.signals import bounce_received, complaint_received
from django.dispatch import receiver


@receiver(bounce_received)
def bounce_handler(sender, *args, **kwargs):
    print("This is bounce email object")
    print(kwargs.get('mail_obj'))


@receiver(complaint_received)
def complaint_handler(sender, *args, **kwargs):
    print("This is complaint email object")
    print(kwargs.get('mail_obj'))