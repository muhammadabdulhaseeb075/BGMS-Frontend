import hashlib
import datetime
from os import stat
import random
import logging

from html5lib import serialize
logger = logging.getLogger('django.request')

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.db import connection
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpRequest, JsonResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.utils import timezone
from django.views.generic import RedirectView, View, FormView, TemplateView
from tenant_schemas.utils import schema_context
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from BGMS.utils import email_ag_admin, password_reset_notify
from bgsite.views import AjaxableResponseMixin, AuthenticatedView, AdminView, BStaffView
from cemeteryadmin.models import EventType
from main.forms import UserCreateForm, SiteRedirectForm, ResetRequestForm
from main.models import BurialGroundSite, RegisteredUser, SitePreferences, BGUser, UserPasswordRequests, siteReferenceSettings
from main.serializers import siteReferenceSettingsSerializer


class ResetRequestView(FormView):
    """
    View defining what a user sees and what the webapp does when a password reset is requested from the login screen.
    """    
    template_name = "request_reset.html"
    form_class = ResetRequestForm

    def form_valid(self, form):

        user_email = form.cleaned_data
        user = BGUser.objects.get(email=user_email)
        user_name = user.get_full_name()
        auth, message = user.get_password_authorizer()
        password_reset_notify(user_name, user_email, auth, message)

        # Add to the list of unresolved password requests, if this request
        # doesn't already exist.
        # There may be an old, non-active, request.
        if not UserPasswordRequests.objects.filter(user=user).exists():
            UserPasswordRequests.objects.create(user=user)

        else:
            old_request = UserPasswordRequests.objects.get(user=user)
            old_request.make_fresh()

        return render(self.request,
                      'request_reset.html',
                      {'request_success': 'true',
                       'email' : user_email})

    def form_invalid(self, form):
        return super(ResetRequestView, self).form_invalid(form)


class ConfirmPasswordResetView(PasswordResetConfirmView):
    """
    View controlling what a user sees, and what the webapp does, when a password reset link is clicked and the resulting form interacted with.
    """    
    template_name = 'main/password_reset.html'
    form_class = SetPasswordForm
    success_url = '/reset/done/'

    def form_valid(self, form):

        form.save()

        # Update request status corresponding to this reset.
        user = form.user

        this_request = UserPasswordRequests.objects.get(user=user)
        this_request.make_complete()

        return super().form_valid(form)

    def form_invalid(self, form):

        user = form.user
        this_request = UserPasswordRequests.objects.get(user=user)
        this_request.set_status("Reset incomplete")

        return super().form_invalid(form)


class IndexView(View):
    """
    It is called when the URL is just the plain domain or subdomain: eg. www.bgms.co.uk

    GET request: Redirects to /home when the user is already authenticated.
                 Redirects to /main/home.html if the user is not authenticated.
    """

    #logger.info("IndexView handler called. INFO level. TT")
    #logger.debug("IndexView handler called. DEBUG level. TT")
    def get(self, request):
        if request.user.is_authenticated:
            #return to profile page here, when profile page is created            
            return render(request, 'main/home.html', {'SiteRedirectForm': SiteRedirectForm()})
        else:                        
            return HttpResponseRedirect('/login')    
    template_name = "main/home.html"


class MainView(BStaffView, TemplateView):
    template_name = "main/booking.html"


class TenantRedirectView(RedirectView):
    """
    It is called when the pattern of the URL is /redirect and Posting the site_name to it wish to be redirected.
    If the wish site_name exists as a Site created in main.BurialGroundSite it redirects to
    http://(main.BurialgroundSite.url)/login so the user will be able to authenticate and interact with that particular site and schema.
    """    
    permanent = True
    query_string = False
    pattern_name = 'tenant_redirect'

    def get_redirect_url(self, *args, **kwargs):
        query = self.request.POST.get('site_name', False)
        if query:
            bgs = get_object_or_404(BurialGroundSite, schema_name__iexact=query)
            return '//'+bgs.domain_url+'/login'

