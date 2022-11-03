from tenant_schemas.test.cases import TenantTestCase
from bgsite.models import Memorial
from geometries.models import TopoPolygons, Layer
from geometriespublic.models import FeatureCode
from tenant_schemas.test.client import TenantClient
import mock


class TestMemorialQuerySet(TenantTestCase):

    def setUp(self):
        self.client = TenantClient(self.tenant)

        fc1 = FeatureCode.objects.create(feature_type='',type='', display_name='', min_resolution=0,max_resolution=0,show_in_toolbar=False)
        l1 = Layer.objects.create(id='0010a200-a098-43ea-abdf-ff20435e88e6', feature_code=fc1, display_name='',show_in_toolbar='',initial_visibility='')
        p1 = TopoPolygons.objects.create(user_created='',layer=l1, feature_id='1', id='0010a200-a098-43ea-abdf-ff20435e88e7', geometry='MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))')
        m1 = Memorial.objects.create(id='0010a200-a098-43ea-abdf-ff20435e88e8',topopolygon=p1)
        m2 = Memorial.objects.create(id='0010a200-a098-43ea-abdf-ff20435e88e9')
        # import pdb; pdb.set_trace()

    def test_get_memorials_features_id(self):
        """Return a queryset conatining memorials uuids and feature id for those who have a Geometry related"""
        memorials = Memorial.objects.get_memorials_features_id()
        # import pdb; pdb.set_trace()
        self.assertIsNotNone(memorials)
        self.assertEqual(len(memorials), 1)
