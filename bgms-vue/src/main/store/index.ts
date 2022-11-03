import Vue from 'vue'
import Vuex from 'vuex'
import Booking from './modules/Booking'

Vue.use(Vuex)

Vue.config.devtools = process.env.NODE_ENV === "development";

export default new Vuex.Store({
  actions: {

  },
  getters: {
    getBereavementStaffAccessSites: state => {
      let returnSites = [];

      if (state.mapmanagementAccessSites) {
        state.mapmanagementAccessSites.map(site => {
          if (site.bereavement_staff)
            returnSites.push(site);
        });
      }
      
      return returnSites;
    },
    getSiteFromId: state => site_id => {
      let returnSite = null;

      if (state.mapmanagementAccessSites) {
        returnSite = state.mapmanagementAccessSites.find(site => site.id === site_id);
      }
      
      return returnSite;
    },
    getEventType: state => (siteID: number, eventTypeID: number) => {
      if (state.mapmanagementAccessSites) {
        const site = state.mapmanagementAccessSites.find(site => site.id === siteID);
        return site.event_types.find(
          event_type => event_type.id === eventTypeID);
      }

      return null;
    }
  },
  state: {
    mapmanagementAccessSites: null,
    sitemanagementAccess: null,
    allSections: {},
    allSubsections: {},
    allGraves: {},
  },
  mutations: {
    commitAccess (state, access) {
      state.mapmanagementAccessSites = access.sites;
      state.sitemanagementAccess = access.sitemanagement;
    },
    populateSections (state, sections) {
      state.allSections = sections;
    },
    populateSubsections (state, subsections) {
      state.allSubsections = subsections;
    },
    populateGraves (state, graves) {
      state.allGraves = graves;
    },
  },
  modules: {
    Booking
  }
})

// hot reloading
if ((module as any).hot) {
  // accept actions and mutations as hot modules
  (module as any).hot.accept(['./modules/Booking'], () => {
    // require the updated modules
    // have to add .default here due to babel 6 module output
    const Booking = require('./modules/Booking').default;
    // swap in the new actions and mutations
    this.$store.hotUpdate({
      modules: {
        Booking: Booking
      }
    });
  })
}