const state = {
  angularMapController: null
}

// getters
const getters = {
  angularInjector: (state) => (type) => {
    if (state.angularMapController) {
      try {
        return state.angularMapController.injector().get(type);
      }
      catch (e) {
        return null;
      }
    }
    else
      return null;
  },
  notificationHelper: (state,getters) => {
    return getters.angularInjector('notificationHelper');
  },
  styleService: (state,getters) => {
    return getters.angularInjector('styleService');
  },
  memorialService: (state,getters) => {
    return getters.angularInjector('memorialService');
  },
  offlineService: (state,getters) => {
    return getters.angularInjector('offlineService');
  },
  featureHelperService: (state,getters) => {
    return getters.angularInjector('featureHelperService');
  },
  personInteractionService: (state,getters) => {
    return getters.angularInjector('personInteractionService');
  },
  featureOverlayService: (state,getters) => {
    return getters.angularInjector('featureOverlayService');
  },
  reportingService: (state,getters) => {
    return getters.angularInjector('reportingService');
  },
  toolbarService: (state,getters) => {
    return getters.angularInjector('toolbarService');
  },
  interactionService: (state,getters) => {
    return getters.angularInjector('interactionService');
  },
  markerService: (state,getters) => {
    return getters.angularInjector('markerService');
  },
  eventService: (state,getters) => {
    return getters.angularInjector('eventService');
  },
  addGraveService: (state,getters) => {
    return getters.angularInjector('addGraveService');
  },
  personService: (state,getters) => {
    return getters.angularInjector('personService');
  },
  mapService: (state,getters) => {
    return getters.angularInjector('MapService');
  },
  exportMapService: (state,getters) => {
    return getters.angularInjector('exportMapService');
  },
  modalHelperService: (state,getters) => {
    return getters.angularInjector('modalHelperService');
  },
  reservedPersonService: (state,getters) => {
    return getters.angularInjector('reservedPersonService');
  },
  geometryHelperService: (state,getters) => {
    return getters.angularInjector('geometryHelperService');
  },
  layerGenerator: (state,getters) => {
    return getters.angularInjector('layerGenerator');
  },
  floatingMemorialToolbarService: (state,getters) => {
    return getters.angularInjector('floatingMemorialToolbarService');
  },
  floatingPlotToolbarService: (state,getters) => {
    return getters.angularInjector('floatingPlotToolbarService');
  },
  layerSelectionService: (state,getters) => {
    return getters.angularInjector('layerSelectionService');
  }
}

// actions
const actions = {
}

// mutations
const mutations = {
  commitAngularMapController (state, value) {
    state.angularMapController = value;
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