class TenantRedirectAjaxView(AjaxableResponseMixin, FormView):
    """
    It is called when the pattern of the URL is /redirect and Posting the site_name to it wish to be redirected.
    If the wish site_name exists as a Site created in main.BurialGroundSite it redirects to
    http://(main.BurialgroundSite.url)/login so the user will be able to authenticate and interact with that particular site and schema.
    """    
    template_name = 'main/home.html'
    success_url = '/register'
    form_class = SiteRedirectForm
    

    def form_valid(self, form):
        data = form.cleaned_data
        site_name = data['site']
        if BurialGroundSite.objects.filter(schema_name__iexact=site_name).exists():
            domain_url = "".join([settings.PROTOCOL_REDIRECT, BurialGroundSite.objects.get(schema_name__iexact=site_name).domain_url])
            if settings.DEBUG:
                domain_url = "".join([domain_url, ":8000"])
            return super(TenantRedirectAjaxView, self).form_valid(form, {'site_url': domain_url})
        else:
            return super(TenantRedirectAjaxView, self).form_valid(form, {'site_url': ''})
    # def get_redirect_url(self, *args, **kwargs):
    #     query = self.request.POST.get('site_name', False)
    #     if query:
    #         bgs = get_object_or_404(BurialGroundSite, schema_name__iexact=query)
    #         return '//'+bgs.domain_url+'/login'

    def form_invalid(self, form):
        return super(TenantRedirectAjaxView, self).form_invalid(form)


class RegisterView(AjaxableResponseMixin, FormView):
    """
    View in charge of register the user in two step process, first: mail validation
    second: AG activation of the user
    """
    template_name = 'main/register.html'
    success_url = '/register'
    form_class = UserCreateForm
    

    def form_valid(self, form):
        data = form.cleaned_data
        # print(data)
        form.save()
        custom_user = get_user_model()
        user = custom_user.objects.get(email=data['email'])
        # import pdb; pdb.set_trace()
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.username = data['username']
        user.is_active = False
        user.save()
        salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
        activation_key = hashlib.sha1((salt+data['email']).encode('utf-8')).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        #create new registered user
        new_registered_user = RegisteredUser(user=user, activation_key=activation_key, key_expires=key_expires)
        new_registered_user.save()

        #send email with activation link
        host = HttpRequest.get_host(self.request)
        # email_body = "Hi %s, thanks for signing up. To verify your mail, click this link within 48 hours http://%s/confirm/%s" % (username, host, activation_key)
        # send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL ,[username], fail_silently=False)

        button_url = "https://{0}/confirm/{1}".format(host, activation_key)
        user.email_user('BGMS email verification', 'mail_templated/site_user_register.tpl', {'button_url':button_url})

        return super(RegisterView, self).form_valid(form, {'data': 'Thank you for registering. Please check your email account and validate your email address by clicking the link provided. If you do not receive the email try checking your junk folder or make sure you entered the address correctly.'})

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)

class ConfirmMailView(View):
    """
    It is called when the link of a confirmation mail is called eg. http://127.0.0.1:8000/accounts/confirm/ca913dfa707224b21314fed7fe8328bcb4d59148

    GET request: check if user is already logged in and if he is redirect him to some other url
                 check if there is UserProfile which matches the activation key
                 check if the activation key has expired, if it hase then render confirm_expired.html
                       if the key hasn't expired save RegisteredUser and set him as mail verified and render confirm template to confirm activation
                 Send email to AG Admin to activate the user account
    """    
    template_name = "main/home.html"

    def get(self, request, activation_key):
        # import pdb; pdb.set_trace()
        #check if user is already logged in and if he is redirect him to some other url, e.g. home
        if request.user.is_authenticated:
            HttpResponseRedirect(self.template_name)
        # check if there is UserProfile which matches the activation key (if not then display 404)
        user_profile = get_object_or_404(RegisteredUser, activation_key=activation_key)
        #check if the activation key has expired, if it hase then render confirm_expired.html
        if user_profile.key_expires < timezone.now():
            return render_to_response('main/confirm_expired.html')
        #if the key hasn't expired save RegisteredUser and set him as mail verified and render confirm template to confirm activation
        user_profile.isMailVerified = True
        user_profile.save()

        #Send email to AG Admin to activate the user account
        # email_subject = 'Account confirmation'
        # host = HttpRequest.get_host(self.request)
        # email_body = "Hi AG Admin, the user %s has verified his mail. Please click in the following link to activate the user's account: http://%s/confirmAccount/%s" % (user_profile.user.email, host, activation_key)
        # send_mail(email_subject, email_body, settings.DEFAULT_FROM_EMAIL ,[settings.EMAIL_AG_ADMIN], fail_silently=False)

        #Send email to AG Admin when user confirmed mail
        email_ag_admin('New user account confirmation', 'mail_templated/ag_admin.tpl', {'new_user' : user_profile.user.username})

        return render_to_response('main/confirm.html')

