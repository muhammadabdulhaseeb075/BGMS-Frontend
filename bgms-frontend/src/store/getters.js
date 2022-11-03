const getters = {
    sites(state) {
        return state.sites;
    },

    getSitesFetched(state){ 
        return state.sitesFetched;
    },

    getSitesFetchCompleted(state){ 
        return state.sitesFetchCompleted;
    },

    allowedSitesFromBereavementStaff(state){
        return state.sites.filter(currentSite => currentSite?.bereavement_staff);
    },

    currentSite(state) { //returns the current site object based on the value store.currentSiteId
        //debugger; // eslint-disable-line no-debugger        
        const siteId = parseInt(state.currentSiteId); //using the select option, sometimes the value comes in as a string        
        let site = null;
        if(siteId) {            
            //console.log("Getting site object for SiteId: " + siteId);
            let sites_t = state.sites;                                                      
            site = sites_t.find(site => site.id === siteId) || null; //TODO: Maybe the sites[] array should be keyed to site.id?            
        }
        return site;
    },

    //Return a site from the array based on id value instead of array index
    getSiteById: (state) => (id) => {
        //debugger; // eslint-disable-line no-debugger   
        let sites_t = state.sites;
        let site = sites_t.find(site =>site.id === id )
        return site;
    },

    //just return all the sites
    getSiteList(state) {
        //debugger; // eslint-disable-line no-debugger   
        //let sites_t = state.sites;
        let sites_t = state.sites.filter(currentSite => currentSite?.bereavement_staff);
        return sites_t;
    },

    getCurrentSite(state) {
        return state.currentSiteId;
    },

    currentSiteName(state, getters) {
        return getters.currentSite?.name ?? "";
    },

    currentSiteId(state, getters) {
        return getters.currentSite?.id ?? "";
    },

    //Return a single funeral director from the array based on id value instead of array index
    getFuneralDirectorById: (state) => (id) => {
        return state.funeralDirectors.find(funeralDirector => funeralDirector.id === id) //TODO: Maybe should be keyed on funeralDirector.id?
    },

    funeralDirectors(state) {
        return state.funeralDirectors;
    },

    searchFormFuneralDirectors(state) {
        return state.searchFormFuneralDirectors;
    },

    newBooking(state){
        return state.newBooking;
    },
    showSiteSelectConfirm(state){
        return state.showSiteSelectConfirm;
    },
    previousSiteId(state){
        return state.previousSiteId;
    },
    meetingLocations(state){
        return state.meetingLocations;
    },
    mapSections(state){
        return state.mapSections;
    },
    //Return a site from the array based on id value instead of array index
    getSectionById: (state) => (section_id) => {
        debugger; // eslint-disable-line no-debugger
        let sections_t = state.mapSections;
        let section = sections_t.find(section =>section.id === section_id );
        return section;
    },
};

export default getters;
