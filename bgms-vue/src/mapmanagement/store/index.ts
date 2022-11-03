import Vue from 'vue'
import Vuex from 'vuex'
import axios, {AxiosResponse} from 'axios'
import MemorialSidebar from './modules/MemorialSidebar'
import ManagementTool from './modules/ManagementTool'
import MemorialCaptureSidebar from './modules/MemorialCaptureSidebar'
import AngularMapController from './modules/AngularMapController'
import Offline from './modules/Offline'
import Styles from './modules/Styles'
import ExportMap from './modules/ExportMap'
import MapLayers from './modules/MapLayers'
import MapEvents from './modules/MapEvents'
import MapMarkers from './modules/MapMarkers'
import MapInteractions from './modules/MapInteractions'
import MapFeatureOverlays from './modules/MapFeatureOverlays'
import Feature from "@/mapmanagement/components/Map/models/Feature";
import Memorial from "@/typings/Memorial";

Vue.use(Vuex)

Vue.config.devtools = process.env.NODE_ENV === "development";

let store = new Vuex.Store({
  actions: {
    populateMemorialLayers({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/geometries/getAllLayerNames/')
        .then(response => {
          
          let memorialLayers = response.data.layer_groups.filter(x => x.group_code === "memorials")[0].layers;
          memorialLayers.sort(function(a,b) {return (a.display_name > b.display_name) ? 1 : ((b.display_name > a.display_name) ? -1 : 0);} );
          commit('populateMemorialLayers', memorialLayers);
          resolve();
        })
        .catch(response => {
          console.warn('Couldn\'t get memorial layers:', response);
          reject();
        });
      });
    },
    getIncludeGravesInSearchValue({ state }) {
      return new Promise((resolve, reject) => {
        axios.get('/mapmanagement/includeGravesInSearch/')
        .then(response => {
          
          state.includeGravesInSearch = response.data.include;
          resolve();
        })
        .catch(response => {
          console.warn('includeGravesInSearch api failed:', response);
          reject();
        });
      });
    },
    editMemorial({ state }, editedMemorial: Pick<Feature, 'id_'>) {
      return new Promise((resolve, reject) => {
        axios.get(`/mapmanagement/memorialDetails/?memorial_uuid=${editedMemorial.id_}`).then(
            (response: AxiosResponse<Partial<Memorial>>) => {
                state.memorialEdited = response.data
              resolve();
            }).catch(error => {
              console.warn('getEditedMemorial api failed:', error);
            }
        )
      })
    }
  },
  state: {
    exportMapOpen: false,
    memorialLayers: undefined,
    includeGravesInSearch: null,
    allSections: undefined,
    allSubsections: undefined,
    allFeatureIDs: undefined,
    siteAdmin: false,
    siteAdminOrSiteWarden: false,
    agStaff: false,
    memorialPhotographyAccess: false,
    dataEntryAccess: false,
    dataMatcherAccess: false,
    authenticatedSession: false,
    isBacasEnabled: false,
    memorialEdited: undefined,
    graveNumber: undefined,
    StepNumber: undefined,
    returnLink: undefined,
  },
  mutations: {
    opencloseExportMap(state, value: boolean) {
      state.exportMapOpen = value
    },
    populateMemorialLayers (state, memorialLayers) {
      state.memorialLayers = memorialLayers;
    },
    populateSections (state, sections) {
      state.allSections = sections;
    },
    populateSubsections (state, subsections) {
      state.allSubsections = subsections;
    },
    populateFeatureIDs (state, featureIDs) {
      state.allFeatureIDs = featureIDs;
    },
    // SiteAdmin includes SiteWarden, SiteWarden includes memorial photography, DataEntry & DataMatcher access
    setSiteAdminAccess (state) {
      state.siteAdmin = true;
      state.siteAdminOrSiteWarden = true;
      state.memorialPhotographyAccess = true;
      state.dataEntryAccess = true;
      state.dataMatcherAccess = true;
    },
    setSiteAdminOrSiteWardenAccess (state) {
      state.siteAdminOrSiteWarden = true;
      state.memorialPhotographyAccess = true;
      state.dataEntryAccess = true;
      state.dataMatcherAccess = true;
    },
    setMemorialPhotographyAccess (state) {
      state.memorialPhotographyAccess = true;
    },
    setAgStaffAccess (state) {
      state.agStaff = true;
    },
    setDataEntry (state) {
      state.dataEntryAccess = true;
    },
    setDataMatcher (state) {
      state.dataMatcherAccess = true;
    },
    setAuthenticatedSession (state) {
      state.authenticatedSession = true;
    },
    setIsBacasEnabled (state) {
      state.isBacasEnabled = true;
    },
    setGraveNumber (state, graveNumber) {
      state.graveNumber = graveNumber;
    },
    setStepNumber(state, stepNumber){
      state.StepNumber = stepNumber;
    },
    setReturnLink(state, bookingURL){
      state.returnLink = bookingURL;
    }
  },
  modules: {
    MemorialSidebar,
    ManagementTool,
    MemorialCaptureSidebar,
    AngularMapController,
    Offline,
    Styles,
    ExportMap,
    MapLayers,
    MapEvents,
    MapMarkers,
    MapInteractions,
    MapFeatureOverlays
  }
})

