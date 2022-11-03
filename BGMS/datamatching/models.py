from django.db import models, transaction
from bgsite.models import Memorial
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.template.defaultfilters import default
from main.models import BGUser, ImageState
import uuid
from django.utils import timezone
from datamatching.managers import DataMatchingMemorialQuerySet,\
    MemorialUserLinkQuerySet, MemorialStateQuerySet
from django.db.models.fields import CharField

# Create your models here.

class MemorialState(models.Model):
    state = CharField(max_length=10)
    objects = MemorialStateQuerySet.as_manager()


class DataMatchingUser(BGUser):
    class Meta:
        proxy = True
        app_label = 'main'

    def set_in_use_memorial(self, current_memorial_id=None, forward=True, memorial=None):
        """Sets the given memorial as the current memorial for the user. If no memorial is given,
        it gets a random memorial and sets that as the current memorial."""
        if memorial and (memorial == self.get_in_use_memorial()):
            return memorial
        with transaction.atomic():
            if memorial is None:

                DataMatchingMemorial.objects.update_datamatching_memorials()

                # all memorials that are currently in use
                in_use_memorials = MemorialHistory.objects.filter(state=MemorialState.objects.get_in_use()).values('memorial')
                # memorials skipped by this user (except for the current memorial is it has just been skipped)
                skipped_memorials = MemorialHistory.objects.filter(state=MemorialState.objects.get_skipped(), user=self).exclude(memorial_id=current_memorial_id).values('memorial')

                available_memorials = DataMatchingMemorial.objects.exclude(state=ImageState.objects.get(image_state='processed')).exclude(memorial__in=in_use_memorials).exclude(memorial__in=skipped_memorials).order_by('memorial__feature_id')
                
                if available_memorials.exists():
                    memorial = available_memorials.first()

                    # if user has a current memorial, then move on to the next (or prev if forward is False)
                    if current_memorial_id:
                        current_found = False
                        
                        for index, item in enumerate(available_memorials):
                            if item.memorial.id == current_memorial_id:
                                if forward:
                                    if index == (len(available_memorials)-1):
                                        # if current memorial is last in list, go back to start
                                        memorial = available_memorials.first()
                                        break
                                    current_found = True
                                else:
                                    if index == 0:
                                        # if current memorial is first in list, go to end
                                        memorial = available_memorials[(len(available_memorials)-1)]
                                    # else memorial will be equal to previous
                                    break
                            else:
                                memorial = item

                                if current_found:
                                    # memorial will be equal to next
                                    break

                    print('setting')
                    print(memorial.memorial.id)
            if memorial:
                memorial.set_processing()
                memorial.save()

                memorial_in_use = MemorialHistory.objects.filter(memorial=memorial, user=self)

                if memorial_in_use:
                    # update existing viewed memorial with new state
                    memorial_in_use.update(state=MemorialState.objects.get_in_use(), time=timezone.now())
                else:
                    MemorialHistory.objects.update_or_create(memorial=memorial, user=self, state=MemorialState.objects.get_in_use(), defaults={'time':timezone.now()})
                return memorial

    def get_in_use_memorial(self):
        memorial_history = MemorialHistory.objects.filter(user=self, state=MemorialState.objects.get_in_use())
        if memorial_history.exists() and (memorial_history.count()==1) :
            return memorial_history.first().memorial
        else:
            return None
    
    def get_in_use_memorial_id(self):
        current_memorial = self.get_in_use_memorial()

        if current_memorial:
            return current_memorial.memorial.id
        else:
            return None

    def get_skipped_memorials(self, select_for_update=False):
        memorial_history = MemorialHistory.objects.filter(user=self, state=MemorialState.objects.get_skipped())
        if memorial_history.exists() and (memorial_history.count()==1) :
            return memorial_history.values('memorial')
        else:
            return None

    def set_skipped_memorial(self, memorial=None):
        with transaction.atomic():
            if not memorial:
                memorial = self.get_in_use_memorial()
            if memorial:
                memorial.set_unprocessed()
                MemorialHistory.objects.filter(memorial=memorial, user=self).update(state=MemorialState.objects.get_skipped(), time=timezone.now())

    def set_current_processed(self):
        with transaction.atomic():
            dmmemorial = self.get_in_use_memorial()
            if dmmemorial:
                dmmemorial.set_processed()
                memorial_history = MemorialHistory.objects.filter(memorial=dmmemorial, user=self, state=MemorialState.objects.get_in_use()).update(state=MemorialState.objects.get_finished())

    def set_memorial_viewed(self):
        with transaction.atomic():
            dmmemorial = self.get_in_use_memorial()
            if dmmemorial:
                dmmemorial.set_unprocessed()
                memorial_history = MemorialHistory.objects.filter(memorial=dmmemorial, user=self).update(state=MemorialState.objects.get_viewed())

