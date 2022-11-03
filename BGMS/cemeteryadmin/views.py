""" Views for cemeteryadmin """

import traceback
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from bgsite.views import group_required
from cemeteryadmin import serializer
from cemeteryadmin.serializer import CalendarEventsSerializer, FuneralEventSerializer, FuneralCreatorsSerializer, FuneralDirectorSerializer, FuneralDirectorsListSerializer, PreburialCheckSerializer, PostburialCheckSerializer, CancelburialSerializer, MeetingLocationListSerializer, MeetingLocationSerializer, SettingsSerializer
from cemeteryadmin.models import CalendarEvents, FuneralEvent, FuneralEventStatus, PreburialCheck, PostburialCheck, Cancelburial, Settings
from config.security.drf_permissions import BereavementStaffPermission
from main.models import BurialGroundSite, ReservePlotState
from bgsite.models import Official, MeetingLocation, GravePlot, ReservedPlot


class SettingsView(ListAPIView):
    """
    Return list of settings for a given site
    """
    serializer_class = SettingsSerializer
    permission_classes = [BereavementStaffPermission]
    #queryset = Settings.objects.filter(name__isnull=False)
    def get_queryset(self):
        """
        Return JSON settings that match the module name
        """

        return Settings.objects \
        .filter(name=self.kwargs['name'])
        #.exclude(Q(funeral_event__isnull=False) & Q(funeral_event__status=FuneralEventStatus.CANCELLED.value))
        #.exclude(Q(funeral_event__isnull=False))

class FuneralCreatorsView(ListAPIView):
    """
    Return list of users who have made funeral bookings
    """

    serializer_class = FuneralCreatorsSerializer
    permission_classes = [BereavementStaffPermission]
    queryset = CalendarEvents.objects.filter(funeral_event__isnull=False).distinct('created_by').select_related('created_by')

class CalendarEventsView(ListAPIView):
    """
    API view for returning a list of calendar events
    """

    serializer_class = CalendarEventsSerializer
    permission_classes = [BereavementStaffPermission]

    def get_serializer_context(self):
        """
        Get this site's timezone and add it to serializer context
        """
        context = super(CalendarEventsView, self).get_serializer_context()
        context.update({
            "timezone": BurialGroundSite.get_site_timezone()
        })
        return context

    def get_queryset(self):
        """
        Return events that fall on the given date range (range in months).

        Note: this is not timezone aware. It doesn't need to be as there is always a one month buffer for the calendar.
        """

        return CalendarEvents.objects \
        .filter(start__range=[self.kwargs['start'], self.kwargs['end']]) \
        #.exclude(Q(funeral_event__isnull=False) & Q(funeral_event__status=FuneralEventStatus.CANCELLED.value))
        #.exclude(Q(funeral_event__isnull=False))

class PreburialCheckView(APIView):
  """
  API view for Preburial Check
  Get / Post / Patch / Delete
  """
   
  def patch(self, request, preburial_id, postburial_id,cancelburial_id):
        """
        Patch an existing funeral event
        """
        for key,data in request.data.items():
          if key == 'predata':
            datapre = data
          elif key == 'postdata':
            datapost = data
          elif key == 'canceldata':
            datacancel = data

        preburial_check = PreburialCheck.objects.get(pk=preburial_id)
        postburial_check = PostburialCheck.objects.get(pk=postburial_id)
        cancelburial = Cancelburial.objects.get(pk=cancelburial_id)

        change_status_pre = True
        change_status_post = True
        change_status_cancel = True
        for reg in datapre.values():
          if reg is None:
            change_status_pre = False
            break

        for reg in datapost.values():
          if reg is None:
            change_status_post = False
            break

        for reg in datacancel.values():
          if reg is None:
            change_status_cancel = False
            break

        funeralevent = FuneralEvent.objects.get(preburial_check_id=preburial_id)
        if change_status_cancel:
          funeralevent.status = FuneralEventStatus.CANCELLED.value
        elif not(change_status_pre):
          funeralevent.status = FuneralEventStatus.PRE_BURIAL_CHECKS.value
        elif change_status_pre and not(change_status_post) and not(change_status_cancel) and funeralevent.status == FuneralEventStatus.PRE_BURIAL_CHECKS.value:    
          funeralevent.status = FuneralEventStatus.AWAITING_BURIAL.value
        elif change_status_pre and change_status_post and not(change_status_cancel):
          funeralevent.status = FuneralEventStatus.COMPLETED.value
        elif change_status_pre and not(change_status_post) and not(change_status_cancel) and funeralevent.status == FuneralEventStatus.COMPLETED.value:
          funeralevent.status = FuneralEventStatus.POST_BURIAL_CHECKS.value        
                 
        funeralevent.save()             

        serializer_preburial = PreburialCheckSerializer(preburial_check, data=datapre,partial=True)
        serializer_postburial = PostburialCheckSerializer(postburial_check, data=datapost,partial=True)
        serializer_cancelburial = CancelburialSerializer(cancelburial, data=datacancel,partial=True)

        if serializer_preburial.is_valid() and serializer_postburial.is_valid() and serializer_cancelburial.is_valid() :
            serializer_preburial.save()
            serializer_postburial.save()
            serializer_cancelburial.save()
            return Response(data=serializer_preburial.data)
        return Response( data="wrong parameters")



