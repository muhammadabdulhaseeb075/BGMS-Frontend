import {VectorImage, Vector, Tile, Image} from 'ol/layer';
import GeoJSON from 'ol/format/GeoJSON';
import { ImageStatic, Vector as VectorSource, Cluster } from 'ol/source';
import WMTS from 'ol/source/WMTS';
import WMTSTilegrid from 'ol/tilegrid/WMTS';
import { boundingExtent, buffer } from 'ol/extent';
import { get as getProj } from 'ol/proj'

import store from '@/mapmanagement/store/index';
import layersStore from '@/mapmanagement/store/modules/MapLayers';
import axios from 'axios';

/**
 * @description
 * Gets the openlayers features from map and a single/array of layer/group names.
 */
export function getOlFeaturesFromLayers(features, layers){
  let olFeatures = [], olJSON = {};
  features.forEach((value, index, collection) => {
    let layer = layers[value.layer];
    let resolution = (window as any).OLMap.getView().getResolution();
    if(layer && layer.getMinResolution()<=resolution && resolution<layer.getMaxResolution() && layer.getOpacity()>0){
      let feature;
      if(value.coordinate) {
        feature = layer.getSource().getFeaturesAtCoordinate(value.coordinate)[0];
        if(!feature)
          feature = layer.getSource().getClosestFeatureToCoordinate(value.coordinate);
        if(feature)
          olJSON[feature.getGeometry().getCoordinates()+'']=(feature);
      }
      else if(value.featureId){
        feature = layer.getSource().getFeatureById(value.featureId);
        if(feature)
          olFeatures.push(feature);
      }
      else if(value.feature)
        olFeatures.push(value.feature);
    }
  });

  var olFeatureArray = [];
  olFeatureArray = Object.keys(olJSON).map(function(k) { return olJSON[k] });
  olFeatures.push.apply(olFeatures, olFeatureArray);
  return olFeatures;
}

export function getOLFeatures(layers, coordinate, pixel, resolution, memorialCapture){
  let features = []
  let layerNames = [];

  if (!store.getters.getCurrentPixel || store.getters.getCurrentPixel != pixel) {
    store.commit('setCurrentPixel', pixel);
    store.commit('setFeaturesAtPixel', {});

    if (pixel) {
      // get all features at pixel
      (window as any).OLMap.forEachFeatureAtPixel(pixel, function (feature) {
        const layer = feature.values_.marker_type;
        if (store.getters.getFeaturesAtPixel[layer])
          store.getters.getFeaturesAtPixel[layer].push(feature);
        else
          store.getters.getFeaturesAtPixel[layer] = [feature];
      });
    }
  }

  const keys = Object.keys(layers)

  keys.forEach(layerName => {
    if(layers[layerName] && layers[layerName].getMinResolution()<=resolution && resolution<layers[layerName].getMaxResolution() && layers[layerName].getOpacity()>0){
      let layerFeatures = [];
      if(store.getters.getFeaturesAtPixel[layerName])
        layerFeatures.push.apply(layerFeatures, store.getters.getFeaturesAtPixel[layerName]);

      if(layers[layerName].getSource().constructor === Cluster){
        console.log('cluster layer');
        // need to deal with points in cluster
        let extent = boundingExtent([coordinate]);
        extent = buffer(extent, 7*resolution);
        layers[layerName].getSource().forEachFeatureInExtent(extent, function(feature){
          layerFeatures.push(feature);
        });
      }
      else if(layerName === 'memorials'){
        //dealing with memorial points temporarily, very bad fix though
        let extent = boundingExtent([coordinate]);
        extent = buffer(extent, 5*resolution);
        layerFeatures.push.apply(layerFeatures, layers[layerName].getSource().getFeaturesInExtent(extent));
      }
      // if memorial capture is enabled, layer is a 'Memorial' group, and there has been no direct hit on a feature, add a buffer
      else if(memorialCapture && layerFeatures.length===0){
        let extent = boundingExtent([coordinate]);
        extent = buffer(extent, 0.5); //0.5m
        let featuresInExtent = layers[layerName].getSource().getFeaturesInExtent(extent);
        if (featuresInExtent.length > 1)
          layerFeatures.push.apply(layerFeatures, [layers[layerName].getSource().getClosestFeatureToCoordinate(coordinate)]);
        else
          layerFeatures.push.apply(layerFeatures, featuresInExtent);
      }
      for (let i = layerFeatures.length-1; i>=0; i--) {
        // This is a bit of a hack to make sure other memorials are prioritiesed over grave_kerbs.
        // There must be a way to do this using hierarchy...
        if (layerName === "grave_kerb") {
          features.push(layerFeatures[i]);
          layerNames.push(layerName);
        }
        else {
          features.unshift(layerFeatures[i]);
          layerNames.unshift(layerName);
        }
      }
    }
  });

  // If true, this means multiple features in different layers are within the extent.
  // We need to find the closest memorial regardless of what layer it is in.
  if (memorialCapture && features.length>1) {
    var vectorSource = new VectorSource();
    vectorSource.addFeatures(features);

    var closestFeature = vectorSource.getClosestFeatureToCoordinate(coordinate);
    features = [closestFeature];
    layerNames = [closestFeature.get("name")];
  }

  return [features, layerNames];
}

