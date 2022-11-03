import { defineComponent } from 'vue'
import '@fullcalendar/core/vdom' // solve problem with Vite
import FullCalendar, { CalendarOptions, EventApi, DateSelectArg, EventClickArg } from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import listPlugin from '@fullcalendar/list'
import interactionPlugin from '@fullcalendar/interaction'

//import VueTailwind from 'vue-tailwind' //pagination component from the vue-tailwind library
//import TPagination from 'vue-tailwind/dist/components'

import { createPopper } from '@popperjs/core'; //pop-up library used when clicking on events

import { DateTime } from "luxon";
import ConfirmModal from 'src/components/confirm-modal';
import SiteSelectModal from 'src/components/site-select-modal';
import {BOOKING_ADD_NAME, BOOKING_STATUS_NAME, CALENDAR_SLOT_DURATION} from "../../constants";
//import { INITIAL_EVENTS, createEventId } from './event-utils.ts'
import { mapActions, mapGetters, mapMutations } from 'vuex'

const TOOLTIP_REF = "tooltipref";

function data() {
    return {
      backgroundColor: 'blue',
        backgroundCancel: "light-gray",
      borderColor: 'black',
        borderPre : 'red',
        borderPost : 'red',
        borderCancel : 'red',
        borderAwaiting : 'red',
        borderComplete : 'red',
      calendarOptions: {
          eventTimeFormat: { // like '14:30:00'
              hour: 'numeric',
              minute: '2-digit',
              meridiem: 'short',
          },
          dayHeaderFormat: { // will produce something like "Tuesday, September 18, 2018"
              weekday: 'short',
              month: 'short',
              day: 'numeric',
          },
          titleFormat: { // will produce something like "Tuesday, September 18, 2018"
              weekday: 'long',
              month: 'long',
              year: 'numeric',
          },
        plugins: [
          dayGridPlugin,
          timeGridPlugin,
          listPlugin,
          interactionPlugin // needed for dateClick
        ],
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,listWeek,timeGridDay'
        },
        initialView: 'timeGridWeek',
        initialEvents: [], // alternatively, use the `events` setting to fetch from a feed
        slotMinTime: "08:00:00",
        slotMaxTime: "18:00:00",
        slotDuration: CALENDAR_SLOT_DURATION,
        allDaySlot: false,
        displayEventEnd: false,
        height: "auto",
        editable: true,
        selectable: true,
        //selectMirror: true,
        dayMaxEvents: true,
        weekends: true,
        select: this.handleDateSelect,
        //selectAllow: this.handleSelectAllow,
        //eventClick: this.handleEventClick,
        //eventsSet: this.handleEvents,
        /* you can update a remote database when these fire:
        eventAdd:
        eventChange:
        eventRemove:
        */
        //dateClick: this.createCalendarEvent,
        eventClick: (clickEvent) => {
          //debugger; // eslint-disable-line no-debugger  
          const { el, event, jsEvent } = clickEvent;

          jsEvent.stopPropagation();
          jsEvent.preventDefault();
          createPopper(el, this.$refs[TOOLTIP_REF]);

          if(!this.showTooltip) {
              const detectedClick = (globalEvent) => {
                  let route = this.$router.currentRoute.value.name;
                  console.log("ROUTE: " + route);

                  //hack to prevent click handler from firing in other modules when routed to from calendar
                  if(route === "booking-split-view"){
                      globalEvent.stopPropagation();
                      globalEvent.preventDefault();

                      const eventCalendarClicked = el.contains(globalEvent.target);
                      const tooltipClicked = this.$refs[TOOLTIP_REF].contains(globalEvent.target);
                      const isClickInside = tooltipClicked || eventCalendarClicked;

                      if (!isClickInside) {
                          this.showTooltip = false;
                          this.selectedEvent = null;
                          document.removeEventListener("click", detectedClick);
                      }
                  }
              }
              document.addEventListener("click", detectedClick);
          }

          this.showTooltip = true;
          this.selectedEvent = { ...event.extendedProps, id: event.id };
        },
      }, //as CalendarOptions,
      currentEvents: [], //as EventApi[],
      siteName: "",
      siteId: "",
      currentSiteName: "", //global selected site  
      showTooltip: false,  
      selectedEvent: null,
      debug: false,
      neo_debug: true,
      settings_debug: "",
    }
}

