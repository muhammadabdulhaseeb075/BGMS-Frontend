from bgsite.models import Image
from bgsite.views import group_required

from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator

from geometries.models import TopoPolygons, TopoPolylines, TopoPoints
from geometriespublic.models import FeatureCode

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from survey.models import Survey, SurveyField, TopoPolygonSurvey, TopoPolylineSurvey, TopoPointSurvey
from survey.serializers import SurveysListSerializer, LayerSurveyTemplatesSerializer, SurveySerializer, MasterTemplateSerializer
from surveypublic.models import MasterSurveyTemplate

import traceback

class SurveyView(APIView):

    def get(self, request):
        """
        Get a survey using survey_id
        """

        data=request.GET

        try:
            if not 'survey_id' in data:
                raise ValidationError("Survey id not specified")
            
            survey = Survey.objects.prefetch_related('survey_fields').get(id=data['survey_id'])

            # get fields with data
            survey_serializer = SurveySerializer(instance=survey)
            survey_serialized_data = survey_serializer.data

            # get all fields in template
            survey_template_serializer = LayerSurveyTemplatesSerializer(instance=survey.survey_template, read_only=True)
            survey_template_serialized_data = survey_template_serializer.data

            for field in survey_template_serialized_data['fields']:

                # look for an existing value for this field
                field_with_value = [f for f in survey_serialized_data['fields'] if f['survey_template_field_id']==field['survey_template_field_id']]
                if any(field_with_value):
                    # if a value exists for this field
                    field['value'] = field_with_value[0]['value']
                    field['survey_field_id'] = field_with_value[0]['survey_field_id']
                else:
                    field['value'] = None
                    field['survey_id'] = survey.id

                if field['field_type'] == 'date':
                    if field['value']:
                        date = field['value']
                        field['day'] = date.day if date else None
                        field['month'] = date.month if date else None
                        field['year'] = date.year if date else None
                    else:
                        field['day'] = None
                        field['month'] = None
                        field['year'] = None

            return JsonResponse(survey_template_serialized_data, safe=False)
    
        except Exception as e:
            print(traceback.format_exc())
            return HttpResponseBadRequest(str(e))
    
    def setFieldAttribute(self, survey_field, field):

        if field['field_type'] == 'image':
            if not field['value']:
                # delete image
                survey_field.image_value = None
            elif 'thumbnail_url' in field['value']:
                # add/replace image
                image = field['value']['thumbnail_url'].replace("data:image/jpeg;base64,", "")
                if image is not None:
                    survey_field.create_image(Image.base64_to_image(image))
        else:
            # set survey field value
            setattr(survey_field, field['field_type'] + '_value', field['value'])
        
        survey_field.save()

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    @transaction.atomic
    def patch(self, request):
        """
        Patch an existing survey
        """

        data=request.data

        try:
            if not 'fields' in data:
                raise ValidationError("Survey fields not specified")

            for field in data['fields']:

                if not 'survey_field_id' in field:
                    survey_field = SurveyField.objects.create(survey_id=field['survey_id'], survey_template_field_id=field['survey_template_field_id'])
                else:
                    survey_field = SurveyField.objects.get(id=field['survey_field_id'])

                self.setFieldAttribute(survey_field, field)

            return HttpResponse(status=204)
    
        except Exception as e:
            print(traceback.format_exc())
            return HttpResponseBadRequest(str(e))

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    @transaction.atomic
    def post(self, request):
        """
        Post a new survey
        """

        data=request.data

        try:
            # this is the id from feature model
            if not 'feature_id' in data:
                raise ValidationError("Feature id not specified")

            if not data.get('fields'):
                raise ValidationError("Survey fields not specified")

            if not data.get('survey_template_id'):
                raise ValidationError("Survey template not specified")

            survey = Survey.objects.create(survey_template_id=data.get('survey_template_id'))
        
            fields = data.get('fields')

            for field in fields:
                ''' create a new survey field '''

                if not field['survey_template_field_id']:
                    raise ValidationError("Survey template field not specified")

                survey_field = SurveyField.objects.create(survey=survey, survey_template_field_id=field['survey_template_field_id'])
                self.setFieldAttribute(survey_field, field)
            
            # Link survey to feature. Don't know what feature type, so try all.
            try:
                topopolygon = TopoPolygons.objects.get(id=data['feature_id'])
                TopoPolygonSurvey.objects.create(topopolygon=topopolygon, survey=survey)
            except:
                try:
                    topopolyline = TopoPolylines.objects.get(id=data['feature_id'])
                    TopoPolylineSurvey.objects.create(topopolyline=topopolyline, survey=survey)
                except:
                    try:
                        topopoint = TopoPoints.objects.get(id=data['feature_id'])
                        TopoPointSurvey.objects.create(topopoint=topopoint, survey=survey)
                    except:
                        raise ValidationError("Feature not found")

            return JsonResponse({ 'survey_id': survey.id }, safe=False)
    
        except Exception as e:
            print(traceback.format_exc())
            return HttpResponseBadRequest(str(e))

    @method_decorator(group_required('SiteWarden', 'SiteAdmin', raise_exception=True,))
    def delete(self, request):
        """
        Delete a survey using survey_id
        """

        data=request.GET

        try:
            if not 'survey_id' in data:
                raise ValidationError("Survey id not specified")
            
            # don't actually delete the survey, instead, set deleted flag to true
            survey = Survey.objects.get(id=data['survey_id'])
            survey.deleted = True
            survey.save()

            return HttpResponse(status=204)
    
        except Exception as e:
            print(traceback.format_exc())
            return HttpResponseBadRequest(str(e))

