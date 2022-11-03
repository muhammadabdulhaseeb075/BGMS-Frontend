import axios from 'axios'

const hash = require('object-hash');

const state = {
  // Do not write a commit for this! That will create a new obj ref which will break things.
  selectedSitesIds: [],
  funeralDirectors: [],

  // This is currently duplicated in backend. We should retrieve these choices from there.
  bookingStatusChoices: [
    // commented can be enabled when funeral directors portal is built
    //{ value: 0, text: 'Provisional' },
    //{ value: 1, text: 'Pending' },
    { value: 2, text: 'Pre-Burial Checks' },
    { value: 3, text: 'Awaiting Burial' },
    { value: 4, text: 'Post-Burial Checks' },
    { value: 5, text: 'Completed' },
    //{ value: 6, text: 'Declined' },
    { value: 7, text: 'Cancelled' }
  ],

  /** Booking form */
  bookingDetails: null,
  unmodifiedBookingDetailsHash: null,
  graveplotTypes: {},

  /** Calendar */
  allEvents: [],
  loadedMonths: {},

  /** Funeral booking table */
  funeralBookingCreators: [],
  funeralTableOptions: {
    sortBy: ['start_date'],
    sortDesc: [true]
  },
  funeralTableFilters: {
    status: [2,4]
  }
}

// getters
const getters = {
  /**
   * Returns events that meet criteria
   * @param {number} siteID
   * @param {string} date Start date of event (YYYY-MM-dd)
   * @param {string} eventTypeCategoryID 
   * @param {string} exludedEventID Exclude this event from result
   */
  getEventsInSameCategoryAndDay: state => (siteID: number, date: string, eventTypeCategoryID: string, exludedEventID: string) => {
    if (state.allEvents && state.allEvents[siteID]) {

      return state.allEvents[siteID].filter(event => {
        return event.id !== exludedEventID && event.event_category === eventTypeCategoryID && event.start.substring(0, 10) === date;
      });
    }

    return null;
  },
  /**
   * Returns graveplot types for given site
   * @param {number} siteID
   */
  /*getGraveplotTypesForSite: state => (siteID: number) => {
    if (state.graveplotTypes && siteID in state.graveplotTypes) {
      if (!state.graveplotTypes[siteID])
        return [];
      else
        return state.graveplotTypes[siteID];
    }

    return null;
  }*/
}

// actions
const actions = {
  /**
   * Get funeral directors registered to site's client.
   * Note: we're assuming only one client is in use!
   * @param siteID 
   */
  getFuneralDirectors({ commit, getters }, siteID) {
    return new Promise((resolve, reject) => {

      const site = getters.getSiteFromId(parseInt(siteID));

      axios.get(site.domain_url + "/cemeteryadmin/funeralDirectorsList/")
      .then(response => {
        commit('populateFuneralDirectors', response.data);
        resolve();
      })
      .catch(response => {
        console.warn('Couldn\'t get funeral directors:', response);
        reject();
      });
    });
  }

  /**
   * Get graveplot types for site.
   * @param siteID 
   */
  /*getGraveplotTypes({ commit, getters }, siteID) {
    return new Promise((resolve, reject) => {

      const site = getters.getSiteFromId(parseInt(siteID));

      axios.get(site.domain_url + "/api/graveplotType/all/")
      .then(response => {
        commit('populateGraveplotTypes', { siteID: siteID, data: response.data });
        resolve();
      })
      .catch(response => {
        console.warn('Couldn\'t get graveplot types:', response);
        reject();
      });
    });
  }*/
}

// mutations
const mutations = {

  populateFuneralDirectors(state, funeralDirectors) {
    state.funeralDirectors.push.apply(state.funeralDirectors, funeralDirectors);
  },

  /** Booking form */
  commitBookingDetails (state, bookingDetails) {
    state.bookingDetails = bookingDetails;
    state.unmodifiedBookingDetailsHash = hash(bookingDetails);
  },
  modifyBookingDetails (state, detail) {
    state.bookingDetails[detail.key] = detail.value;
  },
  modifyCalendarEventDetails (state, detail) {
    state.bookingDetails.calendar_event[detail.key] = detail.value;
  },
  modifyPersonDetails (state, detail) {
    state.bookingDetails.person[detail.key] = detail.value;
  },
  /*populateGraveplotTypes(state, param) {
    state.graveplotTypes[param.siteID] = param.data;
  },*/

  /** Funeral booking table */
  commitFuneralTableOptions (state, options) {
    state.funeralTableOptions = options;
  },
  // reset filters to initial
  resetFuneralTableFilters (state) {
    state.funeralTableFilters['status'].length = 0;
    state.funeralTableFilters['status'].push.apply(state.funeralTableFilters['status'], [2,4]);
    state.funeralTableFilters = {
      status: state.funeralTableFilters['status']
    };
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
