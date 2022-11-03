import { mapGetters, mapActions, mapMutations, mapState } from "vuex";
import SiteSelectModal from "src/components/site-select-modal";

function data() {
    return {
        SiteSelectCurrentSiteId: this.$store.state.currentSiteId,   
        isVisible: true,   
        debug: false,  
    };
}



const methods = {
    ...mapActions([
        "getSitesForUser",
        "selectSite",
    ]),
    ...mapMutations([
        "changeCurrentSiteId",
        "addFuneralDirectors",
        "clearPrevSiteId",
       
    ]),
    removeSelection() {
        this.changeCurrentSiteId(null);
        this.addFuneralDirectors([]);
        this.clearPrevSiteId();
    },    

    handleSiteSelectVisibilityEvent: function(param) { 
        if(this.debug) console.log("Site Visibility Event Recorded in Site-Select. ");
        if(this.debug) debugger; // eslint-disable-line no-debugger
        //this.isVisible = false;        
    },
};

const components = {
    SiteSelectModal,
};


const computed = {
    ...mapGetters([
        "allowedSitesFromBereavementStaff",
        "currentSite",
        "currentSiteId",
    ]),
    ...mapState(["showSiteSelectConfirm"]),
};

const created = function() {
    this.getSitesForUser().then((result) => {
        if(this.debug) console.log("Site list finished loading.");     
        const SiteList = this.allowedSitesFromBereavementStaff;
        if (SiteList.length == 1){
            const siteID = SiteList[0].id;
            this.selectSite(siteID);
        }     
    })  
   
};

function mounted() {
    if(this.debug) console.log("Setting SiteSelect visible=false. ");    
    if(this.debug) debugger; // eslint-disable-line no-debugger
    //this.visible = false;
}

export default {
    name: "site-select",
    props: {'inline':Boolean},
    data,
    methods,
    computed,
    created,
    components,
    mounted,
};
