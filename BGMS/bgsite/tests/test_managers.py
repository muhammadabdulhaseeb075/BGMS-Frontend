# from tenant_schemas.test.cases import TenantTestCase
# from django.db.models.base import Model
# from bgsite.managers import MarkerQuerySet
# from bgsite.models import GravePlot, Memorial, MemorialGraveplot, Person
# from unittest.mock import Mock
# from geometries.models import TopoPolygons
# from model_mommy import mommy
# from tenant_schemas.test.client import TenantClient
# from django.core.exceptions import ObjectDoesNotExist
#
# class TestMarkerQuerySet(TenantTestCase):
#
#     def setUp(self):
#         self.client = TenantClient(self.tenant)
# # #         self.client.logout()
#         graveplot = GravePlot.objects.create(description='graveplot')
#         gravestone = mommy.make('geometries.TopoPolygons',
#                              layer__feature_code__feature_type='gravestone')
#         linked_memorial = Memorial.objects.create(description='gravestone', topopolygon=gravestone)
#         wargrave = mommy.make('geometries.TopoPolygons',
#                              layer__feature_code__feature_type='wargrave')
#         linked_memorial2 = Memorial.objects.create(description='wargrave', topopolygon=wargrave)
#         MemorialGraveplot.objects.create(memorial=linked_memorial, graveplot=graveplot)
#         MemorialGraveplot.objects.create(memorial=linked_memorial2, graveplot=graveplot)
#         person = mommy.make('bgsite.Person')
#         death=mommy.make('bgsite.Death', person=person)
#         person.add_memorial(linked_memorial2)
#
#     """Getting memorials by uuid and linked uuid should return the correct memorial"""
#     def test_get_memorial_from_uuid(self):
#         gravestone = Memorial.objects.get(description='gravestone')
#         self.assertIsNotNone(gravestone)
#         linked_uuid = MemorialGraveplot.objects.get(memorial=gravestone).uuid
#         self.assertEqual(Memorial.objects.get_from_uuid(gravestone.uuid), gravestone)
#         self.assertEqual(Memorial.objects.get_from_uuid(linked_uuid), gravestone)
#
#     """Getting memorials by uuid and linked uuid and marker should return the correct memorial"""
#     def test_get_memorial_from_uuid_marker(self):
#         gravestone = Memorial.objects.get(description='gravestone')
#         self.assertIsNotNone(gravestone)
#         linked_uuid = MemorialGraveplot.objects.get(memorial=gravestone).uuid
#         self.assertEqual(Memorial.objects.get_from_uuid(gravestone.uuid, 'gravestone'), gravestone)
#         self.assertEqual(Memorial.objects.get_from_uuid(linked_uuid, 'gravestone'), gravestone)
#
#     """Deleting memorial assigned to a person should raise exception"""
#     def test_delete_memorial_with_no_person(self):
#         gravestone = Memorial.objects.get(description='wargrave')
#         self.assertIsNotNone(gravestone)
#         linked_uuid = MemorialGraveplot.objects.get(memorial=gravestone).uuid
#         self.assertRaises(ObjectDoesNotExist, Memorial.objects.delete_memorial_with_no_person, linked_uuid, 'wargrave')
#         gravestone = Memorial.objects.get(description='wargrave')
#         self.assertIsNotNone(gravestone)
#
#     """Deleting memorial not linked to a person should delete properly"""
#     def test_delete_memorial(self):
#         gravestone = Memorial.objects.get(description='gravestone')
#         self.assertIsNotNone(gravestone)
#         linked_uuid = MemorialGraveplot.objects.get(memorial=gravestone).uuid
#         self.assertIsNotNone(linked_uuid)
#         Memorial.objects.delete_memorial_with_no_person(linked_uuid, 'gravestone')
#         self.assertRaises(ObjectDoesNotExist, Memorial.objects.get, description='gravestone')
#
#
        
