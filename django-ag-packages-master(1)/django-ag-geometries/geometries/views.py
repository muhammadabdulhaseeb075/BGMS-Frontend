from django.http import HttpResponse, HttpResponseForbidden

from geometries.models import TopoPolylines, TopoPoints, TopoPolygons, Layer, FeatureAttributes
from geometries.serializers import TopoPolygonGeoSerializer, TopoPolylineGeoSerializer, TopoPointGeoSerializer
from geometries.utils import CRS
from bgsite.views import ViewOnlyView, AdminView, PublicAccessOrViewOnlyView

import json
json.encoder.FLOAT_REPR = lambda o: format(o, '.2f')
from django.http.response import JsonResponse, HttpResponseBadRequest
try:
    from bgsite.models import Memorial, GravePlot, MemorialGraveplot, Section, Subsection
except ImportError:
    pass

from django.views.generic.edit import FormView
from os.path import os
from django.contrib.gis.gdal.datasource import DataSource
from geometriespublic.models import FeatureCode, FeatureGroup, PublicAttribute
from django.contrib.gis.geos import MultiPolygon, MultiLineString, Point
import zipfile
from django.core.files.base import File
from geometries.forms import ShapeFileUpload
from django.conf import settings
from django.db.models import Q
from django.contrib.gis.gdal.geometries import Polygon
#from _ast import Str
from django.views.generic import View

import copy

# TODO this should come from database schemas
authenticated_only_layers = ['plots', 'furniture', 'utilities']

def getLayer(layer, authenticated_user):

    layer_obj = Layer.objects.get(feature_code__feature_type=layer)

    if not authenticated_user:
        group_code = layer_obj.feature_code.feature_groups.all()[0].group_code

        if group_code in authenticated_only_layers:
            return False

    layer_cache = layer_obj.get_layer_geojson_cache(True)

    if layer_cache:
        return layer_cache
    else:
        point_features = TopoPoints.objects.get_layer_label(layer, topopoint=True)
        line_features = TopoPolylines.objects.get_layer_label(layer)
        #TODO: remove customisation for grid
        # After re importing grid this method get_layer_label returns empty due label is uppercase in the attribute
        if layer.lower() == 'section':
            polygon_features = TopoPolygons.objects.get_layer(layer)
            for polygon in polygon_features:
                section = Section.objects.all().filter(topopolygon_id=polygon.get('id'))
                if section and len(section) > 0:
                    polygon['label'] = section[0].section_name
                else:
                    polygon['label'] = 'Section'
        elif layer.lower() == 'subsection':
            polygon_features = TopoPolygons.objects.get_layer(layer)
            for polygon in polygon_features:
                subsection = Subsection.objects.all().filter(topopolygon_id=polygon.get('id'))
                if subsection and len(subsection) > 0:
                    polygon['label'] = subsection[0].subsection_name
                else:
                    polygon['label'] = 'Section'
        else:
            polygon_features = TopoPolygons.objects.get_layer_label(layer)
        #TODO: remove customisation for trees & bushes
        if layer.lower() == 'tree':
            if polygon_features and len(polygon_features) > 0:
                point_features = TopoPolygons.objects.get_layer_label(layer, True)
                polygon_features = TopoPolygons.objects.none()
        elif layer.lower() == 'bush':
            if polygon_features and len(polygon_features) > 0:
                point_features = TopoPolygons.objects.get_layer_label(layer, True)
                polygon_features = TopoPolygons.objects.none()
        
        topopolypoint_geoj = None
        topopolyline_geoj = None
        topopolygon_geoj = None
        if(point_features and len(point_features) > 0):
            topopolypoint_geoj = TopoPointGeoSerializer(point_features, many=True).data
        if(line_features and len(line_features) > 0):
            topopolyline_geoj = TopoPolylineGeoSerializer(line_features, many=True).data
        if(polygon_features and len(polygon_features) > 0):
            topopolygon_geoj = TopoPolygonGeoSerializer(polygon_features, many=True).data

        geoj = { 'features': [], 'type': 'FeatureCollection' }

        # append features if from different topo types
        if topopolygon_geoj:
            geoj = topopolygon_geoj
        if topopolyline_geoj:
            if geoj:
                geoj['features'].extend(topopolyline_geoj['features'])
            else:
                geoj = topopolyline_geoj
        if topopolypoint_geoj:
            if geoj:
                geoj['features'].extend(topopolypoint_geoj['features'])
            else:
                geoj = topopolypoint_geoj
        
        geoj.update(CRS)

        layer_obj.update_layer_geojson_cache(geoj, True)

        return geoj


