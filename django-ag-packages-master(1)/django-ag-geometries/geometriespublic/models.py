from geometriespublic.validators import bleach_validator
from django.db.models.query import QuerySet
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.core import validators
import json
json.encoder.FLOAT_REPR = lambda o: format(o, '.2f')
import uuid

#site independent geometries models

class FeatureCodeQuerySet(QuerySet):
	def reorder_hierarchy(self, old_h, new_h):
		fcs = self.all().order_by('hierarchy')
		for fc in fcs:
			if fc.hierarchy == old_h:
				fc.hierarchy = new_h
			elif old_h < new_h and fc.hierarchy > old_h and fc.hierarchy <= new_h:
				fc.hierarchy -= 1
			elif old_h > new_h and fc.hierarchy >= new_h and fc.hierarchy < old_h:
				fc.hierarchy += 1
			fc.save()


class FeatureCode(models.Model):
	feature_type = models.CharField(db_index=True, max_length=20, validators=[bleach_validator])
	type = models.CharField(max_length=20, validators=[bleach_validator])
	display_name = models.CharField(max_length=20, validators=[bleach_validator])
	min_resolution = models.FloatField()
	max_resolution = models.FloatField()
	show_in_toolbar = models.BooleanField()
	hierarchy = models.IntegerField(default=0)
	objects = FeatureCodeQuerySet.as_manager()

	def __str__(self):
		return self.display_name

	class Meta:
		ordering = ['display_name', 'pk']

class FeatureGroupQuerySet(QuerySet):
	def get_layer_groups(self, groups_list):
		result = {} # {group_type: [feature_codes]}
		sorted_groups_list = sorted(groups_list)
		for group_type in sorted_groups_list:
			if self.filter(group_code=group_type).exists():
				values = self.filter(group_code=group_type).values('feature_codes__display_name', 'feature_codes__feature_type').order_by('feature_codes__display_name')
				result.update({group_type : json.dumps(list(values))})

		# TODO: update when empty groups_list to return all
		# self.filter(group_code__in=groups_list).values('feature_codes__display_name', 'feature_codes__feature_type')
		return result
	
	def get_memorial_types(self):
		"""Return featurecodes for group memorials"""
		memorials = self.filter(group_code='memorials').first()
		if memorials is not None:
			return [(fc.id,fc.display_name) for fc in memorials.feature_codes.all().order_by('display_name')]
		else:
			return []

class FeatureGroup(models.Model):
	group_code = models.CharField(max_length=20, validators=[bleach_validator])
	display_name = models.CharField(max_length=20, validators=[bleach_validator])
	switch_on_off = models.BooleanField(default=True)
	initial_visibility = models.BooleanField(default=False)
	hierarchy = models.IntegerField()
	feature_codes = models.ManyToManyField(FeatureCode, related_name='feature_groups')
	objects = FeatureGroupQuerySet.as_manager()

	def __str__(self):
		return self.display_name


class Surveyor(models.Model):
	surveyor_name = models.CharField(max_length=100, validators=[bleach_validator])


class FieldType(models.Model):
	name = models.CharField(max_length=20, primary_key=True)
	label = models.CharField(max_length=200, unique=True)
	type_name = models.CharField(max_length=20)
	attributes = models.BooleanField(default=True)
	survey = models.BooleanField(default=True)

	def __str__(self):
		return self.label.title()


class PublicAttribute(models.Model):
	id = models.UUIDField(default=uuid.uuid4, primary_key=True)
	name = models.CharField(max_length=100, unique=True)
	feature_codes = models.ManyToManyField(FeatureCode, related_name='public_attributes')
	type = models.ForeignKey(FieldType, on_delete=models.CASCADE, limit_choices_to={'attributes': True})
	options = ArrayField(base_field=models.CharField(max_length=50), null=True, blank=True, verbose_name="Options (for 'Select' type only)")
	feature_attributes = GenericRelation('geometries.FeatureAttributes', related_query_name='public_attribute')

	def __str__(self):
		return self.name.title()