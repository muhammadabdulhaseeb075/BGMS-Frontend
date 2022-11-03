import xlwt
import json
import datetime
from django.core import serializers
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from bgsite.views import ViewOnlyView
from main.models import ReportTemplate
from analytics.register import Register
from analytics.models import Report

from rest_framework.views import APIView

register = Register()
    
# Create your views here.
class AnalyticsView(ViewOnlyView, TemplateView):
    template_name = 'index.html'

class ModelsFields(APIView):
    def get(self, request):
        values = register.get_models_with_fields()
        return JsonResponse(values, safe=False)

class ModelEntriesByField(ViewOnlyView):
    def get(self, request, model_name):
        fields_query = request.GET.get('fields')
        fields = fields_query.split(',')
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 20)
        sort = request.GET.get('sort', '')
        all_records = register.get_entries_by_field(
            model_name,
            fields,
            sort
        )
        paginator = Paginator(all_records, limit)
        entries = list(paginator.get_page(page).object_list)
        response = JsonResponse(entries, safe=False)
        response.setdefault('PAGINATION_NUM_PAGES', paginator.num_pages)
        response.setdefault('TOTAL_RECORDS', len(all_records))

        return response
    
    def post(self, request, model_name):
        payload = json.loads(request.body.decode())
        fields_list = payload.get('fields')
        fields = fields_list.split(',')
        filters = payload.get('filters', None)
        page = payload.get('page', 1)
        limit = payload.get('limit', 20)
        sort = payload.get('sort', '')
        all_records = register.get_entries_by_field(
            model_name,
            fields,
            sort,
            filters
        )
        paginator = Paginator(all_records, limit)
        entries = list(paginator.get_page(page).object_list)
        response = JsonResponse(entries, safe=False)
        response.setdefault('PAGINATION_NUM_PAGES', paginator.num_pages)
        response.setdefault('TOTAL_RECORDS', len(all_records))

        return response

class FilterSuggestion(ViewOnlyView):
    def get(self, request, model_name):
        field_filter_query = request.GET.get('field')
        field_suggestion = list(register.get_field_suggestion_by_model(
            model_name,
            field_filter_query
        ))
        print(field_filter_query, field_suggestion)
        return JsonResponse(field_suggestion, safe=False)

class GetAllReports(ViewOnlyView):
    def get(self, request):
        reports = list(Report.objects.all().values(
            'id', 'name', 'table_schema', 'creation_date'
        ))
        response = JsonResponse(reports, safe=False)
        response.setdefault('IS_SUPERUSER', True)

        return response
    
    def post(self, request):
        payload = json.loads(request.body.decode())
        report = Report(name=payload['name'], table_schema=payload['tableSchema'])
        report.save()
        response = model_to_dict(report)

        return JsonResponse(response, safe=False)

class UpdateOneReport(ViewOnlyView):
    def put(self, request, id):
        payload = json.loads(request.body.decode())
        report = Report.objects.get(id=id)
        report.name = payload['name']
        report.table_schema = payload['tableSchema']
        report.save()
        response = model_to_dict(report)

        return JsonResponse(response, safe=False)

class ReportTemplatesView(ViewOnlyView):
    def get(self, request):
        print("report template view")
        report_templates = list(ReportTemplate.objects.all().values(
            'id', 'name', 'table_schema', 'creation_date'
        ))
        response = JsonResponse(report_templates, safe=False)
        response.setdefault('IS_SUPERUSER', True)
        
        return response
    
    def post(self, request):
        payload = json.loads(request.body.decode())
        report = ReportTemplate(name=payload['name'], table_schema=payload['tableSchema'])
        report.save()
        response = model_to_dict(report)

        return JsonResponse(response, safe=False)

class ExcelExport(ViewOnlyView):
    def get(self, request, id):
        report = Report.objects.get(id=id)
        reportDict = model_to_dict(report)
        print(reportDict)
        report_name = reportDict['name']
        table_schema = reportDict['table_schema']
        model_name = table_schema['selectedModelName']
        fields = table_schema['headers']
        all_records = list(register.get_entries_by_field(
            model_name,
            fields,
            '',
            None
        ))

        print(all_records[0])
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="report.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(report_name)
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        for header_index in range(len(fields)):
            ws.write(row_num, header_index, fields[header_index], font_style)
        
        font_style = xlwt.XFStyle()
        for row in all_records:
            row_num += 1
            for col_num in range(len(fields)):
                col_name = fields[col_num]
                value = row[col_name]

                ws.write(row_num, col_num, str(value), font_style)

        wb.save(response)

        return response