/**
 * @description
 * Gets the openlayers layer from map and layer/group name.
 */
export function getLayerFromMap(name, isLayerName) {

  let returnLayers = {};

  (window as any).OLMap.getLayers().forEach(layer => {

    if ((isLayerName && layer.get('name') === name) || (!isLayerName && layer.get('groupName') === name))
      // found single layer or found layer belonging to group
      returnLayers[name] = layer;
  });

  return returnLayers;
}

/**
 * @description
 * Gets the openlayers layer from map and a single/array of layer/group names.
 */
export function getOlLayers(names, isLayerName): {} {
  let layers = {};		
  if(typeof names === 'string'){
    layers = getLayerFromMap(names, isLayerName);
  } 
  else {
    // it is an array of layer or group names
    for (let index in names){
      const name = names[index];
      Object.assign(layers, getLayerFromMap(name, isLayerName))
    }
  }
  return layers;
}

/*
  Map layers are represented by an object of the type
    {
        group: 'if it belongs to a group of layers eg. vegetation, utilities etc'
        name: unique name for identification eg. trees, bushes, lampposts etc
        visibility: if layer should be added to the visible layer stack
        index: where the layer should be initially placed in the visible stack (optional)
        source: source according to angular-openlayers-directive
        style: style according to angular-openlayers-directive
    }
*/

/**
 * Layer object
 *
 */
export class Layer {

  name;
  display_name;
  groupName;
  zIndex;
  source;
  minResolution;
  maxResolution;
  switch_on_off;
  show_in_toolbar;
  style;
  opacity;
  extent;
  defer;
  type;
  attributes_exist;
  surveys_exist;
  layer_group_name;
  visible: boolean = false;

  constructor(layerContructorObject) {
    this.name = layerContructorObject.name;
    this.display_name = layerContructorObject.display_name;
    this.groupName = layerContructorObject.group;
    this.zIndex = layerContructorObject.index;
    this.source = layerContructorObject.source;
    this.minResolution = layerContructorObject.minResolution;
    this.maxResolution = layerContructorObject.maxResolution;
    this.switch_on_off = layerContructorObject.switch_on_off;
    this.show_in_toolbar = layerContructorObject.show_in_toolbar;
    this.style = layerContructorObject.style;
    this.opacity = 1;
    this.extent = layerContructorObject.extent;
    this.defer = layerContructorObject.defer;
    this.type = layerContructorObject.type;
    this.attributes_exist = layerContructorObject.attributes_exist;
    this.surveys_exist = layerContructorObject.surveys_exist;
    this.layer_group_name = layerContructorObject.layer_group_name;
    
    if(layerContructorObject.visibility != undefined)
      this.visibility = layerContructorObject.visibility;
  }

