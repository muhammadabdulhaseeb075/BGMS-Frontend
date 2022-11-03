import { mapActions, mapGetters, mapMutations } from "vuex";
import InputField from "src/components/fields/input-field";
import { createForm } from "src/utils/forms";

import FormSectionField from "../../components/form-section-field";
import searchFormSchema from "./search-form-schema";


const components = {
    InputField,
    FormSectionField,
};

function data() {
    return {
        searchForm: createForm(searchFormSchema),
    };
}

function mounted() {
    debugger; // eslint-disable-line no-debugger
    const queries = this.$router.currentRoute.value.query;
    let searchForm = null;
    if(queries) {
        const searchFormQuery = queries["searchForm"];
        if (searchFormQuery) {
            searchForm = JSON.parse(atob(searchFormQuery));
            console.log("SEARCH_FRM: " + searchForm);
        }
    }

    this.$emit("setSiteSelectVisibility", {show: false});
}

const computed = {
    ...mapGetters(["allowedSitesFromBereavementStaff", "currentSiteId", "funeralDirectors", "searchFormFuneralDirectors"]),

    siteOptions() {
        return this.allowedSitesFromBereavementStaff.map(({name, id}) => ({value: id, label: name}));
    },

    siteChoices() {
        return typeof this.searchForm.data.site !== "undefined" ? this.searchForm.data.site.split(/\s*,\s*/) : [];
        //return this.searchForm.data.site.split(/\s*,\s*/); //split comma delimited string to array and trim values in one op
    },

    siteSelected: {
        get() {
            return this.currentSiteId;
        },

        set(value) {
            this.changeCurrentSiteId(parseInt(value));
        },
    },

    /**
     * 
     */
    /*funeralDirectorOptions() {
        function initials(str) { return str[0]; }
        return this.funeralDirectors.map((director) => ({
            value: director.id,
            label: (director.company_name? director.company_name + ": ":"") + (director.first_names?
                director.first_names.split(" ").map(initials).join(" "): "") || "[director title]",
        }));
    },*/
    funeralDirectorOptions() {
        function initials(str) { return str[0]; }
        return this.searchFormFuneralDirectors.map((director) => ({
            value: director.id,
            label: (director.company_name? director.company_name + ": ":"") + (director.first_names?
                director.first_names.split(" ").map(initials).join(" "): "") || "[director title]",
        }));
    },
};

const watch = {

    siteChoices(newValue, oldValue) { //watch for changes to selected sites and update funeral director options accordingly
        debugger; // eslint-disable-line no-debugger
        let difference = newValue.filter(x => !oldValue.includes(x)); //get the new site number by comparing arrays
        // eslint-disable-next-line no-console
        console.log("New Selected Site: " + difference);
        //this.changeCurrentSiteId(parseInt(difference));
        /*this.requestFuneralDirectors(parseInt(difference)).then(r => {
            // eslint-disable-next-line no-console
            console.log("Returned from Funeral Director Request." + r);
        }*/
        if(difference.length > 0){
            this.requestFuneralDirectorsBySite(parseInt(difference)).then(r => {
                // eslint-disable-next-line no-console
                console.log("Returned from Funeral Director Request." + r);
            }
            );
        }
    }
};


const methods = {
    ...mapMutations(["changeCurrentSiteId", "clearSearchFormFuneralDirectors"]),
    ...mapActions("booking", ["searchForEvents", "cleanSearchEvents"]),
    ...mapActions(["selectSite", "requestFuneralDirectors", "requestFuneralDirectorsBySite", "addNotification", "requestMeetingLocations", "requestMapSections"]),
    /**
     * 
     */
    onSearchEvents() {
        //debugger; // eslint-disable-line no-debugger
        this.$emit("setSiteSelectVisibility", {show: false});
        const searchEventsArguments = {
            filtersCriteria: this.searchForm.data
        };
        this.searchForEvents(searchEventsArguments);
    },

    /**
     * 
     */
    onCleanForm() {
        this.clearSearchFormFuneralDirectors();
        this.searchForm = createForm(searchFormSchema);
        this.cleanSearchEvents();
    },
    formatDate(dateString) {
        const date = new Date(dateString);
        // Then specify how you want your dates to be formatted
        return new Intl.DateTimeFormat("default", {dateStyle: "long"}).format(date);
    },
};

export default {
    name: "search-form",
    components,
    data,
    mounted,
    computed,
    watch,
    methods,
};