class LayerView(PublicAccessOrViewOnlyView):

    def get(self, request):
        layer = request.GET.get('layer', False)

        geoj = getLayer(layer, request.user and request.user.is_authenticated)

        if not geoj:
            return HttpResponseForbidden()
        else:
            return JsonResponse(geoj, safe=False)
        

def getGroupCodes(group):
    codes = None

    if group.group_code == 'memorials':
        # import pdb; pdb.set_trace()
        codes = group.feature_codes.filter(Q(layer__topopolygons__isnull=False, layer__topopolygons__memorial__isnull=False)).distinct('display_name', 'pk')
    elif group.group_code == 'memorial_cluster':
        codes = FeatureGroup.objects.filter(Q(group_code = 'memorials') | Q(group_code = 'plots')).filter(Q(feature_codes__layer__topopolygons__isnull=False, feature_codes__layer__topopolygons__memorial__isnull=False) | Q(feature_codes__layer__topopolygons__isnull=False, feature_codes__layer__topopolygons__graveplot__isnull=False)).distinct('display_name', 'pk')
        if codes.exists():
            codes = group.feature_codes.filter(feature_type='cluster').distinct('display_name', 'pk')
    else:
        # import pdb; pdb.set_trace()
        codes = group.feature_codes.filter(Q(layer__topopolygons__isnull=False) | Q(layer__topopolylines__isnull=False) |
                Q(layer__raster__isnull=False) | Q(layer__topopoints__isnull=False) | Q(type='raster')).distinct('display_name', 'pk')
        if group.group_code == 'plots':
            codes = codes | group.feature_codes.filter(Q(feature_type='available_plot') | Q(feature_type='reserved_plot')).distinct('display_name', 'pk')
            codes.distinct('display_name', 'pk')

    return codes
    

def getALLSiteLayerNamesMinimal():
    """Returns a json object containing the layer groups and names that exist for the site"""
    # TODO: optimise this method
    layers = []
    
    for group in FeatureGroup.objects.all().prefetch_related('feature_codes').order_by('hierarchy'):
        layer_group = {}
        codes = getGroupCodes(group)
        
        if codes:
            layer_group['group_code'] = group.group_code
            layer_group['layers'] = []
            codes = codes.distinct('feature_type', 'display_name').order_by('display_name')
            for code in codes:
                # only need this layer if it exists for the site
                if code.layer_set.first():
                    layer = {}
                    layer['layer_code'] = code.feature_type
                    layer['layer_type'] = code.type
                    layer_group['layers'].append(layer)
            layers.append(layer_group)
    return layers

    
class SiteLayerNames(PublicAccessOrViewOnlyView):

    def get(self, request):
        """Returns a json object containing the layer groups and names that exist for the site"""
        # TODO: optimise this method
        layers = []
        position = 0

        feature_groups = FeatureGroup.objects.all()

        if not (request.user and request.user.is_authenticated):
            feature_groups = feature_groups.exclude(group_code__in=authenticated_only_layers)

        for group in feature_groups.order_by('hierarchy'):
            layer_group = {}
            codes = getGroupCodes(group)
            
            if codes:
                layer_group['group_code'] = group.group_code
                layer_group['display_name'] = group.display_name
                layer_group['switch_on_off'] = group.switch_on_off
                layer_group['hierarchy'] = group.hierarchy
                layer_group['layers'] = []
                codes = codes.distinct('feature_type', 'display_name').order_by('display_name')
                for code in codes:
                    # only need this layer if it exists for the site
                    if code.layer_set.first():
                        layer = {}
                        layer['layer_code'] = code.feature_type
                        layer['layer_type'] = code.type
                        layer['display_name'] = code.layer_set.first().display_name
                        layer['initial_visibility'] = code.layer_set.first().initial_visibility
                        layer['min_resolution'] = code.layer_set.first().min_resolution
                        layer['max_resolution'] = code.layer_set.first().max_resolution
                        layer['show_in_toolbar'] = code.show_in_toolbar
                        layer['hierarchy'] = code.hierarchy
                        layer['attributes_exist'] = code.public_attributes.exists() or code.attributes.exists()
                        layer['surveys_exist'] = code.survey_templates.exists()
                        position+=1
                        layer_group['layers'].append(layer)
                layers.append(layer_group)
            result = {'layer_groups': layers, 'number_of_layers': position}
        response = JsonResponse(result, content_type ='application/json', safe=False)
        return response