  //helper function to create source
  createSource(source) {

    let oSource;
    switch(source.type){
      case 'GeoJSON':
        var geoJsonFormatter = new GeoJSON();
        if (source.projection) {
          geoJsonFormatter = new GeoJSON({
            featureProjection: source.projection
          });
        }
        if (source.url){
          oSource = new VectorSource({
            url: source.url,
            format: geoJsonFormatter,
            // crossOrigin: 'anonymous'
          });
        }
        else {
          //source.geojson.object.features = source.geojson.object.features.filter(feature => feature !== null);
          let features = geoJsonFormatter.readFeatures(source.geojson.object);
          oSource = new VectorSource({
            features: features,
            // crossOrigin: 'anonymous'
          });
        }
        break;
      case 'Cluster':
        var geojsonSource = JSON.parse(JSON.stringify( source ));
        geojsonSource.type = 'GeoJSON';
        oSource = new Cluster({
          distance: source.distance,
          source: this.createSource(geojsonSource),
          // crossOrigin: 'anonymous'
        });
        break;
      case 'EmptyVector':
        oSource = new VectorSource({
          // source: new VectorSource(),
          // crossOrigin: 'anonymous'
        });
        break;
      case 'TileWMTS':
        oSource = new WMTS({
          format: 'image/png',
          requestEncoding: 'REST',
          crossOrigin: 'anonymous',
          url: source.url,
          layer: source.layer,
          matrixSet: source.matrixSet,
          tileGrid: new WMTSTilegrid({
            tileSize: [256, 256],
            extent: source.tileGrid.extent,
            resolutions: source.tileGrid.resolutions,
            matrixIds: source.tileGrid.matrixIds
          }),
          style:source.style
        });
        break;
      case 'ImageStatic':
        if (!source.url) {
          console.error('You need a image URL to create a ImageStatic layer.');
          return;
        }
        var imageExtent;
        if(source.extent)
          imageExtent = source.extent;
        else
          imageExtent = getProj('pixel').getExtent();

        oSource = new ImageStatic({
          url: source.url,
//                        attributions: createAttribution(source),
//                        projection: source.projection,
          imageExtent: imageExtent,
          imageLoadFunction: source.imageLoadFunction,
          crossOrigin: 'anonymous'
        });
        break;
      default:
        oSource = null;
    }
    return oSource;
  }

  getFeatures(): Promise<any> {
    return new Promise<void>(resolve => {
      if (this.source.url) {
        axios.get(this.source.url)
        .then(response => {
          this.source.geojson = { object: response.data };
          this.source.url = null;
          resolve();
        });
      }
      else
        resolve();
    });
  }

  createLayer() {
    // console.log('overridden method createLayer');
    var oLayer;
    switch (this.source.type) {
      case 'GeoJSON':
        if (!(this.source.url || this.source.geojson) ){
          console.error('GeoJSON source needs either source url or geojson object');
          return;
        }
        if (this.type && this.type === 'VectorImage' ){
          //Wrap to use imageVector and change layer style with icons
          oLayer = new VectorImage({
            source: this.createSource(this.source)
          });
        }
        else {
            //Layer.type === Vector : Default if not defined
            oLayer = new Vector({
              source: this.createSource(this.source)
            });
        }
        break;
      case 'Cluster':
        if(!(this.source.distance && (this.source.text || this.source.url || this.source.geojson)) ){
          console.error('Cluster source needs both distance and text or url or geojson');
          return;
        }
        oLayer = new Vector({
          source: this.createSource(this.source)
        });
        break;
      case 'EmptyVector':
        console.log("created empty vector source");

        oLayer = new Vector({
          source: this.createSource(this.source)
        });
        break;
      case 'TileWMTS':
        console.log("created TileWMTS source");
        oLayer = new Tile({
          source: this.createSource(this.source),
          extent: this.source.extent,
          preload: 1
        });
        break;
      case 'ImageStatic':
        oLayer = new Image({
          source: this.createSource(this.source)
        });
        break;
      default:
        break;
    }
    if(this.name)
      oLayer.set('name', this.name);
    if(this.groupName)
      oLayer.set('groupName', this.groupName);
    if(this.zIndex)
      oLayer.setZIndex(this.zIndex);
    if(this.maxResolution)
      oLayer.setMaxResolution(this.maxResolution);
    if(this.minResolution)
      oLayer.setMinResolution(this.minResolution);
    if(!(typeof this.opacity === undefined))
      oLayer.setOpacity(this.opacity);
    if(this.defer){
      oLayer.once('postcompose', function(){
        this.defer.resolve(true);
      })
    }
     if (this.style) {
      const style = this.style;

      // not every layer has a setStyle method
      if (oLayer.setStyle && (typeof oLayer.setStyle === "function")) {
        oLayer.setStyle(style);
      }
    }

    return oLayer;
  }

