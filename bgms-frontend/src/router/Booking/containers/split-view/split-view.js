/* eslint-disable no-console */
import {mapActions, mapGetters} from "vuex";
//import {BOOKING_CALENDAR, BOOKING_SPLIT_VIEW} from "../../constants";
import { VueAgile } from "vue-agile"; //slide component
import GeomaticsCalendar from "/src/router/Booking/containers/ag-calendar";
import CalendarPagination from "/src/router/Booking/containers/calendar-pagination";
import AshesModal from "src/components/ashes-modal";
const { DateTime } = require("luxon");


function data() {
    return {
        slides:[],
        slideCount:0,
        slideCurrent:0,
        renderRequired:false,
        slideOptions: { //slide options
            slidesToShow: 1,
            infinite: false, //infinite scroll causes issues when loaded with one slide
            navButtons: false, //initially only one slide so nav not needed
            dots: false, //pagination dots (check vue-agile samples for styling?)
        },  
        siteChanged: false, 
        showAshesModal: false,
        ashesQuery: "",
        ashesDate: "",
        debug: false,
    };
}

async function mounted() {
    //debugger; // eslint-disable-line no-debugger
    if(this.getSitesFetchCompleted){
        if(this.debug) console.log("Sites already loaded initializing initial SplitView Calendar.");
        var sites = this.getSiteList;
        //check if there are parameters set in the url
        const queries = this.$router.currentRoute?.value?.query || {};
        const siteid_sent = queries["siteId"];
        if(sites != null && sites.length > 0){
            if(siteid_sent != ""){
                this.addNewCalendarById(parseInt(siteid_sent));
            }else{
                this.addNewCalendarById(sites[0].id);
            }
        }        
    }           
}

