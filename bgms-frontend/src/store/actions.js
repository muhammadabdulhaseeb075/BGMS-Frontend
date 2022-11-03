//import { setDefaultResultOrder } from "dns";
import http from "src/services/http";
import { storeKey } from "vuex";



const actions = {
    async selectSite({ commit, dispatch, getters }, siteId) {   
        if(this.debug) console.log("selectSite called for " + siteId);     
        const currentSiteId = getters.getCurrentSite;
        const previousSiteId = getters.previousSiteId;
        if(currentSiteId != null && currentSiteId != siteId){
            commit("changePrevCurrentSiteId", currentSiteId);
        } else if(currentSiteId === null){
            commit("changePrevCurrentSiteId", siteId);
        }
        commit("changeCurrentSiteId", siteId);
        const newBooking = getters.newBooking;
        
        if(newBooking === true && previousSiteId != null && previousSiteId != ""){
            commit("openSiteSelectConfirm", siteId);                
        }
        else{
            await dispatch("requestFuneralDirectors");
            await dispatch("requestMeetingLocations");
            await dispatch("requestMapSections");
        }     
    },

    /**
     * Get all sites available for user. Will only hit the server once when multiple components loaded.
     * - To force a load from server set 'store.sitesFetched' to 'false'. (Or call mutation 'toggleSitesFetched'.)
     * - Result is stored in 'store.sites[]'
     */
    async getSitesForUser({ commit, getters }) {
        try {   
            if(!(getters.getSitesFetched)){ //if the site list has not been fetched getSitesFetched will return false
                if(this.isDebug) console.log("Fetching site list for user. ");
                commit("toggleSitesFetched"); //toggle sitesFetched to true to prevent multiple server requests
                const response = await http.get("/userAccess"); //TODO:The server request is _very_ slow and needs refactoring but is not an issue for the current use case.
                commit("addSites", response.data);     
                commit("toggleSitesFetchCompleted");   
            }else{
                if(this.isDebug) console.log("Site list already fetched. ");
            }        
        }catch(error){
            console.error("Error couldn't fetch sites for user. ", error);
        }
    },

    /**
     * 
     */
    async logout() {
        window.location.assign("/logout");
    },

    /**
     * Gets a list of Funeral Directors for the current site. 
     * @param {*} param0 
     */
    async requestFuneralDirectors({ commit, getters }) {          
        try {     
            let site  = getters.currentSite;          
            const { domain_url } = site;            
            const response = await http.get(`${domain_url}/cemeteryadmin/funeralDirectorsList/`);

            commit("addFuneralDirectors", response.data);
        } catch(error) {
            console.error("Error Couldn't get funeral directors:", error);
        }
    },
    async requestFuneralDirectorsBySite({ commit, getters }, site_id) {
        debugger; // eslint-disable-line no-debugger
        try {
            let site  = getters.getSiteById(site_id);
            const { domain_url } = site;
            const response = await http.get(`${domain_url}/cemeteryadmin/funeralDirectorsList/`);

            commit("addSearchFormFuneralDirectors", response.data);
        } catch(error) {
            console.error("Error Couldn't get funeral directors:", error);
        }
    },
    async addNotification({commit}, notification ) {
        try {
            commit('addOneNotification', notification);
        }catch (error){
            console.error("Error Couldn't add notification:", error);
        }
    },
    async removeNotification({commit}, notification ) {
        try {
            commit('removeNotification', notification);
        }catch (error){
            console.error("Error Couldn't remove notification:", error);
        }
    },

     /**
     * Gets a list of Meeting Locations for the current site. 
     * @param {*} param0 
     */
    async requestMeetingLocations({ commit, getters }){
        try{
            let site = getters.currentSite;
            const { domain_url } = site;
            if(this.isDebug) console.log("Getting Meeting Locations for " + '${domain_url}');
            const response = await http.get(`${domain_url}/cemeteryadmin/meetingLocationsList/`);

            commit("addMeetingLocations", response.data);
        }catch(error) {
            console.error("Error Couldn\'t get meeting locations:", error);
        }
    },

     /**
     * Gets a list of Meeting Locations for the current site. 
     * @param {*} param0 
     */
    async requestMapSections({commit, getters}){
        try{
            let site = getters.currentSite;
            const { domain_url } = site;
            if(this.isDebug) console.log("Getting Map Sections for " + '${domain_url}');

            const response = await http.get(`${domain_url}/mapmanagement/getSections/`);
            commit("addMapSections", response.data);
            commit("addselectedMapSection", null);       
        }catch(error) {
            console.error("Error Couldn\'t get map sections:", error);
        }
    },
    async isDebug() {
        return false;
    },
};

export default actions
