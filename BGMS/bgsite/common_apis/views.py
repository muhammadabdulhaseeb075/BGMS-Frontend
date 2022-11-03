from datetime import datetime, date

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from bgsite.common_apis.serializers import GraveOwnersListSerializer, MemorialInscriptionSerializer
from bgsite.models import GravePlot, GraveOwner, Memorial, MemorialInscriptionDetail, GraveplotType
from bgsite.views import group_required
from config.security.drf_permissions import BereavementStaffPermission
from main.models import PublicPerson, Company as PublicCompany, Address as PublicAddress
from main.serializers import PersonSerializer, CompanySerializer, PublicAddressSerializer

class GraveplotTypesListView(APIView):
    """
    API view for returning a list of all graveplot types
    """

    def get(self, request):
        """ Return grave types ordered by type """
        return JsonResponse({
            'type': list(GraveplotType.objects.all().values('id', 'type').order_by('type')),
            }, safe=False)

class CurrentPersonGraveOwnersListView(ListAPIView):
    """
    Returns list of owners for a grave
    """

    serializer_class = GraveOwnersListSerializer
    permission_classes = [BereavementStaffPermission]

    def get_queryset(self):
        """
        Return persons who are current owners of grave
        """

        graveplot_id = self.kwargs['graveplot_id']
        graveplot = GravePlot.objects.get(id=graveplot_id)

        return GraveOwner.objects.filter(Q(deed__graveplot_id=graveplot.id) & Q(content_type__model='publicperson') & Q(active_owner=True) & (Q(owner_to_date__isnull=True) | Q(owner_to_date__gte=datetime.now())))


class MemorialInscriptionsView(APIView):

    def post(self, request):

        serializer = MemorialInscriptionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def get(self, request):

        memorial_uuid = request.GET.get('memorial_uuid')

        if not memorial_uuid:
            return HttpResponseBadRequest("Memorial not specified")

        memorial = Memorial.objects.get_from_uuid(memorial_uuid)

        if memorial:
            memorial_inscriptions = MemorialInscriptionDetail.objects.filter(memorial=memorial)
            serializer = MemorialInscriptionSerializer(memorial_inscriptions, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            return HttpResponseBadRequest("Memorial does not exist")

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def delete(self, request):
        memorial_inscription_id = request.query_params.get('id')

        if not memorial_inscription_id:
            memorial_inscription_id = request.data.get('id')
        memorial_inscription = MemorialInscriptionDetail.objects.get(id=memorial_inscription_id)

        if memorial_inscription:
            memorial_inscription.delete()
            return HttpResponse(status=204)
        else:
            return HttpResponseBadRequest("Memorial inscription does not exist")

class PublicPersonView(APIView):

    def update_person(self, person, data, user):
        serializer = PersonSerializer(person, data=data, partial=True)
        if serializer.is_valid():
            serializer.save(last_edit_by=user)

            return serializer.data
        else:
            print(serializer.errors)
            raise ValidationError(serializer.errors)

    def get(self, request):

        person_id = request.GET.get('id')

        if not person_id:
            # this is new person record
            person = PublicPerson()
        else:
            try:
                person = PublicPerson.objects.prefetch_related('addresses').get(id=person_id)
            except Exception as e:
                print(e)
                return HttpResponseBadRequest("Person does not exist:" + str(e))

        serializer = PersonSerializer(instance=person)
        return JsonResponse(serializer.data, safe=False)
    
    """ POST /api/person - only sites """
    """ Create a new public person """
    def post(self, request):
        data = request.data
        person = PublicPerson(
          title=data.get("title"),
          first_names=data.get("forename"),
          last_name=data.get("surname"),
          email=data.get("email")
        )

        serializer = PersonSerializer(instance=person)
        return JsonResponse(serializer.data, safe=False)

      
    
    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def patch(self, request):

        data = request.data

        if not data.get('id'):
            return HttpResponseBadRequest("Person not specified")

        try:
            person = PublicPerson.objects.prefetch_related('addresses').get(id=data.get('id'))
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Person does not exist:" + e)

        if person:
            try:
                return Response(self.update_person(person, data, request.user))

            except Exception as e:
                print(e)
                return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseBadRequest("Person does not exist")

class PublicCompanyView(APIView):

    def update_company(self, company, data, user):
        serializer = CompanySerializer(company, data=data, partial=True)
        if serializer.is_valid():
            serializer.save(last_edit_by=user)

            return serializer.data
        else:
            print(serializer.errors)
            raise ValidationError(serializer.errors)

    def get(self, request):

        company_id = request.GET.get('id')

        if not company_id:
            # this is new company record
            company = PublicCompany()
        else:
            try:
                company = PublicCompany.objects.prefetch_related('addresses').get(id=company_id)
            except Exception as e:
                print(e)
                return HttpResponseBadRequest("Company does not exist:" + e)

        serializer = CompanySerializer(instance=company)
        return JsonResponse(serializer.data, safe=False)

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def patch(self, request):

        data = request.data

        if not data.get('id'):
            return HttpResponseBadRequest("Company not specified")

        try:
            company = PublicCompany.objects.prefetch_related('addresses').get(id=data.get('id'))
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Company does not exist:" + e)

        if company:
            try:
                return Response(self.update_company(company, data, request.user))

            except Exception as e:
                print(e)
                return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseBadRequest("Company does not exist")

class PublicAddressView(APIView):

    def new_address(self, data, person_id=None, company_id=None):

        address = PublicAddress.objects.create()

        serializer = PublicAddressSerializer(address, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

            if person_id:
                person = PublicPerson.objects.get(id=person_id)
                person.addresses.add(address)
                person.save()

            if company_id:
                company = PublicCompany.objects.get(id=company_id)
                company.addresses.add(address)
                company.save()

            return serializer.data
        else:
            print(serializer.errors)
            raise ValidationError(serializer.errors)

    def get(self, request):

        address_id = request.GET.get('id')

        if not address_id or address_id == 'null':
            # create new address
            address = PublicAddress()
        else:
            try:
                address = PublicAddress.objects.get(id=address_id)
            except Exception as e:
                print(e)
                return HttpResponseBadRequest("Address does not exist:" + e)

            # if current field needs updated
            if address.current is True and address.to_date and address.to_date < date(datetime.now().year, datetime.now().month, datetime.now().day):
                address.current = False
                address.save()

        serializer = PublicAddressSerializer(instance=address)
        return JsonResponse(serializer.data, safe=False)

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def patch(self, request):

        data = request.data

        if not data.get('id'):
            print("Address ID not specified")
            return HttpResponseBadRequest("Address ID not specified")

        try:
            address = PublicAddress.objects.get(id=data.get('id'))
        except Exception as e:
            print(e)
            return HttpResponseBadRequest("Address does not exist:" + e)

        serializer = PublicAddressSerializer(address, data=data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()

                return Response(serializer.data)
            except ValidationError as e:
                print(e)
                return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def post(self, request):

        data = request.data

        try:
            person_id = None
            if 'person_id' in data:
                person_id = data.get('person_id')
            company_id = None
            if 'company_id' in data:
                company_id = data.get('company_id')
            return Response(self.new_address(data, person_id, company_id))

        except Exception as e:
            print(e)
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