class DataMatchingMemorial(models.Model):
    memorial = models.OneToOneField(Memorial, primary_key=True, related_name='data_matching', on_delete=models.CASCADE)
    state = models.ForeignKey(ImageState, on_delete=models.CASCADE)
    objects = DataMatchingMemorialQuerySet.as_manager()

    def set_processing(self):
        self.state = ImageState.objects.get(image_state='processing')
        self.save()

    def set_processed(self):
        self.state = ImageState.objects.get(image_state='processed')
        self.save()

    def set_unprocessed(self):
        self.state = ImageState.objects.get(image_state='unprocessed')
        self.save()

    def set_user_skipped(self, dmuser):
        if self.is_matched is True:
            raise(Exception('Memorial already matched.'))
        link = self.memorialuserlink_set.select_for_update().get(datamatching_user=dmuser)
        link.skipped = True
        link.save()
        self.in_use = False
        self.revalidation_required = False

    def set_user_matched(self, dmuser):
        self.is_matched = True
        self.in_use = False
        self.revalidation_required = False

#     def set_revalidation_required(self):
#         self.revalidation_required = True
#         self.in_use = False
#         self.is_matched = False


class MemorialHistory(models.Model):
    """Many to many link holding the users history, which records which DataMatchingMemorials
    have been in which state at what time"""
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    memorial = models.ForeignKey(DataMatchingMemorial, on_delete=models.CASCADE)
    state = models.ForeignKey(MemorialState, on_delete=models.CASCADE)
    """State can be 'in_use', 'skipped' or 'revisit'"""
    time = models.DateTimeField(auto_now_add=timezone.now)

    class Meta:
        unique_together = ('user', 'memorial', 'state')



# class DataMatchingMemorial(models.Model):
#     """Datamatching extension of Memorial, with additional fields relating to whether matching is
#     done, validation is done and whether the memorial is locked by a user as in_use.
#     """
# #     memorial = models.OneToOneField(Memorial,primary_key=True)
# #     memorial = models.IntegerField()
# #     memorial = models.OneToOneField(Memorial,primary_key=True)
#     is_matched = models.BooleanField(default=False)
#     in_use = models.BooleanField(default=False)
#     revalidation_required = models.BooleanField(default=False)
#     objects = DataMatchingMemorialQuerySet.as_manager()
#
#     def set_in_use(self):
# #         if self.is_matched is True:
# #             raise(Exception('Memorial already matched.'))
#         self.in_use = True
#         self.revalidation_required = False
#
#     def set_not_in_use(self):
#         self.in_use = False
#
#     def set_skipped(self, dmuser):
#         if self.is_matched is True:
#             raise(Exception('Memorial already matched.'))
#         link = self.memorialuserlink_set.select_for_update().get(datamatching_user=dmuser)
#         link.skipped = True
#         link.save()
#         self.in_use = False
#         self.revalidation_required = False
#
#     def set_is_matched(self):
#         self.is_matched = True
#         self.in_use = False
#         self.revalidation_required = False
#
#     def set_revalidation_required(self):
#         self.revalidation_required = True
#         self.in_use = False
#         self.is_matched = False

# class DatamatchingUser(models.Model):
#     """Datamatching extension of user, which has a list of memorials they have
#     viewed.
#     """
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     memorials = models.ManyToManyField(DataMatchingMemorial, through='MemorialUserLink')
#
#     def get_in_use_memorial(self, select_for_update=False):
#         if select_for_update:
#             memorial = self.memorials.select_for_update()
#         else:
#             memorial = self.memorials
#         memorial = memorial.filter(in_use=True)
#         if memorial.exists():
#             return memorial.first()
#         else:
#             return None
#
#     def get_skipped_memorials(self, select_for_update=False):
#         if select_for_update:
#             memorial = self.memorials.select_for_update()
#         else:
#             memorial = self.memorials
#         return memorial.filter(memorialuserlink__skipped=True, is_matched=False)
#
#     def get_matched_memorials(self, select_for_update=False):
#         if select_for_update:
#             memorial = self.memorials.select_for_update()
#         else:
#             memorial = self.memorials
#         return memorial.filter(memorialuserlink__skipped=False, is_matched=True)
#
#     def get_revalidation_required_memorials(self, select_for_update=False):
#         if select_for_update:
#             memorial = self.memorials.select_for_update()
#         else:
#             memorial = self.memorials
#         return memorial.filter(revalidation_required=True)


# class MemorialUserLink(models.Model):
#     """Linking table between DataMatchingMemorial and MemorialUser implementing a
#     ManyToManyField, with the additional info if user has skipped the given memorial"""
#     datamatching_memorial = models.ForeignKey(DataMatchingMemorial)
#     datamatching_user = models.ForeignKey(DatamatchingUser)
#     skipped = models.BooleanField(default=False)
#     objects = MemorialUserLinkQuerySet.as_manager()
