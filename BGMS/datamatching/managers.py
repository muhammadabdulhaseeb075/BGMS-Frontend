from django.db import models, transaction
from bgsite.models import Memorial
from main.models import ImageState

class MemorialStateQuerySet(models.QuerySet):

    def get_in_use(self):
        """"""
        return self.get_or_create(state='in_use')[0]

    def get_skipped(self):
        """"""
        return self.get_or_create(state='skipped')[0]

    def get_finished(self):
        """"""
        return self.get_or_create(state='finished')[0]

    def get_revisit(self):
        """"""
        return self.get_or_create(state='revisit')[0]

    def get_viewed(self):
        """After searching by file name the current memorial changed to viewed state"""
        return self.get_or_create(state='viewed')[0]

class DataMatchingMemorialQuerySet(models.QuerySet):

    def update_datamatching_memorials(self):
        """Gets memorials from bgsite memorials that haven't yet been added to the
        datamatching portal """
        with transaction.atomic():
            new_memorials = Memorial.objects.exclude(id__in=self.all().values('memorial_id')).exclude(images__isnull=True)
            if new_memorials.exists():
                for memorial in new_memorials:
                    self.create(memorial=memorial, state=ImageState.objects.get(image_state='unprocessed'))
                return True
            else:
                return False

    def get_unmatched_memorial(self, dmuser):
        """Gets an unmatched memorial which the user has never visited, or None if there are no
        unmatched memorials left which the user has not marked as """
        #getting memorials that are neither being processed nor skipped by the user
        unmatched_memorials = self.select_for_update().exclude(in_use=True).exclude(datamatchinguser=dmuser, datamatchinguser__memorialuserlink__skipped=True).filter(is_matched=False)
        if unmatched_memorials.exists():
            return unmatched_memorials.first()
        else:
            return None

#     def get_unmatched_memorial(self, dmuser):
#         """Gets an unmatched memorial which the user has never visited, or None if there are no
#         unmatched memorials left which the user has not marked as """
#         unmatched_memorials = self.select_for_update().exclude(in_use=True).exclude(datamatchinguser=dmuser, datamatchinguser__memorialuserlink__skipped=True).filter(is_matched=False)
#         if unmatched_memorials.exists():
#             return unmatched_memorials.first()
#         else:
#             return None


class MemorialUserLinkQuerySet(models.QuerySet):
    def create_in_use_link(self, dmmemorial, dmuser):
        if dmmemorial.in_use:
            raise(Exception('Memorial already in use.'))
        else:
            dmmemorial.set_in_use()
            dmmemorial.save()
        links = self.select_for_update().filter(datamatching_memorial=dmmemorial, datamatching_user=dmuser)
        if not links.exists():
            return self.select_for_update().create(datamatching_memorial=dmmemorial, datamatching_user=dmuser)
        else:
            return links.first()
