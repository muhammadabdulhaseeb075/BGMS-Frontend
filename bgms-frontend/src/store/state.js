import { routes } from "/src/router";

const state = {
    title: "BGMS Cemetery Management",
    user: document.user,
    router: {
        routes: {},
    },
    currentSiteId: null,
    sitemanagement: null,
    sitesFetched: false,  
    sitesFetchCompleted: false,  
    sites: [],
    funeralDirectors: [],
    searchFormFuneralDirectors: [],
    eventForm:null,
    notifications: [],
    newBooking: false,
    showSiteSelectConfirm: false,
    selectedSiteId: null,
    previousSiteId: null,
    meetingLocations: [],
    mapSections: [],
    selectedMapSection: null,
};

export default state;
