from django.db import models
from django.db.models.query import QuerySet
from geometriespublic.models import FeatureCode

class LayerQuerySet(QuerySet):
    '''manager for `geometries.models.Layer`'''

    def create_layer_from_feature_type(self, feature_type):
        '''Creates the layer instance for the feature_type (type: String) parameter,
            the feature_type must exists or it wont create layer'''
        fc = FeatureCode.objects.get(feature_type=feature_type)
        if not self.filter(feature_code_id=fc.id).exists():
            return self.create(feature_code=fc, display_name=fc.display_name,
                         show_in_toolbar=fc.show_in_toolbar,
                         initial_visibility=fc.feature_groups.first().initial_visibility,
                         min_resolution=fc.min_resolution,
                         max_resolution=fc.max_resolution)
        else:
            return None