class FeatureSurveysListView(APIView):

    def get(self, request):
        """
        Get a list of existing surveys for a feature (empty list if none)
        """

        try:
            # this is the id from feature model
            feature_id = request.GET.get('feature_id')

            if feature_id:
                # feature could be TopoPolygon, TopoPolyline or TopoPoint
                try:
                    topopolygon = TopoPolygons.objects.get(id=feature_id)
                    surveys = Survey.objects.filter(deleted=False, topopolygon_surveys__topopolygon=topopolygon)
                except:
                    try:
                        topopolyline = TopoPolylines.objects.get(id=feature_id)
                        surveys = Survey.objects.filter(deleted=False, topopolyline_surveys__topopolyline=topopolyline)
                    except:
                        try:
                            topopoint = TopoPoints.objects.get(id=feature_id)
                            surveys = Survey.objects.filter(deleted=False, topopoint_surveys__topopoint=topopoint)
                        except:
                            return HttpResponseBadRequest("Feature ID not recognised")
            else:
                return HttpResponseBadRequest("Feature not specified")

            serializer = SurveysListSerializer(instance=surveys, many=True, read_only=True)

            # sort surveys so newest comes first
            data_sorted = sorted(serializer.data, key=lambda x: x['survey_date'], reverse=True)

            return JsonResponse(data_sorted, safe=False)

        except Exception as e:
            print(traceback.format_exc())
            return HttpResponseBadRequest(str(e))

class LayerSurveyTemplatesView(APIView):

    def get(self, request):
        """
        Get a list of survey templates available to a feature
        """

        try:
            feature_type = request.GET.get('layer')

            if feature_type:
                survey_templates = FeatureCode.objects.get(feature_type=feature_type).survey_templates.filter(active=True).prefetch_related('fields').all().order_by('name')

            else:
                return HttpResponseBadRequest("Layer not specified")

            serializer = LayerSurveyTemplatesSerializer(instance=survey_templates, many=True, read_only=True)

            serialized_data = serializer.data

            for template in serialized_data:
                for field in template['fields']:
                    field['value'] = None

                    if field['field_type'] == 'date':
                        field['day'] = None
                        field['month'] = None
                        field['year'] = None

            return JsonResponse(serialized_data, safe=False)

        except Exception as e:
            print(traceback.format_exc())
            return HttpResponseBadRequest(str(e))

class LayerSurveyTemplatesExistView(APIView):

    def get(self, request):
        """
        Finds out of at least one survey template exists for a layer
        """
        
        try:
            survey_exists = False

            feature_type = request.GET.get('layer')

            if feature_type:
                survey_exists = FeatureCode.objects.get(feature_type=feature_type).survey_templates.exists()
            else:
                return HttpResponseBadRequest("Layer not specified")

            return JsonResponse({'surveyExists': survey_exists}, safe=False)

        except Exception as e:
            print(traceback.format_exc())
            return HttpResponseBadRequest(str(e))


class MasterTemplateView(APIView):

    def get(self, request, format=None):
        queryset = MasterSurveyTemplate.objects.get(id=request.GET.get('id'))
        serializer = MasterTemplateSerializer(queryset)
        return Response(serializer.data)