class UserAccessView(AuthenticatedView):
    """
    Return user's access
    """    
    def get(self, request):

        """ Get sites this user can access """
        sites_response = []

        if request.user.is_superuser:
            sites = BurialGroundSite.objects.exclude(schema_name='public')
        else:
            burialgroundsite_ids = request.user.site_groups.filter(Q(group__name='SiteAdmin') | Q(group__name='SiteWarden') | Q(group__name='SiteUser') | Q(group__name='BereavementStaff') | Q(group__name='DataEntry') | Q(group__name='DataMatcher') | Q(group__name='MemorialPhotographer')).values_list('burialgroundsite_id', flat=True).distinct()
            sites = BurialGroundSite.objects.filter(id__in=burialgroundsite_ids)

        for site in sites:
            site_data = {"id": site.id, "name": site.name, "domain_url": site.get_site_domain_url(), "bereavement_staff": False, 'client_id': site.client_id}

            # data entry permission
            if request.user.has_data_entry_permission(site.schema_name):
                site_data['data_entry'] = True

            # data matcher permission
            if request.user.has_data_entry_permission(site.schema_name):
                site_data['data_matcher'] = True

            # site admin permission
            if request.user.has_site_admin_permission(site.schema_name):
                site_data['site_admin'] = True

            # bereavement staff permission
            if request.user.has_bereavement_staff_permission(site.schema_name):
                site_data['bereavement_staff'] = True

                # get the available events for this site
                with schema_context(site.schema_name):

                    # this will fail if empty schema
                    try:
                        site_data['event_types'] = list(EventType.objects.all().values(
                            'id', 'name', 'event_category_id', 'event_category__booking_buffer_duration', 'event_category__simultaneous_bookings', 'event_category__max_booking_per_day',
                            'default_duration', 'event_earliest_time_mon', 'event_latest_time_mon',
                            'event_earliest_time_tue', 'event_latest_time_tue', 'event_earliest_time_wed',
                            'event_latest_time_wed', 'event_earliest_time_thu', 'event_latest_time_thu',
                            'event_earliest_time_fri', 'event_latest_time_fri', 'event_earliest_time_sat',
                            'event_latest_time_sat', 'event_earliest_time_sun', 'event_latest_time_sun'
                        ))

                    except:
                        pass

            # get or create site preferences
            site_preferences, _ = SitePreferences.objects.get_or_create(site_details_id=site.site_details_id)
            site_data['preferences'] = model_to_dict(site_preferences)

            sites_response.append(site_data)

        sites_response = sorted(sites_response, key=lambda k: k['name'])

        return JsonResponse({"sites": sites_response, 'sitemanagement': request.user.is_superuser}, safe=False)

class siteReferenceSettingsView(APIView):
    """CRUD api for Site Reference Settings"""

    def get(self, request, pk):
        """gets a site ref setting by their pk"""
        site_ref_setting = siteReferenceSettings.objects.select_related('ref_style', 'burialgroundsite', 'start_number').get(id=pk)
        serializer = siteReferenceSettingsSerializer(site_ref_setting)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        """Creates new site reference setting """
        request_data = request.data
        serializer = siteReferenceSettingsSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
        else:
            return Response(data={'detail': 'Form contains invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response (data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """patch and existing site reference setting"""
        request_data = request.data
        site_ref_setting = siteReferenceSettings.objects.get(id=pk)
        serializer = siteReferenceSettingsSerializer(site_ref_setting, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(data="Wrong Parameters", status=status.HTTP_400_BAD_REQUEST)