// hot reloading
if ((module as any).hot) {
  // accept actions and mutations as hot modules
  (module as any).hot.accept(['./modules/MemorialSidebar', './modules/ManagementTool', './modules/MemorialCaptureSidebar', './modules/AngularMapController', './modules/Offline', './modules/Styles', './modules/ExportMap', './modules/MapLayers', './modules/MapEvents', './modules/MapMarkers', './modules/MapInteractions', './modules/MapFeatureOverlays'], () => {
    // require the updated modules
    // have to add .default here due to babel 6 module output
    const MEMORIALSIDEBAR = require('./modules/MemorialSidebar').default;
    const MANAGEMENTTOOL = require('./modules/ManagementTool').default;
    const MEMORIALCAPTURESIDEBAR = require('./modules/MemorialCaptureSidebar').default;
    const ANGULARMAPCONTROLLER = require('./modules/AngularMapController').default;
    const OFFLINE = require('./modules/Offline').default;
    const STYLES = require('./modules/Styles').default;
    const EXPORTMAP = require('./modules/ExportMap').default;
    const MAPLAYERS = require('./modules/MapLayers').default;
    const MAPEVENTS = require('./modules/MapEvents').default;
    const MAPMARKERS = require('./modules/MapMarkers').default;
    const MAPINTERACTIONS = require('./modules/MapInteractions').default;
    const MAPFEATUREOVERLAYS = require('./modules/MapFeatureOverlays').default;
    
    // swap in the new actions and mutations
    this.$store.hotUpdate({
      modules: {
        MemorialSidebar: MEMORIALSIDEBAR,
        ManagementTool: MANAGEMENTTOOL,
        MemorialCaptureSidebar: MEMORIALCAPTURESIDEBAR,
        AngularMapController: ANGULARMAPCONTROLLER,
        Offline: OFFLINE,
        Styles: STYLES,
        ExportMap: EXPORTMAP,
        MapLayers: MAPLAYERS,
        MapEvents: MAPEVENTS,
        MapMarkers: MAPMARKERS,
        MapInteractions: MAPINTERACTIONS,
        MapFeatureOverlays: MAPFEATUREOVERLAYS
      }
    });
  })
}

export default store;

// Watch for when the layers have all been loaded
// Then generate the layer groups to be displayed in layer toolbar or legend
let unwatchLayerGenerated = store.watch(
  (state, getters) => getters.areLayersReady, (newValue, oldValue) => {
    if (newValue) {
      let layerGroups = (store.state as any).MapLayers.layerGroups;
      let displayLayerGroups = {};
      
      for (let i in layerGroups) {
        let displayedLayers = {};
        for (let j in layerGroups[i].layers) {
          displayedLayers[j] = true;
        }
  
        const displayGroup = {
          isPanelDisplayed: layerGroups[i].show_in_toolbar(),
          layerGroup: layerGroups[i],
          displayedLayers: displayedLayers
        };

        displayLayerGroups[layerGroups[i].name] = displayGroup;
      }

      store.commit('setDisplayGroups', displayLayerGroups);
      
      // set cluster layer
      if(displayLayerGroups['memorial_cluster']) {
        const layerGroup = store.getters.getLayerGroupByName('memorials');
        if(layerGroup)
        store.commit('setClusterLayer', layerGroup);
        else
        store.commit('setClusterLayer', store.getters.getLayerByName('plot'));
      }

      window.setTimeout(() => {
        // remove watcher once groups are loaded
        unwatchLayerGenerated();
      });
    }
  }, { immediate: true }
);