class ImportShapeFile(AdminView, FormView):
    template_name = 'geometries/upload-shape-file.html'
    success_template_name = 'mapmanagement/edit/person-edit.html'
    success_url = '/mapmanagement'
    form_class = ShapeFileUpload

    def form_valid(self, form):

        #Remove old files from tmp directory
        temp_dir = getattr(settings, 'TEMP_FILES_UPLOAD_PATH')
        for the_file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, the_file)
            try:
                os.remove(file_path)
            except:
                print('Unable to delete old files')

        #unizip files and save them in tmp directory
        data = form.cleaned_data
        shp_file_zip = form.files['shp_file_zip']
        unzipped = zipfile.ZipFile(shp_file_zip)
        shape_file_paths = []
        for libitem in unzipped.namelist():
            path = temp_dir+libitem
            with open(path, 'wb') as f:
                filecontent = f.write(unzipped.read(libitem))
                if libitem.endswith('.shp'):
                    shape_file_paths.append(f.name)

        rel_mem_plot = {}
        #INI FOR shape_file_paths: loop shape files
        for shp_file in shape_file_paths:
            ds = DataSource(shp_file)
            if len(ds)==1:
                layer = ds[0]
                #INI FOR layer: loop features per layer (layer.name = shapefile name)
                for ogr_feature in layer:
                    ogr_feature_type = ogr_feature.geom.geom_type.name
                    print(ogr_feature.get('TYPE'))
                    feature_code = FeatureCode.objects.get(display_name=ogr_feature.get('TYPE'))

                    lyr = None
                    feature_object = None
                    #get or create layer
                    if not Layer.objects.filter(feature_code=feature_code).exists():
                        lyr = Layer.objects.create_layer_from_feature_type(feature_code.feature_type)
                    else:
                        lyr = Layer.objects.get(feature_code=feature_code)

                    if lyr != None:
                        # Removes cahce for this layer. It will be repopulated on the next load.
                        lyr.remove_layer_geojson_cache()

                        #INI SWITCH feature type
                        if ogr_feature_type == 'Polygon':
                            feature_object = TopoPolygons.objects.filter(id=ogr_feature.get('GlobalID')).first()
                            if not feature_object:
                                feature_object = TopoPolygons.objects.create(layer=lyr, feature_id=ogr_feature.get('ID'),                                                        geometry=MultiPolygon(ogr_feature.geom.geos), id=ogr_feature.get('GlobalID'))
                            else:
                                feature_object.geometry=MultiPolygon(ogr_feature.geom.geos)
                                feature_object.feature_id = ogr_feature.get('ID')
                                feature_object.layer = lyr
                                feature_object.save()
                            feature_object.addShapeFileAttributes(ogr_feature)
                        elif ogr_feature_type == 'MultiPolygon':
                            feature_object = TopoPolygons.objects.filter(id=ogr_feature.get('GlobalID')).first()
                            if not feature_object:
                                feature_object = TopoPolygons.objects.create(layer=lyr, feature_id=ogr_feature.get('ID'),
                                                        geometry=ogr_feature.geom.geos, id=ogr_feature.get('GlobalID'))
                            else:
                                feature_object.geometry=ogr_feature.geom.geos
                                feature_object.feature_id = ogr_feature.get('ID')
                                feature_object.layer = lyr
                                feature_object.save()
                            feature_object.addShapeFileAttributes(ogr_feature)

                        elif ogr_feature_type == 'LineString':
                            feature_object = TopoPolylines.objects.filter(id=ogr_feature.get('GlobalID')).first()
                            if not feature_object:
                                feature_object = TopoPolylines.objects.create(layer=lyr, feature_id=ogr_feature.get('ID'),
                                                        geometry=MultiLineString(ogr_feature.geom.geos), id=ogr_feature.get('GlobalID'))
                            else:
                                feature_object.geometry=MultiLineString(ogr_feature.geom.geos)
                                feature_object.feature_id = ogr_feature.get('ID')
                                feature_object.layer = lyr
                                feature_object.save()
                            feature_object.addShapeFileAttributes(ogr_feature)
                        elif ogr_feature_type == 'MultiLineString':
                            feature_object = TopoPolylines.objects.filter(id=ogr_feature.get('GlobalID')).first()
                            if not feature_object:
                                feature_object = TopoPolylines.objects.create(layer=lyr, feature_id=ogr_feature.get('ID'),
                                                        geometry=ogr_feature.geom.geos, id=ogr_feature.get('GlobalID'))
                            else:
                                feature_object.geometry=ogr_feature.geom.geos
                                feature_object.feature_id = ogr_feature.get('ID')
                                feature_object.layer = lyr
                                feature_object.save()
                            feature_object.addShapeFileAttributes(ogr_feature)
                        elif ogr_feature_type == 'Point':
                            feature_object = TopoPoints.objects.filter(id=ogr_feature.get('GlobalID')).first()
                            if not feature_object:
                                feature_object = TopoPoints.objects.create(layer=lyr, feature_id=ogr_feature.get('ID'),
                                                        geometry=ogr_feature.geom.geos, id=ogr_feature.get('GlobalID'))
                            else:
                                feature_object.geometry=ogr_feature.geom.geos
                                feature_object.feature_id = ogr_feature.get('ID')
                                feature_object.layer = lyr
                                feature_object.save()
                            feature_object.addShapeFileAttributes(ogr_feature)
                        #FIN SWITCH feature type
                        
                        if layer.name.lower() == 'section':
                            obj, created = Section.objects.get_or_create(section_name=ogr_feature.get('LABEL'))
                            obj.topopolygon = feature_object
                            obj.save()

                        elif layer.name.lower() == 'subsection':
                            section, created = Section.objects.get_or_create(section_name=ogr_feature.get('Section'))

                            if created:
                                section.topopolygon = feature_object
                                section.save()

                            obj, created = Subsection.objects.get_or_create(subsection_name=ogr_feature.get('LABEL'), section=section)
                            obj.topopolygon = feature_object
                            obj.save()

                        #INI Create memorials or plots, special cases
                        #create/update memorial or plot and assigned topopolygon
                        if ogr_feature.get('ID') != 0:
                            
                            feature_id = ogr_feature.get('ID')

                            if layer.name.lower() == 'plots':
                                # if plots don't exist, create them
                                obj = GravePlot.objects.filter(topopolygon_id=ogr_feature.get('GlobalID')).first()

                                if not obj:
                                    # don't use get_or_create as the topopolygon needs to be set at the start for 'update_GravePlotOrMemorial' to work properly
                                    try:
                                        obj = GravePlot.objects.get(feature_id=feature_id, memorial_feature_id=feature_id)
                                        obj.topopolygon = feature_object
                                        obj.save()
                                    except:
                                        obj = GravePlot.objects.create(feature_id=feature_id, memorial_feature_id=feature_id, topopolygon=feature_object)

                                #Append or create tuple (plot,polygon pk) to dictionary key:feature_id
                                if feature_id in rel_mem_plot and 'plot' in rel_mem_plot[feature_id]:
                                    # rel_mem_plot[feature_id].append(('plot',obj.id))
                                    print('ShapeFileUpload Error: Cannot append multiple Plots to same feature_id: ' + str(feature_id))
                                else:
                                    if feature_id in rel_mem_plot:
                                        rel_mem_plot[feature_id].update({'plot': [obj.id]})
                                    else:
                                        rel_mem_plot[feature_id] = {'plot': [obj.id]}

                            #Append or create tuple (mem,polygon pk) to dictionary key:feature_id
                            elif layer.name.lower() != 'plots':
                                # if memorials don't exists, create them (they can be related in any shapefile)
                                obj = Memorial.objects.filter(topopolygon_id=ogr_feature.get('GlobalID')).first()

                                if not obj:
                                    
                                    # don't use get_or_create as the topopolygon needs to be set at the start for 'update_GravePlotOrMemorial' to work properly
                                    try:
                                        obj = Memorial.objects.get(feature_id=feature_id)
                                        obj.topopolygon = feature_object
                                        obj.save()
                                    except:
                                        obj = Memorial.objects.create(feature_id=feature_id, topopolygon=feature_object)

                                # remove letter and append to dictionary, therefore can multiple relations (memorials-plot)
                                if not feature_id.isdigit():
                                    feature_id = ''.join(filter(lambda x: x.isdigit(), feature_id))
                                
                                if feature_id in rel_mem_plot and 'mem' in rel_mem_plot[feature_id]:
                                    rel_mem_plot[feature_id]['mem'].append(obj.id)
                                else:
                                    if feature_id in rel_mem_plot:
                                        rel_mem_plot[feature_id].update({'mem': [obj.id]})
                                    else:
                                        rel_mem_plot[feature_id] = {'mem': [obj.id]}

                            elif layer.name == 'Vegetation_Points':
                                feature_object.veg_spread = ogr_feature.get('GIRTH_mm')
                                feature_object.save()
                        #FIN Create memorials or plots Special cases
                    else:
                        raise TypeError('Impossible to create layer for feature code ['+ogr_feature.get('TYPE')+'], make sure it exists in main.featurecode')
                #FIN FOR layer
        #FIN FOR shape_file_paths

        # Loop throught dictionary and create relationsip memorial and plot
        # 1(key=feature_id) => uuid1(mem), uuid2(plot)
        # for key in rel_mem_plot:
        #     if len(rel_mem_plot[key]) == 2: #only plot-memorial relationship from the shapefile
        #         memtmp = None
        #         plottmp = None
        #         if rel_mem_plot[key][0][0] == 'mem':
        #             memtmp = Memorial.objects.get(id=rel_mem_plot[key][0][1])
        #             plottmp = GravePlot.objects.get(id=rel_mem_plot[key][1][1])
        #         elif rel_mem_plot[key][0][0] == 'plot':
        #             plottmp = GravePlot.objects.get(id=rel_mem_plot[key][0][1])
        #             memtmp = Memorial.objects.get(id=rel_mem_plot[key][1][1])
        #         if memtmp != None and plottmp != None:
        #             MemorialGraveplot.objects.create(memorial=memtmp, graveplot=plottmp)
        #     else:
        #         print(key)
        #         print(len(rel_mem_plot[key]))
        #         print(rel_mem_plot[key])
        
        
        # Loop throught dictionary and create relationsip memorial and plot
        # (key=feature_id) => 'mem': [uuid1(mem)], 'plot': [uuid2(plot)]
        for key in rel_mem_plot:
            if 'mem' in rel_mem_plot[key] and 'plot' in rel_mem_plot[key]:
                #Get plot, only one plot per feature_id, then get [0] position of the array
                plottmp = GravePlot.objects.get(id=rel_mem_plot[key]['plot'][0])
                
                #loop memorial(s) and create relation(s)
                for mem_id in rel_mem_plot[key]['mem']:
                    memtmp = Memorial.objects.get(id=mem_id)

                    if memtmp != None and plottmp != None:
                        MemorialGraveplot.objects.create(memorial=memtmp, graveplot=plottmp)
                
                #print 1 plot, multiple memorials
                if len(rel_mem_plot[key]['mem']) > 1:
                    print('KEY: '+key)
                    print(rel_mem_plot[key])

        return super(ImportShapeFile, self).form_valid(form)


