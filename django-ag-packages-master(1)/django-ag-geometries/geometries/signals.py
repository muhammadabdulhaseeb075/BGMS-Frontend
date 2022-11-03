from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from geometries.models import TopoPolygons, TopoPolylines, TopoPoints, LayerCache

@receiver([post_save], sender=TopoPolygons)
@receiver([post_save], sender=TopoPolylines)
@receiver([post_save], sender=TopoPoints)
def update_Feature(sender, instance, **kwargs):

    # skip for memorial and graveplot as this will be handled seperately
    try:
        if sender == TopoPolygons and instance.memorial:
            return
    except:
        pass
    try:
        if sender == TopoPolygons and instance.graveplot:
            return
    except:
        pass

    created = kwargs.get('created', False)
    
    """Updates the layer cache. Including removing from a layer cache if the layer has been changed."""
    instance.update_layer_cache(created)

@receiver([post_delete], sender=TopoPolygons)
@receiver([post_delete], sender=TopoPolylines)
@receiver([post_delete], sender=TopoPoints)
def delete_Feature(sender, instance, **kwargs):

    # skip for memorial and graveplot as this will be handled seperately
    try:
        if sender == TopoPolygons and instance.memorial:
            return
    except:
        pass
    try:
        if sender == TopoPolygons and instance.graveplot:
            return
    except:
        pass
    
    """Deletes the feature."""
    instance.layer.update_feature_in_layer_geojson_cache(instance.id, None, True, deleted=True)