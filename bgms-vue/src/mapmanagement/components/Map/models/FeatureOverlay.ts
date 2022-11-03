import { getOlLayers, getOlFeaturesFromLayers } from '@/mapmanagement/components/Map/models/Layer';
import Feature from '@/mapmanagement/components/Map/models/Feature';
import VectorLayer from 'ol/layer/Vector';
import { Vector as VectorSource, Cluster as ClusterSource } from 'ol/source';

/**
 * @description
 * Defines a feature-overlay(unmanagedLayer) object
 */
export default class FeatureOverlay {

  name;
  group;
  style;
  features = [];
  featureOverlay;
  olLayers = {};
  layerKey = [];
  lk1;

  constructor(name, group, style) {
  
    this.name = name;
    this.group = group;
    this.style = style;
    
    this.featureOverlay = new VectorLayer({
      style: this.style,
      map: (window as any).OLMap,
      source: new VectorSource({
        useSpatialIndex: false, // optional, might improve performance
        // crossOrigin: 'anonymous'
      }),
      updateWhileAnimating: true, // optional, for instant visual feedback
      updateWhileInteracting: true // optional, for instant visual feedback
    });

    this.lk1 = (window as any).OLMap.getView().on('change:resolution', evt =>{
      console.log('change:resolution:'+evt.target.getResolution());
      this.featureOverlay.getSource().clear(true);
      this.featureOverlay.getSource().addFeatures(getOlFeaturesFromLayers(this.features, this.olLayers));
    });
  }

  addFeature(feature) {
    if(this.getFeaturePositionInStack('name', feature.name)[0] === -1){
      let newFeature = new Feature(feature.name, feature.feature, feature.layer, feature.isLayerGroup);
      this.features.push(newFeature);

      if(!this.olLayers[feature.layer]){
        const LAYERS = getOlLayers(feature.layer, !feature.isLayerGroup);
        this.addLayerListeners(LAYERS, this.layerKey, this.featureOverlay);
        Object.assign(this.olLayers, LAYERS);
      }
      
      this.layerKey.push(this.lk1);

      this.featureOverlay.getSource().addFeatures(getOlFeaturesFromLayers([newFeature], this.olLayers));
    }
  }

  addFeatures(additionalFeatures) {
    for (var index in additionalFeatures){
      this.addFeature(additionalFeatures[index]);
    }
  }

  getFeatures() {
    return this.features;
  }

  getFeatureByName(featureName) {
    var positions = this.getFeaturePositionInStack('name', featureName)[0];
    if(positions[0] != -1)
      return this.features[positions[0]];
  }

  removeFeatureByName(name){
    const positions = this.getFeaturePositionInStack('name', name);
    if(positions.length > 0) {
      for(let i=positions.length-1; i>=0; i--){
        if(positions[0] > 0){
          this.features[positions[0]].removeFeatureFromLayer(name, name);
          this.features.splice(positions[0], 1);
        }
      }
    }
  }

  public removeAllFeatures() {
    this.featureOverlay.getSource().clear();
    this.features = [];
  }

  getFeaturePositionInStack(key, value) {
    //optimise this
    var positions = [-1];
    var i = 0;
    this.features.forEach((feature, index) => {
      if(feature[key] === value){
        positions[i++] = index;
      }
    });
    return positions;
  }

  public featureExistsInOverlay(featureId): boolean {
    return this.features.some(feature =>
      feature.featureId === featureId
    );
  }

  /**
   * @function
   * @description
   * Adds listeners to layers to listen for changes in opacity i.e. if the layer is hidden, it
   * removes the feature overlay, and when the layer is made visible again, it adds back the
   * feature overlay.
   */
  addLayerListeners(olLayers, layerKey, featureOverlay) {
    if(olLayers){
      const layerKeys = Object.keys(olLayers)
      layerKeys.forEach(key => {
        let olLayer = olLayers[key];

        if(olLayer){
          let lk2 = olLayer.on('change:opacity', (evt) => {
            console.log('change:opacity');
            if(olLayer.getOpacity()===0)
              featureOverlay.setMap(null);
            else
              featureOverlay.setMap((window as any).OLMap);
          });

          layerKey.push(lk2);

          if(olLayer.getSource().constructor===ClusterSource) {
            //if it is a cluster source, wait for the clusters to be redrawn and then redraw feature overlay
            let lk3 = olLayer.on('change', (evt) => {
              console.log('changefeature');
              featureOverlay.getSource().clear(true);
            });
            layerKey.push(lk3);
          }
        }
      });
    }
  }
}