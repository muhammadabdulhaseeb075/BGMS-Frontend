import { Calendar } from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import listPlugin from '@fullcalendar/list';
import interactionPlugin from '@fullcalendar/interaction';
import { createPopper } from '@popperjs/core';
import { DateTime } from "luxon";
import { mapGetters, mapActions, mapMutations } from "vuex";

import ConfirmModal from "src/components/confirm-modal";
import SiteSelectModal from "src/components/site-select-modal";
import {BOOKING_ADD_NAME, CALENDAR_SLOT_DURATION} from "../../constants";

const CALENDAR_REF = "calendarref";
const TOOLTIP_REF = "tooltipref";

function data() {
    return {
        showTooltip: false,
        showRemoveConfirm: false,
        fCalendar: null,
        selectedEvent: null,
        dateRangeTitle: "",
        currentSiteName: "",     
        localSite: null,   
        localSiteId: null,
    }
}

async function mounted() {    
    const queries = this.$router.currentRoute?.value?.query || {};
    const { calendarDate } = queries;
    const calendarref = this.$refs[CALENDAR_REF];
    const tooltipref = this.$refs[TOOLTIP_REF];

    this.fCalendar = new Calendar(calendarref, {
        plugins: [dayGridPlugin, timeGridPlugin, listPlugin, interactionPlugin,],
        initialView: "timeGridWeek",
        slotMinTime: "08:00:00",
        slotMaxTime: "18:00:00",
        slotDuration: CALENDAR_SLOT_DURATION,
        allDaySlot: false,
        displayEventEnd: false,
        height: "auto",
        headerToolbar: {
            left: "",
            center: "",
            right: "",
        },
        events: [],
        dateClick: this.createCalendarEvent,
        dayHeaderContent: ({date}) => {
            const macroFormat = "EEE dd MMM";
            const labelDate = DateTime.fromJSDate(date).toFormat(macroFormat);
            return labelDate;
        },
        eventClick: (clickEvent) => {
            const { el, event, jsEvent } = clickEvent;

            jsEvent.stopPropagation();
            jsEvent.preventDefault();
            createPopper(el, tooltipref);

            if(!this.showTooltip) {
                const detectedClick = (globalEvent) => {
                    globalEvent.stopPropagation();
                    globalEvent.preventDefault();

                    const eventCalendarClicked = el.contains(globalEvent.target);
                    const tooltipClicked = tooltipref.contains(globalEvent.target);
                    const isClickInside = tooltipClicked || eventCalendarClicked;

                    if (!isClickInside) {
                        this.showTooltip = false;
                        this.selectedEvent = null;
                        document.removeEventListener("click", detectedClick);
                    }
                }
                document.addEventListener("click", detectedClick);
            }

            this.showTooltip = true;
            this.selectedEvent = { ...event.extendedProps, id: event.id };
        },
    });

    this.fCalendar.render();
    this.dateRangeTitle = this.fCalendar.view.title;
    if (calendarDate) {
        this.goToDateFromQuery(calendarDate);
    }
    /* This does not work when calling component dynamically when store.sites[] may not yet be set
    else if (this.currentSiteId || this.initialid > 0) {
        this.getCalendarEvents();
    }*/
}

const methods = {
    ...mapActions("booking", ["getEventsByDate", "removeEvent"]),
        
    editEvent() {
        const currentDateRange = this.fCalendar.getDate();
        const formatedDate = DateTime.fromJSDate(currentDateRange).toISODate();
        // send it to the new booking form to start editing
        const query = {
            eventId: this.selectedEvent.id,
            siteId: this.currentSiteId,
            calendarDate: formatedDate,
        };
        this.$router?.push({ name: BOOKING_ADD_NAME, query });
    },

    async deleteEvent() {
        await this.removeEvent(this.selectedEvent.id);
        this.updateRange();
    },

    nextRangeCalendar() {
        this.fCalendar.next();
        this.updateRange();
    },

    prevRangeCalendar() {
        this.fCalendar.prev();
        this.updateRange();
    },

    goTodayCalendar() {
        this.fCalendar.today();
        this.updateRange();
    },

    updateRange() {
        this.dateRangeTitle = this.fCalendar.view.title;
        this.getCalendarEvents();
        this.showTooltip = false;
    },

    createCalendarEvent(dateClickInfo) {
        const dateFromClick = DateTime.fromISO(dateClickInfo.dateStr);

        const query = {
            eventDate: dateFromClick
        };
        this.$router?.push({ name: BOOKING_ADD_NAME, query });
    },

    async getCalendarEvents() {
        //debugger; // eslint-disable-line no-debugger      
        const { activeStart, activeEnd } = this.fCalendar.view;

        this.fCalendar.removeAllEvents();

        let site_id = null;
        if(!(this.currentSiteId === "")){
            site_id = this.currentSiteId;
        }else if(this.initialid > 0){ //default id as prop is 0, will be something else is passed in.
            site_id = this.initialid; 
        }

        if(site_id != null) { //the site id has been set either dynamically or via prop
            const start = DateTime.fromJSDate(activeStart).toISODate();
            const end = DateTime.fromJSDate(activeEnd).toISODate();
            const events = await this.getEventsByDate({start, end, site_id});
            //const events = await this.getEventsBySiteAndRange(start, end, site_id);
            
            if(events.length) {
                events.forEach((event) => {
                    this.fCalendar.addEvent({
                        ...event,
                        title: event.details,
                        backgroundColor: event.status===7?'#CCCCCC':'#3788d8;',
                        borderColor: event.status === 7 ? '#CCCCCC' : '#3788d8;'
                    });
                });
            }
        }
    },

    goToDateFromQuery(calendarDate) {
        const jsDate = DateTime.fromISO(calendarDate).toJSDate();
        this.fCalendar.gotoDate(jsDate);
        this.updateRange();
    }

}

const computed = {
    ...mapGetters(["currentSiteId", "showSiteSelectConfirm", "getSitesFetchCompleted"]),
}

const watch = {      
    currentSiteId() {
        this.showTooltip = false;
        this.getCalendarEvents();
    },
    getSitesFetchCompleted() {
        console.log("Site fetch finished in calendar.");
        if(this.initialid > 0){ //assume global site has not been set
            this.localSiteId = this.initialid; 
            //this.localSite = getSiteById(this.localSiteId);
        }
        this.getCalendarEvents();
    },
}

const components = {
    ConfirmModal,
    SiteSelectModal,
}

export default {
    name: 'booking-calendar',
    props: {'initialid':0},
    data,
    mounted,
    methods,
    computed,
    watch,
    components,
};