class SiteAllLayerNames(ViewOnlyView):

    def get(self, request):
        """Returns a json object containing the layer groups and names that exist for the site"""
        # TODO: optimise this method
        layers = []
        position = 0

        feature_groups = FeatureGroup.objects.all()

        if not (request.user and request.user.is_authenticated):
            feature_groups.exclude(group_code__in=authenticated_only_layers)

        for group in feature_groups.order_by('hierarchy'):
            layer_group = {}
            codes = None

            if group.group_code == 'memorials':
                # import pdb; pdb.set_trace()
                codes = group.feature_codes.distinct('display_name', 'pk')
            elif group.group_code == 'memorial_cluster':
                codes = FeatureGroup.objects.filter(Q(group_code = 'memorials') | Q(group_code = 'plots')).distinct('display_name', 'pk')
                if codes.exists():
                    codes = group.feature_codes.filter(feature_type='cluster').distinct('display_name', 'pk')
            else:
                codes = group.feature_codes.distinct('display_name', 'pk')
                if group.group_code == 'plots':
                    codes = codes | group.feature_codes.filter(Q(feature_type='available_plot') | Q(feature_type='reserved_plot')).distinct('display_name', 'pk')
            if codes:
                layer_group['group_id'] = group.id
                layer_group['group_code'] = group.group_code
                layer_group['display_name'] = group.display_name
                layer_group['switch_on_off'] = group.switch_on_off
                layer_group['hierarchy'] = group.hierarchy
                layer_group['layers'] = []
                codes = codes.distinct('feature_type', 'display_name').order_by('display_name')
                for code in codes:
                    # only need this layer if it exists for the site
                    if code.layer_set.first():
                        layer = {}
                        layer['layer_id'] = code.id
                        layer['layer_code'] = code.feature_type
                        layer['layer_type'] = code.type
                        layer['display_name'] = code.layer_set.first().display_name if hasattr(code.layer_set.first(), 'display_name') else code.display_name
                        layer['initial_visibility'] = code.layer_set.first().initial_visibility
                        layer['min_resolution'] = code.layer_set.first().min_resolution
                        layer['max_resolution'] = code.layer_set.first().max_resolution
                        layer['show_in_toolbar'] = code.show_in_toolbar
                        layer['hierarchy'] = code.hierarchy
                        position+=1
                        layer_group['layers'].append(layer)
                layers.append(layer_group)
            result = {'layer_groups': layers, 'number_of_layers': position}
        response = JsonResponse(result, content_type ='application/json', safe=False)
        return response

