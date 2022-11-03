import {mapGetters, mapActions, mapMutations} from "vuex";
import { BOOKING_ADD_NAME, BOOKING_STATUS_NAME } from "../../constants";
import { urlQueries } from "../../../../services/http/helpers";
import {createEvent} from "src/router/Booking/module/actions";
const props = {
    title: {type: String, default: "View"},
};
const ZOOM_IN_QUERY = "zoomIn";
const ADMIN_DOMAIN = "adminDomain";
const SITE_SELECTED_QUERY = "siteId";
const FORM_CACHE_QUERY = "searchForm";

const computed = {
    ...mapGetters(["allowedSitesFromBereavementStaff", "currentSite", "getSiteById"]),
    ...mapGetters("booking", ["searchResultEvent", "totalRows", "searchEventCriteria"]),
};

const methods = {
    ...mapActions("booking", ["getEvent"]),
    ...mapGetters(["getSiteById"]),
    ...mapMutations(["changeCurrentSiteId"]),

    getSiteName(siteId) {
        let siteName = "";

        if (this.allowedSitesFromBereavementStaff.length) {
            const site = this.allowedSitesFromBereavementStaff.find(site => site.id === siteId);
            siteName = site ? site.name : "";
        }

        return siteName;
    },

    getSiteDomain(siteId) {
        //debugger; // eslint-disable-line no-debugger
        let siteDomain = "";
        let site = this.getSiteById(siteId);
        if(site) {
            siteDomain = site.domain_url;
        }
        /*
        if (this.allowedSitesFromBereavementStaff.length) {
            const site = this.allowedSitesFromBereavementStaff.find(site => site.id === siteId);
            siteName = site ? site.name : "";
        }*/

        return siteDomain;
    },

    editEvent(eventId, siteId) {
        //debugger; // eslint-disable-line no-debugger
        // send it to the new booking form to start editing
        //let domain = this.getSiteDomain(siteId);
        this.$router?.push({ name: BOOKING_ADD_NAME, query: { eventId, siteId }});
    },

    async editStatus(eventId, siteId) {
        //debugger; // eslint-disable-line no-debugger
        // send it to the status form to start editing
        this.changeCurrentSiteId(siteId); //currentSiteId is used by the getEvent method called next
        const eventData = await this.getEvent(eventId); //getEvent also maps the fetched event to the current booking in vuex
        this.$router?.push({ name: BOOKING_STATUS_NAME, query: { eventId, siteId } });
    },

    async openMapWithGravePlot(mapManagement, siteId) {
        debugger; // eslint-disable-line no-debugger
        const {
            grave_plot_uuid,
            topopolygon_id,
            memorial_uuid,
            layer_type
        } = mapManagement;
        const queriesParams = {};
        const site = this.allowedSitesFromBereavementStaff.find(site => site.id === siteId);
        const baseURL = site?.domain_url ?? this.currentSite?.domain_url;
        queriesParams[ZOOM_IN_QUERY] = true;
        //Add params similar to event form to allow return from map.
        queriesParams[ADMIN_DOMAIN] = encodeURIComponent(window.location.origin);
        queriesParams[SITE_SELECTED_QUERY] = siteId;
        queriesParams["search"] = true;

        //encode current search criteria
        let search_criteria = this.searchEventCriteria;
        const jsonForm = JSON.stringify(search_criteria);
        const encode = btoa(jsonForm);
        queriesParams[FORM_CACHE_QUERY] = encode; //cachedForm;


        const encodeQueries = urlQueries(queriesParams);


        if(baseURL && grave_plot_uuid) {
            if (topopolygon_id) {
                // Available graveplot.
                const siteMapURL = `${baseURL}/mapmanagement/#/gravemanagement/${grave_plot_uuid}/available_plot/${topopolygon_id}?${encodeQueries}`;
                window.location.assign(siteMapURL);   
            } else {
                // Custom graveplot from memorial.
                const siteMapURL = `${baseURL}/mapmanagement/#/gravemanagement/${grave_plot_uuid}/plot?${encodeQueries}`;
                window.location.assign(siteMapURL);
            }
        }
        
        if(baseURL && memorial_uuid && layer_type) {
            // Custom memorial.
            const siteMapURL = `${baseURL}/mapmanagement/#/memorialmanagement/${memorial_uuid}/${layer_type}?${encodeQueries}`;
            window.location.assign(siteMapURL);
        }
    },

    funeralDirectorOption(funeral_director_name, funeral_director_title, funeral_director_company_name,
        funeral_director_last_names) {
        let funeral_director = "";
        if( funeral_director_company_name )
            funeral_director = funeral_director_company_name + ": ";
        if( funeral_director_title ) {
            if (funeral_director_title == 1)
                funeral_director = funeral_director + "Mr. ";
            if (funeral_director_title == 2)
                funeral_director = funeral_director + "Mrs. ";
            if (funeral_director_title == 3)
                funeral_director = funeral_director + "Miss ";
            if (funeral_director_title == 4)
                funeral_director = funeral_director + "Ms. ";
        }
        //funeral_director = funeral_director + funeral_director_title + " ";
        if( funeral_director_name )
            funeral_director = funeral_director + funeral_director_name + " ";
        if( funeral_director_name )
            funeral_director = funeral_director + funeral_director_last_names + " ";
        return funeral_director;
    },
};


export default {
    computed,
    methods,
    props,
};