async function mounted() {
  var site_id = this.guessInitialSiteId();
  if(this.debug) console.log("Initial Calendar Site: " + site_id)
  this.getCalendarEvents(parseInt(site_id));
  this.setSiteSettings(parseInt(site_id));
}

const methods = {
  ...mapActions("booking", ["getEventsByDate", "getEvent", "removeEvent", "getSettings", "getSitesForUser"]),
  ...mapGetters(["getSiteById", "getSitesFetchCompleted"]), 
  ...mapMutations([
    "changeCurrentSiteId",       
  ]), 

  changeWindowIdIndex(new_id){
    this.windowIdIndex = new_id;
  },

  changeLocalSite(new_id){
    //debugger; // eslint-disable-line no-debugger
    if(new_id){ //new_id is undefined on intial load
      if(this.debug) console.log("Local Site Changed (ag-c). site_id=" + new_id);
      this.siteId = parseInt(new_id); //make sure value passed is a number not string    
      this.getCalendarEvents(this.siteId);
      this.setSiteSettings(this.site_id);
    }
  },

  guessInitialSiteId(){ //sets the current siteId based on passed in value or first site in list
    let site_id = 0;
    if(!(this.siteId === "")){ //is it already set?
        site_id = parseInt(this.siteId);
        if(this.debug) console.log("Using Local SiteId: " + site_id);        
    }else if(this.initialid > 0){ //default id as prop is 0, will be something else is passed in.
        site_id = parseInt(this.initialid); 
        this.siteId = site_id;
        if(this.debug) console.log("Using Initial/Prop SiteId: " + site_id);
    }else{ //default to the first site in the user list
      var sites = this.getSiteList;                
      if(sites != null && sites.length > 0){                                             
        return parseInt(sites[0].id); //add calendar for first site in user site list
      } 
    }
    return site_id;
  },

  async configureCalendarForSite(site_id) { //do we need a way to reconfigure or just destroy/create
    return true;
  },

  async setSiteSettings(site_id) {
    //debugger; // eslint-disable-line no-debugger
    let calendarApi = this.$refs.ag_calendar.getApi();
    
    if(site_id != null){ this.siteId = site_id; } //set the id for the calendar

    if(site_id != null) { //the site id has been set either dynamically or via prop
        if(this.debug) debugger; // eslint-disable-line no-debugger
        let settings_fetched = [];
        try{
          settings_fetched = await this.getSettings({"site_id":parseInt(site_id), "module_name":"calendar"});
          if(this.debug) console.log("SETTINGS: "); console.log(settings_fetched);
        }catch(error) {console.log("Error Getting Settings. " + error);}        
        
        if(settings_fetched.length) {          
          //debugger; // eslint-disable-line no-debugger
          this.settings_debug = settings_fetched;
          var settings = settings_fetched[0].preferences; //point to payload for convenience
          if(this.debug) console.log(settings);
          try{
            this.backgroundColor = settings["backgroundColor.default"];
            this.borderColor = settings["borderColor.default"];
            //Set custom status colors. Applied in the getCalendarEvents method
            this.backgroundCancel = settings["backgroundColor.cancel"];
            this.borderPre = settings["borderColor.pre"];
            this.borderPost = settings["borderColor.post"];
            this.borderCancel = settings["borderColor.cancel"];
            this.borderAwaiting = settings["borderColor.awaiting"];
            this.borderComplete = settings["borderColor.complete"];
            this.borderCancel = settings["borderColor.cancel"];
            this.calendarOptions.slotMaxTime = settings.slotMaxTime;
            this.calendarOptions.slotMinTime = settings.slotMinTime;
            calendarApi.setOption("slotMaxTime", settings.slotMaxTime);
            calendarApi.setOption("slotMinTime", settings.slotMinTime);
          }catch(error){
            console.log("Error applying calendar settings. " + error);
          }
        }
    }else{
      //calendarApi. //touch the calendar to force resize?
    }
    
  },

  async getCalendarEvents(site_id) {
    if(this.debug) debugger; // eslint-disable-line no-debugger
    let calendarApi = this.$refs.ag_calendar.getApi();
    const { activeStart, activeEnd } = calendarApi.view;
    calendarApi.removeAllEvents(); //

    if(site_id != null){ this.siteId = site_id; } //set the id for the calendar
    
    try{
      //debugger; // eslint-disable-line no-debugger     
      let local_site = this.$store.getters['getSiteById'](site_id);
      if(local_site != null){
        this.siteName = local_site.name;
        //TODO: Set additional site params here.
      }
    } catch(error) {
      console.log("Error getting site.", error);
    }

    if(site_id != null) { //the site id has been set either dynamically or via prop
        //debugger; // eslint-disable-line no-debugger     

        //TODO: Handle calendar range changes? //Hack to set end date six months ahead
        activeStart.setMonth((activeStart.getMonth() - 2));
        let start = DateTime.fromJSDate(activeStart).toISODate();
        activeEnd.setMonth(activeEnd.getMonth() + 6);
        let end = DateTime.fromJSDate(activeEnd).toISODate();

        let events = [];
        try{
          events = await this.getEventsByDate({start, end, site_id});
          if(this.debug) console.log("EVENTS (length): " + events.length);
        }catch(error) {console.log("Error Getting Events. " + error);}        
        
        if(events.length) {
            this.currentEvents = events;
          //this.handleEvents(events); //this should work but doesn't
          events.forEach((event) => {
              let back_color = this.backgroundColor;
              let bord_color = this.borderColor;
              if(event.status == 2){
                  bord_color = this.borderPre;
              }else if(event.status == 3){
                  bord_color = this.borderAwait;
              }else if(event.status == 4){
                  bord_color = this.borderPost;
              }else if(event.status == 5){
                  bord_color = this.borderCompleted;
              }else if(event.status == 7){
                  bord_color = this.borderCancel;
                  back_color = this.backgroundCancel;
              }
              //add events using styling from above
              calendarApi.addEvent({
                  ...event,
                  title: event.details,
                  //status: event.status,
                  backgroundColor: back_color,
                  borderColor: bord_color,
                  //backgroundColor: event.status===7 ?'#CCCCCC':'#3788d8;',
                  //borderColor: event.status === 7 ? '#CCCCCC' : '#3788d8;'
              });
          }); 
        }
    }else{
      //calendarApi. //touch the calendar to force resize?
    }
    
  },

  goToDateFromQuery(calendarDate) {
      const jsDate = DateTime.fromISO(calendarDate).toJSDate();
      this.fCalendar.gotoDate(jsDate);
      this.updateRange();
  },

  handleWeekendsToggle() {
      this.calendarOptions.weekends = !this.calendarOptions.weekends; // update a property
  },
  /*  handleSelectAllow(selectInfo) {
        if(!selectInfo) return; //this method is called on component load with click event

        debugger; // eslint-disable-line no-debugger
        const dateFromClick = DateTime.fromISO(selectInfo.startStr);

        var todaysDay = new Date().getDate();
        if (dateFromClick.day < todaysDay) { //check if date of click is before today and return if so.
            //selectInfo.jsEvent.stopPropagation(); //stop click from triggering default event creation?
            //selectInfo.jsEvent.preventDefault();
            return false;
        }else{
            return true;
        }
    },*/
  handleDateSelect(selectInfo) {
    if(!selectInfo) return; //this method is called on component load with click event
    
    //debugger; // eslint-disable-line no-debugger
    const dateFromClick = DateTime.fromISO(selectInfo.startStr);

    var todaysDay = new Date().getDate();
    var todaysMonth = new Date().getMonth();
    var todaysYear = new Date().getFullYear();
    if (dateFromClick.day < todaysDay && (dateFromClick.month <= (todaysMonth + 1) && dateFromClick.year == todaysYear || dateFromClick.year < todaysYear)) { //check if date of click is before today and return if so.
        selectInfo.jsEvent.stopPropagation(); //stop click from triggering default event creation?
        selectInfo.jsEvent.preventDefault();
        return;
    }

    const site_id = this.siteId;
    console.log("Site: " + site_id + " New Event Date: " + dateFromClick);
        
    this.changeCurrentSiteId(site_id); //Booking form still uses vuex currentSiteId?    
        
    var query = {
      eventDate: dateFromClick,      
      siteId: site_id,
      fc: true
    };
    
    //Pass event to parent and display modal there for alignment reasons.
    this.$emit('ashesModalFromChild', {query: query});

    //this.$refs.AshesModal.reset(); //clear the initial value?        
    //this.showAshesModal = true; //show the modal ashes/burial select form
 
  },
  editEvent() {
    //debugger; // eslint-disable-line no-debugger
    const site_id = this.siteId;
    this.changeCurrentSiteId(site_id); //Booking form still uses vuex currentSiteId?
    var event_id = null;
              
    if(this.selectedEvent && this.selectedEvent.id){      
      event_id = this.selectedEvent.id;
      console.log("EVENT ID: " + event_id);
      const query = {
        eventId: event_id,
        siteId: site_id,
        fc: true
      };
      this.$router?.push({ name: BOOKING_ADD_NAME, query });
    }
  },
    async editStatus() {
        //debugger; // eslint-disable-line no-debugger
        const site_id = this.siteId;
        this.changeCurrentSiteId(site_id); //Booking form still uses vuex currentSiteId?
        var event_id = null;

        if(this.selectedEvent && this.selectedEvent.id){
            event_id = this.selectedEvent.id;
            console.log("EVENT ID: " + event_id);
            const eventData = await this.getEvent(event_id); //getEvent also maps the fetched event to the current booking in vuex
            const query_local = {
                eventId: event_id,
                siteId: site_id,
            };
            this.$router?.push({ name: BOOKING_STATUS_NAME, query: query_local });
            //this.$router?.push({ name: BOOKING_ADD_NAME, query });
        }
    },

  handleEventClick(clickInfo) {
      if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
        clickInfo.event.remove()
      }
  },
}

