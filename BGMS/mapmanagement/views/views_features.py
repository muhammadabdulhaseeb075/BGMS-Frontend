from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from django.http.response import JsonResponse, HttpResponseBadRequest

from bgsite.models import Memorial, GravePlot, Section, Subsection, GraveRef
from bgsite.views import WardenView
from geometries.models import TopoPolygons, Layer
from geometries.serializers import TopoPolygonGeoSerializer
from geometries.utils import getGeojson
from geometriespublic.models import FeatureGroup

import json
import traceback

# Iterates through list of plots and links to section/subsection if they are contained in one.
# If plots argument is missing, all plots will be used.
def linkPlotsToSection(plots=[], detailed_error_message=True):
    if not plots:
        feature_group = FeatureGroup.objects.filter(group_code='plots')
        print(feature_group[0])
        plots = TopoPolygons.objects.all().filter(layer__feature_code__feature_groups__in=feature_group)

    sections = Section.objects.exclude(topopolygon__isnull=True)
    subsections = Subsection.objects.exclude(topopolygon__isnull=True)
    
    section_linked_count = 0
    section_partial_linked_count = 0
    subsection_linked_count = 0
    subsection_partial_linked_count = 0
    not_saved = []

    if sections or subsections:
        for plot in plots:
        
            graveplot,created = GravePlot.objects.select_related('topopolygon').get_or_create(topopolygon=plot)
            
            max_intersecting_area = 0
            
            # **** Sections ****
            
            partially_in = False
            new_section = None
            
            for section in sections:
                # if graveplot is completely contained within section
                if section.topopolygon.geometry.contains(graveplot.topopolygon.geometry):
                    new_section = section
                    break
                # if graveplot is partially contained within section
                elif section.topopolygon.geometry.overlaps(graveplot.topopolygon.geometry):
                    intersection = graveplot.topopolygon.geometry.intersection(section.topopolygon.geometry)
                    
                    # if most of graveplot is contained within section
                    if intersection.area > (graveplot.topopolygon.geometry.area / 2):
                        new_section = section
                        partially_in = True
                        break
                    # if less than 50% is contained within section but this is the biggest intersection yet
                    elif intersection.area > max_intersecting_area:
                        new_section = section
                        partially_in = True
                        max_intersecting_area = intersection.area
            
            if not graveplot.graveref or new_section != graveplot.graveref.section:
                section_linked_count += 1
                
                if partially_in:
                    section_partial_linked_count += 1

            # **** Subsections ***
            
            partially_in = False
            new_subsection = None
            
            for subsection in subsections:
                # if graveplot is completely contained within subsection
                if subsection.topopolygon.geometry.contains(graveplot.topopolygon.geometry):
                    new_subsection = subsection
                    break
                # if graveplot is partially contained within subsection
                elif subsection.topopolygon.geometry.overlaps(graveplot.topopolygon.geometry):
                    intersection = graveplot.topopolygon.geometry.intersection(subsection.topopolygon.geometry)
                    
                    # if most of graveplot is contained within subsection
                    if intersection.area > (graveplot.topopolygon.geometry.area / 2):
                        new_subsection = subsection
                        partially_in = True
                        break
                    # if less than 50% is contained within subsection but this is the biggest intersection yet
                    elif intersection.area > max_intersecting_area:
                        new_subsection = subsection
                        partially_in = True
                        max_intersecting_area = intersection.area
            
            if not graveplot.graveref or new_subsection != graveplot.graveref.subsection:
                subsection_linked_count += 1
                
                if partially_in:
                    subsection_partial_linked_count += 1
            
            try:
                if graveplot.graveref and graveplot.graveref.grave_number:
                    # if a graveref already exists, modify it

                    if graveplot.graveref.grave_number == '':
                        # blank grave numbers should always be null rather than blank
                        graveplot.graveref.grave_number = None
                    
                    graveplot.graveref.section = new_section
                    graveplot.graveref.subsection = new_subsection
                    graveplot.graveref.save()
                
                elif new_section:
                    # need to add graveref relationship

                    grave_ref = GraveRef.objects.filter(grave_number=None, section=new_section, subsection=new_subsection)

                    if not grave_ref.exists() or hasattr(grave_ref[0], 'graveref_graveplot'):
                        # if graveref already existed, but belongs to another grave
                        # (this is possible when graves have no grave_number but are in a section)
                        grave_ref = GraveRef.objects.create(grave_number=None, section=new_section, subsection=new_subsection)
                    else:
                        grave_ref = grave_ref[0]

                    graveplot.graveref = grave_ref
                    graveplot.save()

            except ValidationError as e:
                if 'already exists' in e.messages[0] or 'Duplicate' in e.messages[0]:
                    message = ""
                    # a graveplot with this ref already exists
                    if detailed_error_message:
                        message = "Error changing section/subsection for graveplot_uuid: " + str(graveplot.uuid) + "; " + "burials: "
                        
                        burials = graveplot.burials.all()
                        
                        if burials.count() == 0:
                            message += 'None'
                        else:
                            for i in range(burials.count()):
                                if i > 0:
                                    message += ", "
                                message += burials[i].death.person.first_names + " " + burials[i].death.person.last_name
                                
                        message += ". "
                    
                    message += "A graveplot with this grave number, section and subsection already exists."
                    
                    not_saved.append(message)
                    print(message)
                        
                else:
                    print(e.messages)
            
    return section_linked_count, section_partial_linked_count, subsection_linked_count, subsection_partial_linked_count, not_saved

