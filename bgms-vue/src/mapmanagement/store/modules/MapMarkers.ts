import store from '@/mapmanagement/store/index';
import Vue from 'vue'
import MapMarker from '@/mapmanagement/components/Map/models/Marker';

// add jquery events to be used in angularjs
(window as any).jQuery(document).on("pushMarker", (e,marker) => {
  store.commit('pushMarker', marker);
});
(window as any).jQuery(document).on("removeMarkerByName", (e,marker) => {
  store.commit('removeMarkerByName', marker);
});
(window as any).jQuery(document).on("removeMarkerById", (e,marker) => {
  store.commit('removeMarkerById', marker);
});
(window as any).jQuery(document).on("removeMarkersByGroup", (e,marker) => {
  store.commit('removeMarkersByGroup', marker);
});

function getMarkerPositionInStack(key, value) {
  let positions = [];

  store.getters.getMarkers.forEach((marker, index) => {
    if(marker[key] === value){
      positions.push(index);
    }
  });

  return positions;
}

const state = {
  markers: [],
  markerIndex: 0,
  bookingForm: null,
  redirectMetadata: null,
  sectionCoords: [],
}

// getters
const getters = {
  getMarkers: (state) => {
    return state.markers;
  },
  getMarkerPositionInStack: (state) => (key, value) => {
    return getMarkerPositionInStack(key, value);
  },
  getBookingForm: (state) => {
    return state.bookingForm;
  },
  getRedirectMetadata: (state)  => {
    return state.redirectMetadata;
  },
  getSectionCoords: (state) =>{
    return state.sectionCoords;
  }
 }

// actions
const actions = {
}

// mutations
const mutations = {

  setBookingForm(state, bookingForm) {
    state.bookingForm = bookingForm;
  },

  setRedirectMetadata(state, redirectInfo) {
    state.redirectMetadata = redirectInfo;
  },

  pushMarker(state, marker) {

    let newMarker = new MapMarker(marker, state.markerIndex);
    state.markers.push(newMarker);
    state.markerIndex += 1;

    Vue.nextTick(() => {
      newMarker.addMarkerToMap();
    });
  },

  removeMarkerByName(state, markerName){
    const positions = getMarkerPositionInStack('name', markerName);
    if(positions.length) {
      state.markers[positions[0]].removeMarkerFromMap();
      state.markers.splice(positions[0], 1);
    }
  },

  removeMarkerById(state, featureId){
    const positions = getMarkerPositionInStack('featureId', featureId);
    if(positions.length) {
      state.markers[positions[0]].removeMarkerFromMap();
      state.markers.splice(positions[0], 1);
    }
  },

  removeMarkersByGroup(state, markerGroup){
    const positions = getMarkerPositionInStack('group', markerGroup);
    if(positions.length !== null) {
      for(let i=positions.length-1; i>=0; i--){
        state.markers[positions[i]].removeMarkerFromMap();
        state.markers.splice(positions[i], 1);
      }
    }
  },
  setSectionCoords(state, coords){
    state.sectionCoords = coords;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};

(window as any).MapMarkers = state.markers;