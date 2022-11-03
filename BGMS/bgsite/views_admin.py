from django.core import exceptions
from django.shortcuts import render
from bgsite.views import AdminView, AjaxableResponseMixin
from bgsite.forms_admin import UploadPhotosForm, UploadBurialRecordPhotosForm, addPermissionsForm, sendEmailInvitationForm, UploadOwnershipRegisterPhotosForm
from django.views.generic.edit import FormView
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from bgsite.models import Memorial, Burial, DataUpload, Image, REGISTER_IMAGE_PAGENUMBER_PATTERN, REGISTER_IMAGE_GRAVENUMBER_PATTERN, GravePlot, GraveDeed
from django.contrib import admin
from django.conf import settings
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.views.generic import View
from django.db import IntegrityError, transaction, connection
from django.db.models import Q
import copy
import bgsite.admin
from main.models import BGUser, BurialGroundSite, UserPasswordRequests
from django.shortcuts import redirect
from BGMS.utils import email_non_user
from mapmanagement.views import linkPlotsToSection
from _sqlite3 import Row
import datetime
import json
import collections
from bgsite import data_upload_dicts as dud
from bgsite.spooler_functions import _process_data_upload, _process_delete_data_upload
import re
import traceback


class UploadPhotosView(AdminView, FormView):
    """
    GET request: Redirects to /uploadPhotos from the upload data tools option.
    POST request: Validates first if there are photo files and csv files uploaded
    then send the files to process the photos and relate the memorials to it
    """

    form_class = UploadPhotosForm

    def get(self, request):
        # import pdb; pdb.set_trace()
        upload_photos_form = UploadPhotosForm()
        return render(request, 'admin/upload_mass_photos.html', {'form': upload_photos_form, 'user': request.user, 'site_header': bgsite.admin.tenant_admin_site.site_header, 'has_permission': bgsite.admin.tenant_admin_site.has_permission(request), 'site_url': bgsite.admin.tenant_admin_site.site_url})

    def post(self, request):
        upload_photos_form = self.form_class(request.POST)
        if upload_photos_form.is_valid():
            if len(request.FILES.getlist('photosFiles')) > 0 and len(request.FILES.getlist('csv_file')) == 1:
                result = Memorial.objects.upload_photos_and_relate_memorial(request.FILES['csv_file'], request.FILES.getlist('photosFiles'))
                if len(result['error']) > 0:
                    # return HttpResponse(result['error'])
                    return render(request, 'admin/upload_mass_photos_error.html', {'errors': result['error'], 'user': request.user, 'site_header': bgsite.admin.tenant_admin_site.site_header, 'has_permission': bgsite.admin.tenant_admin_site.has_permission(request), 'site_url': bgsite.admin.tenant_admin_site.site_url})
                else:
                    return render(request, 'admin/upload_mass_photos_success.html', {'user': request.user, 'site_header': bgsite.admin.tenant_admin_site.site_header, 'has_permission': bgsite.admin.tenant_admin_site.has_permission(request), 'site_url': bgsite.admin.tenant_admin_site.site_url})
            else:
                # responseData = {'error': 'Please make sure to upload a CSV file and the same number of photos specified whithin the csv file.'}
                result = {'error': ['Please upload a CSV file and at least one Photo']}
                return render(request, 'admin/upload_mass_photos_error.html', {'errors': result['error'], 'user': request.user, 'site_header': bgsite.admin.tenant_admin_site.site_header, 'has_permission': bgsite.admin.tenant_admin_site.has_permission(request), 'site_url': bgsite.admin.tenant_admin_site.site_url})
        return HttpResponseBadRequest(upload_photos_form.errors)


class DataUploadView(AdminView):

    def get(self, request):
        return render(request, 'admin/data_upload.html', {'user': request.user, 'uploads': DataUpload.objects.all().order_by('-date'), 'site_header': bgsite.admin.tenant_admin_site.site_header, 'has_permission': bgsite.admin.tenant_admin_site.has_permission(request), 'site_url': bgsite.admin.tenant_admin_site.site_url, 'burial_fields': dud.burialFields, 'grave_fields': dud.graveFields, 'grave_owners_fields': dud.graveOwnershipFields, 'relation_fields': dud.relationshipFields})


