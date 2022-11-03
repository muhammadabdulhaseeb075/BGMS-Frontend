import store from '@/mapmanagement/store/index';
import FeatureOverlay from '@/mapmanagement/components/Map/models/FeatureOverlay';

// add jquery events to be used in angularjs
(window as any).jQuery(document).on("addFeatureOverlay", (e,featureOverlay) => {
  store.commit('addFeatureOverlay', featureOverlay);
});
(window as any).jQuery(document).on("removeAllFeaturesInGroup", (e,groupName) => {
  store.commit('removeAllFeaturesInGroup', groupName);
});

const state = {
  featureOverlayStore: {}
}

// getters
const getters = {
  getFeatureOverlayStore: (state) => {
    return state.featureOverlayStore;
  },
}

// actions
const actions = {
}

// mutations
const mutations = {

  addFeatureOverlay(state, featureOverlay) {

    if (typeof(featureOverlay) === 'string') {
      if (featureOverlay === "hovered-memorials") {
        featureOverlay = {
          name: 'hovered-memorials',
          group: 'person',
          // layerGroup: ['memorials', 'memorial_cluster'],
          layerGroup: ['memorials'],
          style: store.getters.getLayerStyles.selectedStyleFunction
        }
      }
      else if (featureOverlay === "clicked-memorials") {
        featureOverlay = {
          name: 'clicked-memorials',
          group: 'person',
          layerGroup: ['memorials', 'memorial_cluster'],
          style: store.getters.getLayerStyles.selectedStyleFunction
        }
      }
      else if (featureOverlay === "searched-memorials") {
        featureOverlay = {
          name: 'searched-memorials',
          group: 'person',
          layerGroup: ['memorials', 'memorial_cluster'],
          style: store.getters.getLayerStyles.selectedStyleFunction
        }
      }
    }
    
    const newFeatureOverlay = new FeatureOverlay(featureOverlay.name, featureOverlay.group, featureOverlay.style);

    state.featureOverlayStore[featureOverlay.name] = newFeatureOverlay;
  },

  removeAllFeaturesInGroup(state, groupName){
    const featureOverlayStoreKeys = Object.keys(state.featureOverlayStore);
    featureOverlayStoreKeys.forEach(key => {
      let featureOverlay = state.featureOverlayStore[key];
      if(featureOverlay.group === groupName)
        featureOverlay.removeAllFeatures();
    });
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};

(window as any).MapFeatureOverlayStore = state.featureOverlayStore;