  /**
   * setter/getter functions for visibility, uses the opacity property
   * in the background.
   */
  get visibility() {
    return this.visible;
  }
  set visibility(visibility) {

    const OLMAP = (window as any).OLMap;
    
    this.visible = visibility;

    let layerFound = null;
    let BreakException = {};
    
    try {
      OLMAP.getLayers().forEach(layer => {
        if (layer.get('name') === this.name) {
          layerFound = layer;
          // break foreach now that we've found what we need
          throw BreakException;
        }
      });
    }
    catch (e) {
      if (e !== BreakException) throw e;
    }
    
    // for layers other than memorials and plots, actually remove the layer from openlayers while not visible
    if (!layerFound || (this.groupName!=='memorials' && this.groupName!=='plots')) {

      if (layerFound && !visibility) {
        // this needs removed
        OLMAP.removeLayer(layerFound);
        store.dispatch('updateOlLayers');
      }

      if (!layerFound && visibility) {
        // we need to add this layer
        
        if (this.source.type !== 'TileWMTS') {
          this.getFeatures()
          .then(() => {
            OLMAP.addLayer(this.createLayer());
            store.dispatch('updateOlLayers');
          });
        }
        else {
          OLMAP.addLayer(this.createLayer());
          store.dispatch('updateOlLayers');
        }
      }
    }
    else 
      // change visibility of layer
      layerFound.setVisible(visibility);
    
    // if cluster is based on this layer, also update cluster visibility
    if (layersStore.state.clusterLayer && this.name===layersStore.state.clusterLayer.name)
      (store.getters.getLayerByName('cluster') as any).visibility = visibility;
  }
}

/*
  Map layer groups are represented by an object of the type
      {
          name: unique name for identification eg. vegetation, utilities etc
          display_name: name shown in ui
          visibility: if layers should be added to the visible layer stack
          layers: json object of layers in the group
      }
  */

/**
 * LayerGroup object
 *
 */
export class LayerGroup {

  name;
  hierarchy;
  display_name;
  switch_on_off;
  layers = {};

  constructor(layerGroupContructorObject) {
    this.name = layerGroupContructorObject.name;
    this.hierarchy = layerGroupContructorObject.hierarchy;
    this.display_name = layerGroupContructorObject.display_name;
    this.switch_on_off = layerGroupContructorObject.switch_on_off;
    
    if(layerGroupContructorObject.layers){
      for (let i in layerGroupContructorObject.layers) {
        this.addLayer(layerGroupContructorObject.layers[i]);
      }
    }
    if(layerGroupContructorObject.visibility != undefined)
      this.visibility = layerGroupContructorObject.visibility;
  }

  /**
   * Setter/getter functions for visibility
   */
  get visibility() {
    // return true if any of the layers are visible
    for (let i in this.layers) {
      if (this.layers[i].visibility)
        return true;
    }

    return false;
  }
  set visibility(visibility) {
    //setting visibility if it is true/false
    for (let i in this.layers) {
      this.layers[i].visibility = visibility;
    }
    
    // if cluster is based on this layer, also update cluster visibility
    if (layersStore.state.clusterLayer && this.name===layersStore.state.clusterLayer.name)
      (store.getters.getLayerByName('cluster') as any).visibility = visibility;
  }

  show_in_toolbar() {
    //if visibility is undefined, then getting it from layers
    for (let layerkey in this.layers){
        if(this.layers[layerkey].show_in_toolbar){
          return true;
        }
    }
    return false;
  }

  addLayer(layer) {
    this.layers[layer.name] = layer;
  }

  getLayerByName(layerName) {
    if(this.layers[layerName])
      return this.layers[layerName];
    else
      console.log('layer '+layerName+' doesnt exist in '+this.name);
  }

  getAllLayers() {
    return this.layers;
  }
}