class ResetAuthView(AdminView):

    def get(self, request):

        # Some paranoid guards against empty queries here. But that's okay.
        if (request.GET.get('DeleteButton')):

            this_request = UserPasswordRequests.objects.get(id=request.GET.get('DeleteButton'))

            if this_request:
                this_request.delete()

        elif (request.GET.get('ActionButton')):

            this_request = UserPasswordRequests.objects.get(id=request.GET.get('ActionButton'))

            if this_request:
                this_request.authorize_reset()


        if request.user.in_site_groups('SiteAdmin') and not request.user.is_superuser:
            # Show active requests for people who are below SiteAdmin, i.e.
            # for people who are not staff.
            active_requests = UserPasswordRequests.active_reqs_admins
            inactive_requests = UserPasswordRequests.inactive_reqs_admins

        else:
            # AG Admin
            active_requests = UserPasswordRequests.active_reqs_staff
            inactive_requests = UserPasswordRequests.inactive_reqs_staff

        return render(request, 'admin/reset_auth.html',
            {'active_requests': active_requests,
            'inactive_requests': inactive_requests,
            'site_header': bgsite.admin.tenant_admin_site.site_header,
            'has_permission': bgsite.admin.tenant_admin_site.has_permission(request),
            'site_url': bgsite.admin.tenant_admin_site.site_url,
            'password_timeout': settings.PASSWORD_RESET_TIMEOUT_DAYS})


class SectionLinkView(AdminView):

    def get(self, request):
        try:
            result = linkPlotsToSection()
            return JsonResponse({"section_linked_count":result[0], "section_partial_linked_count":result[1],"subsection_linked_count":result[2], "subsection_partial_linked_count":result[3], "not_saved":result[4]})
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(e)


def link_registers(request):
    """
    Auto link registry images with burial or ownership records

    Two formats:
    REGISTER_IMAGE_PAGENUMBER_PATTERN - link to burials with matching registry name and page number to that contined in file name
    REGISTER_IMAGE_GRAVENUMBER_PATTERN - link to burials with the same grave number (grave number must be unique) to that contined in file name
    """
    data = json.loads(request.body.decode())
    ownership_register = False

    if 'ownership_register' in data and data.get('ownership_register'):
        ownership_register = True

    if ownership_register:
        search_prefix = '{0}/images/user_uploads/ownership_register/'.format(connection.schema_name)
    else:
        search_prefix = '{0}/images/user_uploads/burial_record/'.format(connection.schema_name)

    images = Image.objects.filter(url__istartswith=search_prefix).order_by('url')
    count = 0

    try:
        i = 0
        graves_per_page = 0
        register = None

        while i < len(images):
            image = images[i]

            gravenumber_pattern = re.compile(REGISTER_IMAGE_GRAVENUMBER_PATTERN + '.*.(jpg|jpeg)', re.IGNORECASE).match(image.url.url)
            pagenumber_pattern = re.compile(REGISTER_IMAGE_PAGENUMBER_PATTERN + '.*.(jpg|jpeg)', re.IGNORECASE).match(image.url.url)

            # use the grave number contained in image filename
            if gravenumber_pattern:

                top_grave_number = gravenumber_pattern.group(2)

                if not register==gravenumber_pattern.group(1):
                    # Need to work out how many graves are featured on one page in this registry.
                    # Look at the next page...
                    gravenumber_pattern_2 = re.compile(REGISTER_IMAGE_GRAVENUMBER_PATTERN + '.*.(jpg|jpeg)', re.IGNORECASE).match(images[i+1].url.url)
                    next_top_grave_number = gravenumber_pattern_2.group(2)
                    graves_per_page = int(next_top_grave_number) - int(top_grave_number)

                    register = gravenumber_pattern.group(1)

                # for each grave on the page
                for j in range(graves_per_page):
                    grave_number = str(int(top_grave_number) + j).zfill(len(top_grave_number))

                    if ownership_register:
                        deeds = GraveDeed.objects.filter(graveplot__graveref__grave_number=grave_number)

                        # add image to each ownership in that grave
                        # (Although it'll only be relavent to one. But we're don't know which one.)
                        for deed in deeds:
                            if not deed.images.filter(pk=image.pk).exists():
                                deed.images.add(image)
                                count+=1
                    else:
                        burials = Burial.objects.filter(graveplot__graveref__grave_number=grave_number)

                        # add image to each burial in that grave
                        for burial in burials:
                            if not burial.burial_record_image == image:
                                burial.burial_record_image = image
                                burial.save()
                                count+=1

            # use the registry and page number contained in image filename
            elif pagenumber_pattern:

                register = pagenumber_pattern.group(1)
                page_number = pagenumber_pattern.group(2)
                burials = Burial.objects.filter(burial_record_image__isnull=True, register=register, register_page=int(page_number))

                for burial in burials:
                    burial.burial_record_image = image
                    burial.save()
                    count+=1

            i += 1

    except Exception as e:
        print(traceback.format_exc())
        return HttpResponseBadRequest(e)

    return JsonResponse({"success":'true', "count":count})


