enum sideBarTypeEnum { memorialCapture, graveLink }

const state = {
  sideBarType: undefined,
  sideBarTypeEnum: sideBarTypeEnum,
  memorial: undefined,
  markerText: undefined,
  stopSidebarClose: false
}

// getters
const getters = {
  imageCount: state => {
    if (state.memorial)
      return state.memorial.get('images_count') || 0;
    else
      return 0;
  }
}

// actions
const actions = {
}

// mutations
const mutations = {
  updateSidebarType (state, type: sideBarTypeEnum) {
    state.sideBarType = type;
  },
  resetSidebar (state) {
    state.memorial = undefined;
  },
  updateMemorial (state, memorial) {
    state.memorial = memorial;
  },
  modifyMemorialLayer (state, layer) {
    state.memorial.set('marker_type', layer);
  },
  commitMarkerText (state, value) {
    state.markerText = value;
  },
  toggleStopSidebarClose (state, value) {
    state.stopSidebarClose = value;
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
