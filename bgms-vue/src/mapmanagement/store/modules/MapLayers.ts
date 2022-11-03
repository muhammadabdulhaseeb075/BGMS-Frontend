import { LayerGroup, Layer } from '@/mapmanagement/components/Map/models/Layer';
import LayerStyles from '@/mapmanagement/components/Map/models/LayerStyle';

const state = {
  layerStyles: new LayerStyles(),
  layerGroups: {},
  layers: {},
  displayGroups: {},
  // Do we have aerial layer?
  aerialLayer: false,
  //Do we have plans layer?
  plansLayer: false,
  //Remember wheter aerial was active before, default MAP view then false
  wasAerialVisible: false,
  //disable aerial button
  disableAerial: false,
  //change style class button
  disableClass: '',
  clusterLayer: null,
  layersGenerated: false,
  layersLoadingAsync: []
}

// getters
const getters = {
  /*
  Gets layer group from layer group store
  */
 getLayerGroupByName: (state) => (layerGroupName) => {
    if (state.layerGroups[layerGroupName])
      return state.layerGroups[layerGroupName];
    
    return false;
  },
  /*
  Gets layer from layer store (displayed or hidden)
  */
  getLayerByName: (state) => (layerName) => {
    if (state.layers[layerName])
      return state.layers[layerName];

    return false;
  },
  /*
  Gets layer from layer store (displayed or hidden)
  */
  getLayerStyles: (state) => {
    if (state.layerStyles)
      return state.layerStyles;

    return false;
  },
  /*
  True if layers have been loaded and are ready to be added to layer toolbar
  */
  areLayersReady: (state) => {
    if (state.layersGenerated && !state.layersLoadingAsync.length)
      return true;

    return false;
  },
}

// actions
const actions = {
}

// mutations
const mutations = {
  /*
  Adds layer group into layer group store, and sets it as visible if position and initial position are defined
  */
  addLayerGroup(state, layerGroup: LayerGroup) {
    if(layerGroup){
      //if not already in store, add it
      if(!state.layerGroups[layerGroup.name]){
        state.layerGroups[layerGroup.name] = layerGroup;
      } 
      else {
        console.log("layer group "+layerGroup.name+" already exists in store");
      }
    }
  },
  createLayerGroupAndAdd(state, layerGroupConstructorObject) {
    const newLayerGroup = new LayerGroup(layerGroupConstructorObject);
    this.commit("addLayerGroup", newLayerGroup);
  },
  /*
    Adds layer into layer store (if not there already), and sets it as visible if position and initial position are defined.
    Also adds to layergroup.
  */
  addLayer(state, layer: Layer) {
    if(layer){
      if(!state.layers[layer.name]){
        state.layers[layer.name] = layer;
      } 
      else {
        console.log("layer "+layer.name+" already exists in store");
      }

      if (layer.layer_group_name) {
        let layerGroup = (this.getters.getLayerGroupByName(layer.layer_group_name) as any);
        if (layerGroup) layerGroup.addLayer(layer);
      }
    }
  },
  createLayerAndAdd(state, layerConstructorObject) {
    const newLayer = new Layer(layerConstructorObject);
    this.commit("addLayer", newLayer);
  },
  createGeoJSONLayerAndAdd(state, layerProperties) {
    let source = null;
    
    if (layerProperties['geojsonObject']) {
      source = {
        type: 'GeoJSON',
        url: null,
        geojson: { object: layerProperties.geojsonObject },
      };
    }
    else {
      source = {
        type: 'GeoJSON',
        url: layerProperties.url,
      };
    }

    state.layersLoadingAsync.push(layerProperties.name);

    Promise.resolve(state.layerStyles[layerProperties.name])
    .then((style) => {
      const layerConstructorObject = {
        name: layerProperties.name,
        display_name: layerProperties.display_name,
        group: layerProperties.group,
        source: source,
        index: layerProperties.index,
        minResolution: layerProperties.minResolution,
        maxResolution: layerProperties.maxResolution,
        show_in_toolbar: layerProperties.show_in_toolbar,
        switch_on_off: layerProperties.switch_on_off,
        style: style,
        visibility: layerProperties.visibility,
        type: layerProperties.layer_type,
        attributes_exist: layerProperties.attributes_exist,
        surveys_exist: layerProperties.surveys_exist,
        layer_group_name: layerProperties.layer_group_name
      };

      this.commit("createLayerAndAdd", layerConstructorObject);

      state.layersLoadingAsync = state.layersLoadingAsync.filter((val) => val !== layerProperties.name);
    });
  },
  createClusterLayerAndAdd(state, layerProperties) {
    const source = {
      type: 'Cluster',
      distance: layerProperties.distance,
      url: layerProperties.url
    };

    Promise.resolve(state.layerStyles[layerProperties.name])
    .then((style) => {
      const layerConstructorObject = {
        name: layerProperties.name,
        display_name: layerProperties.display_name,
        index: layerProperties.index,
        group: layerProperties.group,
        source: source,
        minResolution: layerProperties.minResolution,
        maxResolution: layerProperties.maxResolution,
        show_in_toolbar: layerProperties.show_in_toolbar,
        switch_on_off: layerProperties.switch_on_off,
        style: style,
        visibility: layerProperties.visibility,
        layer_group_name: layerProperties.layer_group_name
      };

      this.commit("createLayerAndAdd", layerConstructorObject);
    });
  },
  setClusterLayer(state, layer) {
    state.clusterLayer = layer;
  },
  setDisplayGroups(state, displayGroups) {
    state.displayGroups = displayGroups;
  },
  setWasAerialVisible(state, bool: boolean) {
    state.wasAerialVisible = bool;
  },
  setAerialLayer(state, bool: boolean) {
    state.aerialLayer = bool;
  },
  /**
   * Disable or Enable Aerial Layer, including button in layer toolbar
   */
  toggleAerial(state, bool: boolean) {
    if(state.aerialLayer){
      state.disableAerial = bool;
      if (bool)
        state.disableClass = 'disable-layer-btn';
      else
        state.disableClass = '';
    }
  },
  setPlansLayer(state, bool: boolean) {
    state.plansLayer = bool;
  },
  setLayersGenerated(state, bool: boolean) {
    state.layersGenerated = bool;
  },
}

export default {
  state,
  getters,
  actions,
  mutations
};

(window as any).MapLayers = state;