def update_graveplot_layers(request):
    """
    Update any incorrect graveplot layers i.e. burial, reservated plot or available plot.
    """

    plot_to_reserved_plot_count = 0
    plot_to_available_plot_count = 0
    reserved_plot_to_plot_count = 0
    reserved_plot_to_available_plot_count = 0
    available_plot_to_plot_count = 0
    available_plot_to_reserved_plot_count = 0

    try:
        graveplots = GravePlot.objects.filter(topopolygon__isnull=False)

        for graveplot in graveplots:

            original_layer = graveplot.topopolygon.layer.feature_code.feature_type
            new_layer = graveplot.update_plot_layer()

            # record changes
            if not original_layer==new_layer:
                if original_layer=='plot':
                    if new_layer=='reserved_plot':
                        plot_to_reserved_plot_count+=1
                    elif new_layer=='available_plot':
                        plot_to_available_plot_count+=1
                elif original_layer=='reserved_plot':
                    if new_layer=='plot':
                        reserved_plot_to_plot_count+=1
                    elif new_layer=='available_plot':
                        reserved_plot_to_available_plot_count+=1
                elif original_layer=='available_plot':
                    if new_layer=='plot':
                        available_plot_to_plot_count+=1
                    elif new_layer=='reserved_plot':
                        available_plot_to_reserved_plot_count+=1

    except Exception as e:
        print(traceback.format_exc())
        return HttpResponseBadRequest(e)

    return JsonResponse({'success':'true', 'plot_to_reserved_plot_count':plot_to_reserved_plot_count,
    'plot_to_available_plot_count': plot_to_available_plot_count, 'reserved_plot_to_plot_count': reserved_plot_to_plot_count,
    'reserved_plot_to_available_plot_count': reserved_plot_to_available_plot_count, 'available_plot_to_plot_count': available_plot_to_plot_count, 'available_plot_to_reserved_plot_count': available_plot_to_reserved_plot_count})


def submit_data_upload(request):

    graveFile = None
    graveOwnershipFile = None
    burialFile = None
    relationFile = None

    if 'graveFile' in request.FILES:
        graveFile = request.FILES['graveFile']

    if 'graveOwnershipFile' in request.FILES:
        graveOwnershipFile = request.FILES['graveOwnershipFile']

    if 'burialFile' in request.FILES:
        burialFile = request.FILES['burialFile']

    if 'relationFile' in request.FILES:
        relationFile = request.FILES['relationFile']

    files = collections.OrderedDict()
    filenames = ""

    if graveFile:
        files["grave"] = graveFile
        filenames = graveFile.name

    if graveOwnershipFile:
        files["graveOwnership"] = graveOwnershipFile
        filenames = graveOwnershipFile.name

    if burialFile:
        files["burial"] = burialFile
        if len(filenames)>0:
            filenames += "; "
        filenames += burialFile.name

    if relationFile:
        files["relation"] = relationFile
        filenames = relationFile.name

    dataUploadRecord = DataUpload(file_name=filenames, status="Processing", created_by=request.user)
    dataUploadRecord.save()

    """ In development, uWSGI spooler will not be available and process_data_upload will run synchronously
        On production server, uWSGI spooler will run process_data_upload asynchronously """
    #try:
    #    process_data_upload.spool(files, dataUploadRecord)
    #except:
    _process_data_upload(files, dataUploadRecord)

    return JsonResponse({"success":'true', "fileName": dataUploadRecord.file_name, "dataUploadRecordID": dataUploadRecord.id, "date": dataUploadRecord.date})

def delete_data_upload(request):
    
    data_upload_id = json.loads(request.body.decode('utf-8')).get("id")
    
    data_upload_record = DataUpload.objects.get(id=data_upload_id)
    data_upload_record.Status = "Deleting"
    data_upload_record.save()

    """ In development, uWSGI spooler will not be available and process_data_upload will run synchronously
        On production server, uWSGI spooler will run process_data_upload asynchronously """
    #try:
        #process_delete_data_upload.spool(dataUploadID, dataUploadRecord)
    #except:
    _process_delete_data_upload(data_upload_record)
    
    return JsonResponse({"success":'true'})

