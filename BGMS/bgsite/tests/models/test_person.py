from tenant_schemas.test.cases import TenantTestCase
from bgsite.models import Person, GravePlot
from geometries.models import TopoPolygons, Layer
from tenant_schemas.test.client import TenantClient
from model_mommy import mommy
from django.core.serializers import serialize
import json
from geometriespublic.models import FeatureCode


'''
Dealing with no UUID serialization support in json
'''
from json import JSONEncoder
from uuid import UUID
JSONEncoder_olddefault = JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)
JSONEncoder.default = JSONEncoder_newdefault


class TestPerson(TenantTestCase):

    def setUp(self):
        self.client = TenantClient(self.tenant)
        avp = FeatureCode.objects.get(feature_type='available_plot')
        avl = Layer.objects.get(feature_code=avp)
        gvp = mommy.make('bgsite.GravePlot')
        available_plot = mommy.make('geometries.TopoPolygons', layer=avl)
        
        # geo_json = serialize('geojson', [available_plot], geometry_field='geometry')

        person = mommy.make('bgsite.Person')
        death = mommy.make('bgsite.Death', person=person)
        # import pdb; pdb.set_trace()
        # person = Person.objects.all().first()
        # person.add_death_details(death_date=person_death_date, age_years=person_data['age_years'],
                                    # age_months=person_data['age_months'], age_hours=person_data['age_hours'], age_days=person_data['age_days'],
                                    # impossible_date_day=person_data['impossible_date_day_death'],
                                    # impossible_date_month=person_data['impossible_date_month_death'], impossible_date_year=person_data['impossible_date_year_death'],)
        # death=mommy.make('bgsite.Death', person=person)
        # person.add_memorial(linked_memorial2)
        # Person.objects.create()


    def test_bury_person(self):
        """Return a dictionary {'feature_dict': feature_dict, 'graveplot': graveplot, 'graveplot_dict': graveplot_dict}"""

        # graveplot_polygon_feature: encoded 2 times sample:
        # '"{\\"type\\":\\"Feature\\",\\"id\\":\\"0bed60ed-7338-45bb-ad1f-3388b50a144d\\",\\"geometry\\":{\\"type\\":\\"MultiPolygon\\",\\"coordinates\\":[[[[332604.79,539895.51],[332605.69,539895.51],[332605.69,539897.51],[332604.79,539897.51],[332604.79,539895.51]]]]},\\"properties\\":{\\"marker_type\\":\\"plot\\",\\"id\\":\\"0bed60ed-7338-45bb-ad1f-3388b50a144d\\",\\"layer\\":\\"plot\\",\\"headpoint\\":\\"{\\\\\\"type\\\\\\":\\\\\\"Point\\\\\\",\\\\\\"coordinates\\\\\\":[332605,539896.51]}\\"}}"'

        # testg = '"{\\"type\\":\\"Feature\\",\\"id\\":\\"0bed60ed-7338-45bb-ad1f-3388b50a144d\\",\\"geometry\\":{\\"type\\":\\"MultiPolygon\\",\\"coordinates\\":[[[[332604.79,539895.51],[332605.69,539895.51],[332605.69,539897.51],[332604.79,539897.51],[332604.79,539895.51]]]]},\\"properties\\":{\\"marker_type\\":\\"plot\\",\\"id\\":\\"0bed60ed-7338-45bb-ad1f-3388b50a144d\\",\\"layer\\":\\"plot\\",\\"headpoint\\":\\"{\\\\\\"type\\\\\\":\\\\\\"Point\\\\\\",\\\\\\"coordinates\\\\\\":[332605.24,539896.51]}\\"}}"'

        # "{\"type\":\"Feature\",\"id\":\"7885beaf-1aef-422d-8f3c-3d9d5259adf5\",\"geometry\":{\"type\":\"MultiPolygon\",\"coordinates\":[[[[332606.89,539896.63],[332607.79,539896.63],[332607.79,539898.63],[332606.89,539898.63],[332606.89,539896.63]]]]},\"properties\":{\"id\":\"7885beaf-1aef-422d-8f3c-3d9d5259adf5\",\"marker_type\":\"available_plot\",\"layer\":\"available_plot\",\"headpoint\":\"{\\\"type\\\":\\\"Point\\\",\\\"coordinates\\\":[332607.33999999997,539897.63]}\"}}"

        # geo_json = serialize('geojson', [available_plot], geometry_field='geometry')
        # '{"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "EPSG:4326"}}, "features": [{"geometry": {"type": "MultiPolygon", "coordinates": [[[[-7.557159805206323, 49.766807239117234], [-7.557160831822299, 49.76681619094689], [-7.557147011212153, 49.766816855901844], [-7.557159805206323, 49.766807239117234]]]]}, "properties": {"layer": "602b53ff-45ac-479b-a36e-14dac5e67dcc", "surveyor": null, "feature_id": -9273, "user_created": false, "date_uploaded": "2016-08-15T13:36:21.905Z", "geom_acc": null, "attributes": []}, "type": "Feature"}]}'

        ap = TopoPolygons.objects.all().first()
        gvp = GravePlot.objects.all().first()
        geo_json = serialize('geojson', [ap], geometry_field='geometry')
        tmpgj = json.loads(geo_json)
        tmpgj["properties"] = {'marker_type':'available_plot'}

        # aa.update({'geometry': aa["features"][0]["geometry"]})
        tmpgj.update({'geometry': tmpgj["features"][0]["geometry"], 'id':gvp.uuid})
        geo_json = json.dumps(tmpgj)
        # import pdb; pdb.set_trace()

        person = Person.objects.all().first()
        bp = person.bury_person(geo_json)
        print(bp)
        # This unit test will fail due to the geo_json parameter has been encoded 2 times from client side which its unusual, that its not possible to do in server side, therefore the secon json.loads inside bury_person will throw an error. Solution: needs refactoring so it can work properly with just one enconding.
        #Solution: the method was refactored so it receives 1 encoding geojson
        self.assertIsNotNone(bp)
    
    def test_add_person_details(self):
        """
        Save their details base on the parameter list kwargs, the parameter names have to match Person's field names.
        """
        # import pdb; pdb.set_trace()
        person_data = {'first_names':'first_names','last_name': 'last_name','gender': 'gender','title': 'title','description': 'description','impossible_date_day': 31,'impossible_date_month': 2,'impossible_date_year': 1000}
        person = Person.objects.all().first()
        person.add_person_details(first_names=person_data['first_names'], last_name=person_data['last_name'],gender=person_data['gender'],title=person_data['title'],description=person_data['description'],impossible_date_day=person_data['impossible_date_day'],impossible_date_month=person_data['impossible_date_month'],impossible_date_year=person_data['impossible_date_year'])
        
        result_data = Person.objects.filter(id=person.id).values('first_names','last_name','gender','title','description','impossible_date_day','impossible_date_month','impossible_date_year')[0]

        
        self.assertIsNotNone(result_data)
        self.assertDictEqual(person_data,result_data)
        # self.assertDictContainsSubset(person_data,result_data)


