const BLOCKED_ROUTES = ["root"];

function parseRoutes({ name, path, meta, children = [] }) {
    let parsedChildren = children
        // remove entry point subroute which is basically same parent root
        .filter((sub) => !!(sub.path && sub.name))
        .map(parseRoutes);

    return {
        name,
        path,
        meta,
        children: parsedChildren,
    };
}

const mutations = {
    addSites(state, { sites, sitemanagement}) {
        state.sites = sites;
        state.sitemanagement = sitemanagement;
    },

    toggleSitesFetched(state) {
        if(state.sitesFetched){ state.sitesFetched = false; }
        else{ state.sitesFetched = true }
    },

    toggleSitesFetchCompleted(state) {
        //console.log("Toggling SiteFetchCompleted");
        if(state.sitesFetchCompleted){ state.sitesFetchCompleted = false; }
        else{ state.sitesFetchCompleted = true }
    },

    changeCurrentSiteId(state, siteId) {
        state.currentSiteId = siteId;
    },

    addRoutes(state, routes) {
        const parsedRoutes = routes
            .filter(route => !(BLOCKED_ROUTES.includes(route.name)))
            .map(parseRoutes);
        
        state.router.routes = parsedRoutes;
    },

    addFuneralDirectors(state, directors) {
        state.funeralDirectors = directors;
    },

    addSearchFormFuneralDirectors(state, directors) {
        debugger; // eslint-disable-line no-debugger
        directors.forEach(o => {
            state.searchFormFuneralDirectors.push(o);
        });
    },
    clearSearchFormFuneralDirectors(state) {
        debugger; // eslint-disable-line no-debugger
        state.searchFormFuneralDirectors = [];
    },


    addOneFuneralDirector(state, director) {
        //debugger; // eslint-disable-line no-debugger
        state.funeralDirectors.push(director);
    },    
    updateOneFuneralDirector(state, director) { //update an exiting funeral director
        //debugger; // eslint-disable-line no-debugger
        const index = state.funeralDirectors.findIndex(item => item.id === director.id);
        state.funeralDirectors.splice(index, 1); //delete the object currently in the Vuex store
        //now just add the new object (easier than modifying in place?)
        state.funeralDirectors.push(director);
    },
    addOneNotification (state, notification) {
        state.notifications.push(notification);
    },
    removeNotification (state, notificationToRemove) {
        state.notifications = state.notifications.filter(notification => {
            return notification.id != notificationToRemove.id;
        });
    },
    openSiteSelectConfirm(state, siteId) {
        state.selectedSiteId = siteId;
        state.showSiteSelectConfirm = true;
    },

    updateNewBooking(state, book){
        state.newBooking = book;
    },
    changePrevCurrentSiteId(state, siteId){
       
        state.previousSiteId = siteId;
    },
    clearPrevSiteId(state){
        state.previousSiteId = null;
    },
    addMeetingLocations(state, locations) {
        state.meetingLocations = locations;
    },
    addMapSections(state, sections) {
        if(sections == null){
            state.mapSections = [];
        }else{
            state.mapSections = sections;
        }
       
    },
    addselectedMapSection(state, sectionid){
        state.selectedMapSection = sectionid;
    }
};

export default mutations;
