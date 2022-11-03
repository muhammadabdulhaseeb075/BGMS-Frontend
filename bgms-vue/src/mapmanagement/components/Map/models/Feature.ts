import OLFeature from 'ol/Feature';

/**
 * @description
 * A very basic representation of a feature, not linked via directive to ol.Feature
 */
export default class Feature {

  id_;
  name;
  featureId;
  feature;
  coordinate;
  layer;
  isLayerGroup;

  constructor(name, feature_or_id_or_coord, layerName, isLayerGroup) {

    this.name = name;

    if (typeof feature_or_id_or_coord === 'string') {
      this.featureId = feature_or_id_or_coord
      this.layer = layerName;
      this.isLayerGroup = isLayerGroup;
    }
    else if (feature_or_id_or_coord.constructor === OLFeature) {
      this.feature = feature_or_id_or_coord;
      this.layer = layerName;//feature_or_id_or_coord.get('marker_type');
      this.isLayerGroup = false;
    }
    else if (feature_or_id_or_coord.constructor === Array) {
      this.coordinate = feature_or_id_or_coord;
      this.layer = layerName;
      this.isLayerGroup = isLayerGroup;
    }
  }
}