class AddAvailablePlot(WardenView):

    def post(self, request):
        response = request.body.decode()
#         print(response)
        geojson_feature = json.loads(response)['geojsonFeature']
        geojson_polygon = json.dumps(json.loads(geojson_feature)['geometry'])
        print(geojson_polygon)
        plot = TopoPolygons.objects.get_or_create_from_geojson(geojson_feature)[0]

        # look to see if this plot needs linked to a section
        result = linkPlotsToSection([plot], False)

        geoj = TopoPolygonGeoSerializer(TopoPolygons.objects.get(id=plot.id), context={ 'marker_type': plot.layer.feature_code.feature_type }).data

        return JsonResponse({'geometry':geoj, 'updated_section':result[0]>0, 'updated_subsection':result[2]>0}, content_type ='application/json', safe=False)


class UpdatePlot(WardenView):
    @transaction.atomic
    def post(self, request):
        response = request.body.decode()
#         print(response)
        geojson_feature = json.loads(response)['geojsonFeature']
        properties = json.loads(geojson_feature)['properties']
        feature_id = json.loads(geojson_feature)['id']
        # import pdb; pdb.set_trace()
        try:
            with transaction.atomic():
                plot = None
                graveplot = GravePlot.objects.select_related('topopolygon').get_from_uuid(feature_id)
                if graveplot:
                    plot = graveplot.topopolygon
                else:
                    plot = TopoPolygons.objects.get_or_create_from_geojson(geojson_feature)[0]

                geojson_polygon = getGeojson(geojson_feature)
                plot.update_geometry(geometryGeoJSON=geojson_polygon)
            
                # update section/subsection if new location
                result = linkPlotsToSection([plot], False)
                
                if len(result[4]) > 0:
                    # update section/subsection has been unsuccessful
                    raise ValidationError("Error linking to section/subsection")
        except ValidationError:
            print(result[4][0])
            return JsonResponse({'error_updating_section':result[4][0]}, status=500)
            
        except (ValueError, ObjectDoesNotExist):
            print('Could not update plot')
            print(traceback.format_exc())
            return HttpResponseBadRequest(properties['marker_type'])

        geoj = TopoPolygonGeoSerializer(plot, context={ 'marker_type': properties['marker_type'] }).data

        return JsonResponse({'geometry':geoj, 'updated_section':result[0]>0, 'updated_subsection':result[2]>0}, content_type ='application/json', safe=False)

class DeletePlot(WardenView):

    def post(self, request):
        response = request.body.decode()
        plot_id = json.loads(response)['plot_id']
        layer_name = json.loads(response)['layer_name']
        
        #deleting limited only to available plot and reserved plot layer_name

        if layer_name == 'available_plot':
            # plot = TopoPolygons.objects.get(pk=plot_id)
            
            if  TopoPolygons.objects.filter(id=plot_id).exists():
                plot = TopoPolygons.objects.get(id=plot_id)
            else:
                plot = GravePlot.objects.get(uuid=plot_id).topopolygon

        elif layer_name == 'reserved_plot':
            # import pdb; pdb.set_trace()
            grave_plot = GravePlot.objects.get_from_uuid(plot_id)
            grave_plot.delete_reserved_plot()
            plot = grave_plot.topopolygon
            
        plot.delete_feature(feature_type=layer_name)

        return JsonResponse({'plot_id':plot_id}, content_type = 'application/json')


class UpdateMemorial(WardenView):

    def post(self, request, *args, **kwargs):
        response = request.body.decode()
        # print(response)
        # print(self.kwargs)
        geojson_feature = json.loads(response)['geojsonFeature']
        properties = json.loads(geojson_feature)['properties']
        feature_id = json.loads(geojson_feature)['id']
        try:
            topopolygon = None
            memorial = Memorial.objects.get_from_uuid(feature_id)
            if memorial:
                topopolygon = memorial.topopolygon

            geojson_polygon = getGeojson(geojson_feature)
            topopolygon.update_geometry(geometryGeoJSON=geojson_polygon)
            topopolygon.update_feature_code(feature_type=properties['marker_type'])
            topopolygon.save()
        except (ValueError, ObjectDoesNotExist):
            print('could not update plot')

        geoj = memorial.get_geojson()

        return JsonResponse(geoj, safe=False)