const computed = {
    ...mapGetters(["currentSiteId", "showSiteSelectConfirm", "getSitesFetchCompleted", "getSiteList"]),
    showCloseButton() { //return true if there is more than one calendar
      return true;
      /*if(this.$parent.slideCount > 1){ //doesn't seem to update?
        return true;
      } else {return false;}*/
    },
    /*
    parentSiteChange: function(){      
        return this.$parent.siteChanged;
    },*/
}

const watch = {
    getSitesFetchCompleted() {
      //debugger; // eslint-disable-line no-debugger   
      if(this.debug) console.log("Site fetch finished in geomatics-calendar."); 
      var site_id = this.guessInitialSiteId();     
      this.getCalendarEvents(site_id);
      var settings = this.getSettings(site_id, "calendar");
      if(this.debug) console.log(settings);
    },
    /*
    parentSiteChange: {
      handler: function () {
          console.log("Parent SiteId Change In Child.");
          debugger; // eslint-disable-line no-debugger  
          var parentSiteId = this.$parent.slides[this.windowIdIndex].siteId;
          if(parentSiteId && parentSiteId != this.siteId){
            this.changeLocalSite(parentSiteId);
          }          
      },      
  },*/
}

const components = {
    FullCalendar,
    ConfirmModal,
    SiteSelectModal,    
}

export default {//Demo
    name: 'geomatics-calendar',
    props: {'initialid':0, 'windowIdIndex':0},
    data,
    mounted,
    methods,
    computed,
    watch,
    components,
};
