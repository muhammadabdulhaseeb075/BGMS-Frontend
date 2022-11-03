from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, m2m_changed

from bgsite.models import Person, Memorial, MemorialGraveplot, GravePlot
from geometries.models import TopoPolygons, Layer, FeatureAttributes
from geometriespublic.models import PublicAttribute
from mapmanagement.views import getClusterLayer

@receiver(m2m_changed, sender=Memorial.images.through)
def update_memorial_image(instance, action, **kwargs):
    """Clears the cache when a post_add or post_remove signal is recieved from the model"""

    if action == 'post_add' or action == 'post_remove':
        """Updates the layer cache when a memorial has been added or removed"""
        instance.update_layer_cache(False)

@receiver([post_save, post_delete], sender=MemorialGraveplot)
def update_MemorialGraveplot(instance, **kwargs):

    """Updates the layer cache when a link has been made or removed"""
    instance.memorial.update_layer_cache(False)

@receiver([post_save], sender=TopoPolygons)
def update_TopoPolygon(instance, **kwargs):
    """
    Updates the layer cache if this is a memorial or graveplot.
    Other feature types are updated in geometries app.
    """

    try:
        memorial = instance.memorial
    except:
        memorial = False
    
    try:
        graveplot = instance.graveplot
    except:
        graveplot = False

    created = kwargs.get('created', False)

    if not created:
        # If created, this is dealt with in update_GravePlotOrMemorial.
        # Note: created does seem to work. Hence try except below.
        if memorial:
            try:
                obj = Memorial.objects.get(topopolygon__id=instance.id)
                obj.update_layer_cache(created)
            except:
                pass

        elif graveplot:
            try:
                obj = GravePlot.objects.get(topopolygon__id=instance.id)
                obj.update_layer_cache(created)
            except:
                pass
    
    if memorial or graveplot:
        query_set = Memorial.objects.filter(topopolygon__geometry__isnull=False).prefetch_related('topopolygon')
        
        # update the cluster layer if its based on memorials and a memorial has changed
        # or it's based on a graveplot and a graveplot has changed
        if (query_set.exists() and memorial) or ((not query_set.exists()) and graveplot):
            getClusterLayer()

@receiver([post_delete], sender=TopoPolygons)
def delete_TopoPolygon(instance, **kwargs):
    """
    Updates the layer cache if this is a memorial or graveplot.
    Other feature types are updated in geometries app.
    """

    try:
        memorial = instance.memorial
    except:
        memorial = False
    
    try:
        graveplot = instance.graveplot
    except:
        graveplot = False

    if memorial:
        layer_obj = instance.layer
        layer_obj.update_feature_in_layer_geojson_cache(memorial.uuid, None, False, deleted=True)

    elif graveplot:
        # this graveplot has been deleted
        layer_obj = instance.layer

        # exception for available plot
        if layer_obj.feature_code.feature_type == 'available_plot':
            layer_obj.update_feature_in_layer_geojson_cache(instance.id, None, True, deleted=True)
        else:
            layer_obj.update_feature_in_layer_geojson_cache(graveplot.uuid, None, False, deleted=True)

    
    if memorial or graveplot:
        query_set = Memorial.objects.filter(topopolygon__geometry__isnull=False).prefetch_related('topopolygon')
        
        # update the cluster layer if its based on memorials and a memorial has changed
        # or it's based on a graveplot and a graveplot has changed
        if (query_set.exists() and memorial) or ((not query_set.exists()) and graveplot):
            getClusterLayer()

@receiver([post_save], sender=Memorial)
@receiver([post_save], sender=GravePlot)
def update_GravePlotOrMemorial(instance, created, **kwargs):
    """
    If feature has just been created
    """
    if created and instance.topopolygon:
        if instance.topopolygon.layer.feature_code.feature_type == 'available_plot':
            # remove current cache if it exists
            instance.topopolygon.layer.update_feature_in_layer_geojson_cache(instance.topopolygon.id, None, False, deleted=True)

        instance.update_layer_cache(created)

@receiver(m2m_changed, sender=TopoPolygons.feature_attributes.through)
def update_MaterialFeatureAttributes(instance, action, **kwargs):
    """Clears the cache when a post_add or post_remove signal is recieved from the model"""

    if action == 'post_add' or action == 'post_remove':
        material_attribute = PublicAttribute.objects.get(name='Material')

        pk_set = kwargs.get('pk_set', False)
        pk = pk_set.pop()

        feature_attribute = FeatureAttributes.objects.get(pk=pk)
            
        # if it's the material attribute being modified
        if feature_attribute.attribute == material_attribute:

            try:
                memorial = instance.memorial
            except:
                memorial = False
            
            if memorial:
                memorial.update_layer_cache(False)

@receiver([post_save], sender=FeatureAttributes)
def update_MaterialFeatureAttributes2(instance, **kwargs):

    created = kwargs.get('created', False)

    # if attribute has just been created, cache update will happen in update_MaterialFeatureAttributes
    if not created:
        material_attribute = PublicAttribute.objects.get(name='Material')
        
        # if it's the material attribute being modified
        if instance.attribute == material_attribute:

            try:
                memorial = instance.topopolygons_set.all()
                memorial = memorial[0].memorial
            except:
                memorial = False
            
            if memorial:
                memorial.update_layer_cache(False)