from django.conf import settings
from django.contrib.gis.db import models
from django.db.models.query import QuerySet
from django.utils import timezone

"""
Abstract base classes to be used with models throughout BGMS
"""

class CreatedEditedFields(models.Model):
    """
    Abstract base model for created and modified fields.
    null=True for prexisting models that do not already have these fields.
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_created_by")
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    last_edit_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="%(app_label)s_%(class)s_last_edit_by")
    last_edit_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        """
        Soft delete an entire queryset
        """
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        """
        Hard delete an entire queryset
        """
        return super(SoftDeletionQuerySet, self).delete()

    def not_deleted(self):
        return self.filter(deleted_at=None)

    def deleted(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    """
    Makes delete() a soft delete.
    Actual delete can be performed with hard_delete.

    Normal querysets will not included deleted records.
    Can be included by using all_objects rather than objects.
    """

    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        """
        Soft delete an object
        """
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """
        Hard delete an object
        """
        super(SoftDeletionModel, self).delete()