# curently only works for memorials
class FeatureAttributeMaterials(ViewOnlyView):

    def get(self, request):
        try:
            material_attribute = PublicAttribute.objects.get(name='Material')
            return JsonResponse({'materials':material_attribute.options}, safe=False)
        except:
            msg = "The 'material' public attribute is missing!"
            print(msg)
            return HttpResponseBadRequest(msg)
    
    def post(self, request):
        response = request.body.decode()
        material = json.loads(response)['material']
        memorial_id = json.loads(response)['memorial_id']
        memorial = Memorial.objects.get_from_uuid(memorial_id)

        material_attribute = PublicAttribute.objects.get(name='Material')

        # check if attribute already exists for this memorial
        if memorial.topopolygon.feature_attributes.exists():
            featureMaterialAttributes = memorial.topopolygon.feature_attributes.filter(public_attribute=material_attribute)

            if featureMaterialAttributes.exists():
                featureMaterialAttribute = featureMaterialAttributes[0]
                featureMaterialAttribute.char_value = material
                featureMaterialAttribute.save()
                return HttpResponse(status=204)
        
        # attribute does not exist for this memorial.
        feature_attribute = FeatureAttributes.objects.create(attribute=material_attribute, char_value=material)
        memorial.topopolygon.feature_attributes.add(feature_attribute)
        return HttpResponse(status=204)