const methods = {
    ...mapActions(["getSitesForUser"]),
    //...mapActions("booking", ["getEventsByDate", "removeEvent"]),
    //...mapGetters("getSiteList"),
    
    handleCloseEvent: function(windowId) {        
        this.removeSlideByIndex(windowId);        
    },

    handleSiteChangeEvent: function(param) {  //this is called when a child calendar changes sites, not really necessary?
        if(this.debug) console.log("Site Change Recorded in Parent. ");
        //debugger; // eslint-disable-line no-debugger             
        if(this.slides[param.index]){
            this.slides[param.index].siteId = param.new; //change the siteId, calendar should be watching and update accordingly
        }
        //siteChanged = true;
        this.replaceSlideByIndex(param.index, param.new);            
    },

    handleAshesModal: function(param) {
        if(this.debug) console.log("Ashes Modal Recorded in Parent. ");
        //debugger; // eslint-disable-line no-debugger
        var query = param.query;
        this.ashesQuery = query;
        let date = query.eventDate;
        let date_string = date.toLocaleString(DateTime.DATETIME_MED)
        this.ashesDate = date_string;

        this.$refs.AshesModal.reset(); //clear the initial value?        
        this.showAshesModal = true; //show the modal ashes/burial select form
    },

    /** Returns best guess of current site ID. If ID is not set then it uses first id in user site list. */
    guessInitialSiteId(){ //sets the current siteId based on passed in value or first site in list
        //debugger; // eslint-disable-line no-debugger
        let site_id = 0;
        //get variables passed in url
        const queries = this.$router.currentRoute?.value?.query || {};
        const siteid_sent = queries["siteId"];
        if(!(this.siteId === "") && this.siteId != null){ //is it already set?
            site_id = this.siteId;
            if(this.debug) console.log("Using Local SiteId: " + site_id);        
        }
        else if(siteid_sent){
            site_id = siteid_sent;
        }
        else{ //default to the first site in the user list
            var sites = this.getSiteList;                
            if(sites != null && sites.length > 0){                                             
                site_id = sites[0].id; 
            } 
        }
        return parseInt(site_id);
    },

    addNewCalendar(){ //add a new default calendar from button click
        //debugger; // eslint-disable-line no-debugger
        if(this.debug) console.log("Add Calendar in Parent. ");
        var slideCount = this.slideCount;        
        this.addNewSlide({id: slideCount, siteId: this.guessInitialSiteId(), windowIdIndex: slideCount}); //TODO: Guess next site?
        this.current_slide = this.slideCount - 1; 
    },

    addNewCalendarById(site_id){ //add a new default calendar by site_id
        //debugger; // eslint-disable-line no-debugger
        var slideCount = this.slideCount;        
        this.addNewSlide({id: slideCount, siteId: site_id, windowIdIndex: slideCount});
        this.current_slide = this.slideCount - 1; 
    },

    /**
     * Adds a new slide to the end of the deck and triggers a render.
     * @param {*} slide Object with values needed to init slide contents {id:, siteId:, windowIdIndex:} 
     */
    addNewSlide(slide){ //add a new slide to the end of the list        
        if(this.debug) console.log("addNewSlide in Parent. ");
        //let current_slide = this.$refs.ag_canvas.getCurrentSlide(); //note visible position in deck
        this.slides.push(slide);        
        this.slideCount++;
        if(this.slideCount > 1){
            this.slideOptions.slidesToShow = 2;
        }
        if(this.slideCount > 2){
            this.slideOptions.navButtons = false;
            this.slideOptions.dots = false;
        }        
        this.triggerRender();
        //console.log("SLIDE To: " + slideCount + 1);
        //this.$refs.ag_canvas.goToSlideIndex(slideCount + 1);               
        /*if(current_slide % 2){
            this.$refs.ag_canvas.goTo(current_slide + 1);               
        }else{
            this.$refs.ag_canvas.goTo(current_slide + 2);
        }*/
        //this.$refs.ag_canvas.goTo(current_slide + 1); //return to the visible slide after render
        //this.$refs.ag_canvas.reload; //force a reload of the split-view container 
    },

    /** 
     * Removes the slide/window at the current index and replaces it with a new slide from site_id. 
     * This forces a full re-render when the site_id changes so initial settings apply.
    */
    replaceSlideByIndex(index, site_id){ //removes a slide at index and adds a new slide at the same position        
        //let current_slide = this.$refs.ag_canvas.getCurrentSlide(); //note visible position in deck
        delete this.slides[index]; //delete removes the item but leaves an undefined/empty object in it's place       
        this.slides[index] = {id: index, siteId: site_id, windowIdIndex: index};                           
        //Trigger a reload/render of the slide deck    
        this.triggerRender();
        //this.$refs.ag_canvas.goToSlideIndex(current_slide);                   
        /*if(current_slide % 2){
            this.$refs.ag_canvas.goTo(current_slide);               
        }else{
            this.$refs.ag_canvas.goTo(current_slide + 1);
        }*/
    },

    removeSlideByIndex(index){
        //let current_slide = this.$refs.ag_canvas.getCurrentSlide(); //note visible position in deck
        this.slides.splice(index, 1); //splice removes the item and resizes the array
        //reindex the components
        for (var count = 0; count < this.slides.length; count++) {
            this.slides[count].windowIdIndex = count;
        }
        this.slideCount--;
        if(this.slideCount < 2){
            this.slideOptions.slidesToShow = 1;
        }
        if(this.slideCount < 3){
            this.slideOptions.navButtons = false;
            this.slideOptions.dots = false;
        }
        this.triggerRender();
        /*if(current_slide > 0){
            this.$refs.ag_canvas.goToSlideIndex(current_slide - 1);               
        }else{
            this.$refs.ag_canvas.goToSlideIndex(0);               
        }*/
    },

    removeLastSlide(){ //removes the last slide added
        this.slides.shift();
        this.slideCount--;
    },


    /**
     * Wrapper methods to navigate through slides from child component.
     */
    goToSlideIndex(slide){ //go to specific slide.
        this.$refs.ag_canvas.goTo(slide);               
    },
    goToNextSlide(){ //go to next slide                                       
        this.$refs.ag_canvas.goToNext();               
    },
    goToPreviousSlide(){ //go to previous slide
        this.$refs.ag_canvas.goToPrev();               
    },

    /**
     * Toggles the renderRequired Boolean to trigger a render. 
     * Value of renderRequired doesn't matter so long as it changes to trigger rebuild.
     */
    triggerRender(){ 
        this.renderRequired = this.renderRequired ? false : true;
    }
};

const computed = {
    ...mapGetters(["currentSiteId", "currentSiteName", "getSitesFetchCompleted", "getSiteList"]),
};

const watch = {
    getSitesFetchCompleted() {
        //debugger; // eslint-disable-line no-debugger
        if(this.debug) console.log("Site fetch finished event in split-view component.");
        this.addNewCalendarById(this.guessInitialSiteId());
    },
    /* //now ignoring the global site id
    currentSiteId() {
        this.getCalendarEvents();
    }*/
};
const components = {
    GeomaticsCalendar,  
    CalendarPagination,  
    AshesModal,
    agile: VueAgile,
};

export default {
    name: "split-view",
    props: {"siteChanged":false},
    data,
    mounted,
    methods,
    computed,
    watch,
    components,
};