class uploadBurialRecordPhotosView(AdminView, FormView):
    """
    GET request: Redirects to /uploadBurialRecordPhotos from the upload data tools option.
    POST request: Validates file name to have the following input mask:
                  {SITE REFERENCE}_{YEAR FROM}-{YEAR TO}_{PAGE NO}.jpg e.g. 3244_1867-1952_168.jpg
                  or
                  {SITE REFERENCE}_{BOOK REFERENCE}_{TOP GRAVE NO}.jpg e.g. 3244_A_00168.jpg
                  Only if valid case the photo is uploaded. Otherwise it shows and error to the user for that file.
    """

    form_class = UploadBurialRecordPhotosForm
    def get(self, request):
        upload_photos_form = self.form_class()
        return render(request, 'admin/burial_record/upload_mass_photos.html',  {'form': upload_photos_form, 'user': request.user, 'site_header': bgsite.admin.tenant_admin_site.site_header,'has_permission': bgsite.admin.tenant_admin_site.has_permission(request), 'site_url': bgsite.admin.tenant_admin_site.site_url})

    def post(self, request):
        upload_photos_form = self.form_class(request.POST)
        if upload_photos_form.is_valid():
            if len(request.FILES.getlist('qqfile')) > 0:
                # import pdb; pdb.set_trace()
                result = Burial.objects.upload_photos(request.FILES.getlist('qqfile'), upload_photos_form.data['filename_format'])
                # import pdb; pdb.set_trace()
                if len(result['error']) > 0:
                    #[0] due to change for using fineupload pluging only processing one by one image, therefore only one error to return.
                    return JsonResponse({"error": result['error'][0]})
                else:
                    return JsonResponse({"success":'true'})
            else:
                result = {'error': ['Please upload at least one file']}
                return render(request, 'admin/upload_mass_photos_error.html', {'errors': result['error'], 'user': request.user, 'site_header': bgsite.admin.tenant_admin_site.site_header, 'has_permission': bgsite.admin.tenant_admin_site.has_permission(request), 'site_url': bgsite.admin.tenant_admin_site.site_url})
        return JsonResponse({"success": 'false'})


class uploadOwnershipRegisterPhotosView(AdminView, FormView):
    """
    GET request: Redirects to /uploadOwnershipRegisterPhotos from the upload data tools option.
    POST request: Validates file name to have the following input mask:
                  {SITE REFERENCE}_{BOOK REFERENCE}_{TOP GRAVE NO}.jpg e.g. 3244_A_00168.jpg
                  Only if valid case the photo is uploaded. Otherwise it shows and error to the user for that file.
    """

    form_class = UploadOwnershipRegisterPhotosForm
    def get(self, request):
        upload_photos_form = self.form_class()
        return render(request, 'admin/ownership_registry/upload_mass_ownership_registry_photos.html',  {'form': upload_photos_form, 'user': request.user, 'site_header': bgsite.admin.tenant_admin_site.site_header,'has_permission': bgsite.admin.tenant_admin_site.has_permission(request), 'site_url': bgsite.admin.tenant_admin_site.site_url})

    def post(self, request):
        upload_photos_form = self.form_class(request.POST)
        if upload_photos_form.is_valid():
            if len(request.FILES.getlist('qqfile')) > 0:
                # import pdb; pdb.set_trace()
                result = GraveDeed.objects.upload_photos(request.FILES.getlist('qqfile'))
                # import pdb; pdb.set_trace()
                if len(result['error']) > 0:
                    #[0] due to change for using fineupload pluging only processing one by one image, therefore only one error to return.
                    return JsonResponse({"error": result['error'][0]})
                else:
                    return JsonResponse({"success":'true'})
            else:
                result = {'error': ['Please upload at least one file']}
                return render(request, 'admin/upload_mass_photos_error.html', {'errors': result['error'], 'user': request.user, 'site_header': bgsite.admin.tenant_admin_site.site_header, 'has_permission': bgsite.admin.tenant_admin_site.has_permission(request), 'site_url': bgsite.admin.tenant_admin_site.site_url})
        return JsonResponse({"success": 'false'})


class addUserPermissions(AdminView, FormView):
    """
    GET request: Redirects to /addUserPermissions from add teant user (site user).
    POST request:
    """

    form_class = addPermissionsForm
    # success_url = '/mapmanagement'
    # def get(self, request):
        # return render(request, 'admin/user/add_permissions1.html',  {'form': self.form_class()})

    def post(self, request):
        # import pdb; pdb.set_trace()
        form = self.form_class(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if BGUser.objects.filter(username=form_data['username']).exists():
                user = BGUser.objects.get(username=form_data['username'])
                user.add_me_current_site_connection()
                user.email_user('BGMS site access', 'mail_templated/site_user_added.tpl', {'site_url':BurialGroundSite.get_login_domain_url(), 'site_name':BurialGroundSite.get_name()})

                return JsonResponse({"url": '/siteadminportal/main/tenantuser/{0}/'.format(user.id)})
            else:
                return JsonResponse({"url": ''})
        else:
            print('invalid data addUserPermissions view')
            return super(addUserPermissions, self).form_invalid(form)


class sendEmailInvitationView(AjaxableResponseMixin, AdminView, FormView):
    """
    POST request: send email invitation to register to BGMS site
    """
    template_name = 'admin/user/add_permissions.html'
    form_class = sendEmailInvitationForm
    success_url = '/register'

    def form_valid(self, form):
        form_data = form.cleaned_data
        email_non_user(form_data['email_invitation'], 'BGMS Invitation to register', 'mail_templated/email_invitation.tpl',{'url_button':BurialGroundSite.get_register_domain_url()})
        return JsonResponse({"status": 'ok'})

    def form_invalid(self, form):
        return super(sendEmailInvitationView, self).form_invalid(form)