class CancelburialView(APIView):
  """
  API view for Preburial Check
  Get / Post / Patch / Delete
  """ 

  @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
  def post(self, request):
    """
    Post an existing funeral event
    """
    data = request.data
    serializer = CancelburialSerializer(data=data)
    if serializer.is_valid(True):
      serializer.save(created_by=request.user)
    else:
      return Response(data={'detail': 'Form contains invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={'status': serializer.data.get('status')}, status=status.HTTP_200_OK)

  def patch(self, request, cancelburial_id):
        """
        Patch an existing funeral event
        """

        data = request.data
        cancelburial = Cancelburial.objects.get(pk=cancelburial_id)
        changeStatus = True
        for reg in data.values():
          if reg is None:
            changeStatus = False
            break

        if changeStatus:
          funeralevent = FuneralEvent.objects.get(cancelburial_id=cancelburial_id)
          funeralevent.status = FuneralEventStatus.CANCELLED.value
          funeralevent.save()             

        serializer = CancelburialSerializer(cancelburial, data=request.data,partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response( data="wrong parameters")

class PostburialCheckView(APIView):
  """
  API view for Preburial Check
  Get / Post / Patch / Delete
  """
  

  @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
  def post(self, request):
    """
    Post an existing funeral event
    """
    data = request.data
    serializer = PostburialCheckSerializer(data=data)
    if serializer.is_valid(True):
      serializer.save(created_by=request.user)
    else:
      return Response(data={'detail': 'Form contains invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(data={'status': serializer.data.get('status')}, status=status.HTTP_200_OK)

  def patch(self, request, postburial_id):
        """
        Patch an existing funeral event
        """

        data = request.data
        postburial_check = PostburialCheck.objects.get(pk=postburial_id)
        changeStatus = True
        for reg in data.values():
          if reg is None:
            changeStatus = False
            break

        if changeStatus:
          print(FuneralEventStatus.AWAITING_BURIAL.value)
          funeralevent = FuneralEvent.objects.get(postburial_check_id=postburial_id)
          funeralevent.status = FuneralEventStatus.COMPLETED.value
          funeralevent.save()
        
        serializer = PostburialCheckSerializer(postburial_check, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response( data="wrong parameters")

class FuneralEventView(APIView):
    """
    API view for funeral events
    Get / Post / Patch / Delete
    """
    permission_classes = [BereavementStaffPermission]

    @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
    def get(self, request, event_id):
        """
        Gets an existing funeral event by event_uuid
        """
        funeral_event = FuneralEvent.objects.select_related('calendar_event', 'person', 'person__death', 'person__next_of_kin', 'burial', 'reservation', 'preburial_check', 'postburial_check').get(pk=event_id)
        serializer = FuneralEventSerializer(funeral_event, context={'user': request.user})
        return JsonResponse(serializer.data, safe=False)

    @transaction.atomic
    @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True, ))
    def post(self, request):
        """
        Creates a new funeral event
        """
        data = request.data

        """ Format datetimes """

        if not 'start' in data['calendar_event']:
            return Response({'detail': "ERROR: Start datetime is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not 'end' in data['calendar_event']:
            return Response({'detail': "ERROR: End datetime is required"}, status=status.HTTP_400_BAD_REQUEST)

        """Confirm Funeral Director is set"""
        if not 'funeral_director_id' in data:
            return Response({'detail': "ERROR: Funeral Director is required"}, status=status.HTTP_400_BAD_REQUEST)        
      
    
        fmt = '%Y-%m-%dT%H:%M'
        site_tz = BurialGroundSite.get_site_timezone()

        start = datetime.strptime(data['calendar_event']['start'], fmt)
        data['calendar_event']['start'] = make_aware(start, site_tz)
        end = datetime.strptime(data['calendar_event']['end'], fmt)
        data['calendar_event']['end'] = make_aware(end, site_tz)
        try:
            CalendarEvents.objects.validate_event_datetime(start, end, data['calendar_event']['event_type_id'], None)
        except ValidationError as e:
            return Response(data={'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)

        #If next of kin is passed in parse the data to create an associated person object
        next_of_kin_person = data['next_of_kin_person'] if 'next_of_kin_person' in data else None

        #Save to initialize the uuid values, since the reservation uses a personid (hardly ideal but so it goes) we need to save first then grab the id
        serializer = FuneralEventSerializer(data=data, context={'next_of_kin': next_of_kin_person, 'user': request.user})
        if serializer.is_valid(True):
            serializer.save(created_by=request.user)
        else:
            return Response(data={'detail': 'Form contains invalid data'}, status=status.HTTP_400_BAD_REQUEST)


        # Create a reservation and add it to the FuneralEvent
       # plot_state = ReservePlotState.objects.get(id=1)
      #  reservation = ReservedPlot(person=serializer.instance.person, date=start, state=plot_state)
        # TODO: set graveplot & notes
     #   reservation.save()  # New reservation object so should always save?
    #    serializer.reservation = reservation
        # serializer.reservation_id = reservation.pk  # Also need to save id value to table?

   #     if serializer.is_valid(True):
  #          serializer.save()
            # serializer.save(created_by=request.user)
 #       else:
#            return Response(data={'detail': 'Form contains invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        # At this point the FuneralEvent should be created with associated objects included in data.
        # The ReservedPlot object is not passed in but is created based on included data.
        # Since data has been validated we can now create a ReservedPlot and add it to the FuneralEvent


        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
    def patch(self, request, event_id):
        """
        Patch an existing funeral event
        """
        data = request.data
        funeral_event = FuneralEvent.objects.select_related('calendar_event', 'person', 'person__death', 'reservation', 'burial').get(pk=event_id)
        
        try:
            if 'calendar_event' in data:

                fmt = '%Y-%m-%dT%H:%M'

                start = datetime.strptime(data['calendar_event'].get('start'), fmt) if 'start' in data['calendar_event'] else funeral_event.calendar_event.start
                end = datetime.strptime(data['calendar_event'].get('end'), fmt) if 'end' in data['calendar_event'] else funeral_event.calendar_event.end

                fe_status = data['status'] if 'status' in data else funeral_event.status

                try:
                    CalendarEvents.objects.validate_event_datetime(start, end, funeral_event.calendar_event.event_type_id, funeral_event.calendar_event_id, fe_status)
                    if(funeral_event.reservation):
                        funeral_event.reservation.date = start
                        funeral_event.reservation.save()
                except ValidationError as e:
                    raise ValidationError(e.message)
            
            next_of_kin_person = data['next_of_kin_person'] if 'next_of_kin_person' in data else None

            #Check if graveplot uuid has been passed in. If so fetch Graveplot object
            grave_plot_uuid = data['burial']['burial_uuid'] if 'burial' in data else None
            graveplot = None
            if(grave_plot_uuid):
                try:
                    graveplot = GravePlot.objects.get(uuid=grave_plot_uuid)
                except ValidationError as e:
                    raise ValidationError(e.message)
            #If graveplot has been passed in and exists then add it to the funeral_event.
            if(graveplot):
                if(funeral_event.reservation):
                    funeral_event.reservation.grave_plot = graveplot
                    funeral_event.reservation.save()
                funeral_event.burial.add_graveplot(graveplot)
                funeral_event.burial.save()

            serializer = FuneralEventSerializer(funeral_event, data=data, partial=True, context={'next_of_kin': next_of_kin_person, 'user': request.user})
        
            if serializer.is_valid():
                serializer.save(last_edit_by=request.user)
                return Response(data={'status': serializer.data.get('status'), 'next_of_kin_person': serializer.data['next_of_kin_person']}, status=status.HTTP_200_OK)
            else:
                raise ValidationError("Form contains invalid data")
        except ValidationError as e:
            return Response(data={'detail': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(traceback.format_exc())
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
    def delete(self, request, event_id):
        """
        Deletes an already cancelled funeral event (hard delete)
        """

        funeral_event = FuneralEvent.objects.get(pk=event_id)

        """
        Can only delete cancelled events.
        Don't handle wrong status code as this should never happen.
        """
        if funeral_event.status == 7:
            funeral_event.burial.hard_delete()
            funeral_event.person.hard_delete()
            funeral_event.calendar_event.delete()
            funeral_event.delete()

            return Response(status=status.HTTP_200_OK)

class CancelFuneralEventView(APIView):
    """
    API view for cancelling a funeral event (soft delete)
    """

    @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
    def put(self, request, event_id):
        """
        Cancels a funeral event (soft delete)
        """

        funeral_event = FuneralEvent.objects.get(pk=event_id)

        """
        Can only cancel events that have not yet taken place.
        Don't handle wrong status code as this should never happen.
        """
        if funeral_event.status < 4:
            funeral_event.status = FuneralEventStatus.CANCELLED.value
            funeral_event.burial.delete()
            funeral_event.person.delete()
            funeral_event.save()

            return Response(status=status.HTTP_200_OK)

class FuneralDirectorsListView(ListAPIView):
    """
    Returns list of funeral directors that belong to the same client that the current connection belongs to.
    """

    serializer_class = FuneralDirectorsListSerializer
    permission_classes = [BereavementStaffPermission]

    def get_queryset(self):
        """
        Return funeral events that belong to current client
        """        
        return Official.objects.all().filter(deleted_at=None)

class FuneralDirectorView(APIView):
    """
    CRUD api for funeral director
    """
    @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
    def get(self, request, pk):
        """
        Gets a funeral director by their pk
        """

        funeral_director = Official.objects.get(id=pk)
        serializer = FuneralDirectorSerializer(funeral_director)
        return JsonResponse(serializer.data, safe=False)

    @transaction.atomic
    @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
    def post(self, request):
        """
        Creates a new funeral director
        """
        request_data = request.data
        #if request_data['company']['name']:
        #    request_data["company_name"] = request_data["company"]["name"]
        #request_data.pop('company')
        serializer = FuneralDirectorSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
        else:
            return Response(data={'detail': 'Form contains invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

      
    @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
    def patch(self, request, pk):
        """
        Patch an existing funeral director
        """
        request_data = request.data
        funeral_director = Official.objects.get(id=pk)

        serializer = FuneralDirectorSerializer(funeral_director, data=request_data, partial=True) # set partial=True to update 
        if serializer.is_valid():          
            serializer.update(funeral_director, serializer.validated_data);
            return JsonResponse(data=serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(data="Wrong Parameters", status=status.HTTP_400_BAD_REQUEST)

class MeetingLocationListView(ListAPIView):
    """Returns list of Meeting Locations that belong to the same client that the current connection belongs to"""

    serializer_class = MeetingLocationListSerializer
    permission_classes = [BereavementStaffPermission]

    def get_queryset(self):
      """Return meeting locations that belong to current client"""
      return MeetingLocation.objects.all()

class MeetingLocationView(APIView):
  """CRUD api for Meeting Location"""

  @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
  def get(self, request, pk):
    """gets a meeting location by their pk"""
    meeting_location = MeetingLocation.objects.get(id=pk)
    serializer = MeetingLocationSerializer(meeting_location)
    return JsonResponse(serializer.data, safe=False)

  @transaction.atomic
  @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
  def post(self, request):
    """creates a new Meeting location"""
    request_data = request.data
    serializer = MeetingLocationSerializer(data=request_data)
    if serializer.is_valid():
      serializer.save(created_by=request.user)
    else:
      return Response(data={'detail': 'Form contains invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=serializer.data, status=status.HTTP_200_OK)

  @method_decorator(group_required('BereavementStaff', 'SiteAdmin', raise_exception=True,))
  def patch(self, request, pk):
    """patch an existing meeting location"""
    request_data = request.data
    meeting_location = MeetingLocation.objects.get(id=pk)

    serializer = MeetingLocationSerializer(meeting_location, data=request_data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return JsonResponse(data=serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(data="Wrong Parameters", status=status.HTTP_400_BAD_REQUEST)