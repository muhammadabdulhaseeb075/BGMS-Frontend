from django.db.models.signals import post_delete
from django.dispatch import receiver
from bgsite.models import Image, Thumbnail


@receiver(post_delete, sender=Image)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    instance.url.delete()


@receiver(post_delete, sender=Thumbnail)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes image files on `post_delete` """
    instance.url.delete()
