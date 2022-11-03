/* eslint-disable no-console */
import _delay from "lodash/delay";
import _get from "lodash/get";
import _omitBy from "lodash/omitBy";
import _isNil from "lodash/isNil";
import _isEmpty from "lodash/isEmpty";
import _isUndefined from "lodash/isUndefined";
import _isObject from "lodash/isObject";
import _obj from "lodash/object";
import _merge from "lodash/merge";
import _set from "lodash/set";
import _isEqual from "lodash/isEqual";
import _cloneDeep from "lodash/cloneDeep";
import InputField from "src/components/fields/input-field";
import { urlQueries } from "src/services/http/helpers";
import { createForm, matchForm } from "src/utils/forms";
import {
    mapActions,
    mapGetters,
    mapMutations,
} from "vuex";

import {
    CALENDAR_FIELD,
    PERSON_RESIDENCE_FIELD
} from "./constants";
import eventFormSchema from "./new-event-form-schema";
import parsePayload from "./parse-payload";
import { unparseEventPayload as unparsePayload, unparseEventDate } from "./unparse-payload";
import FormModals from "../form-modals";
import NewBookingHeader from "../new-booking-header";
import AddressEventField from "../address-event-field";
import FormSection from "../../components/form-section";
import FormSectionField from "../../components/form-section-field";
import TimePicker from "../../../../components/time-picker";
import { BOOKING_STATUS_NAME, BOOKING_CALENDAR } from "../../constants";
import NotificationsList from "../../../../components/notifications-list";
import ConfirmModal from "src/components/confirm-modal";
import SiteSelectModal from "src/components/site-select-modal";
import PostSaveModal from "src/components/post-save-modal";
import { createNull } from "typescript";
import axios from "axios";
import bookingStore from "src/router/Booking/module";
import store from "src/store";

const FORM_CACHE_QUERY = "bookingForm";
const OPEN_SEARCH_GRAVE_QUERY = "openSearch";
const FILTER_PLOTS_QUERY = "filterAvailablePlots";
const SITE_SELECTED_QUERY = "siteId";
const ADMIN_DOMAIN = "adminDomain";
const EVENT_ID_QUERY = "eventId";
const CALENDAR_DATE = "calendarDate";
const EVENT_DATE_QUERY = "eventDate";
const FORM_SECTION_ZOOM = "zoomToMapSection";
const FORM_SECTION_ID = "section_id";
const FORM_SECTION_COORDS = "coords1";
const FORM_SECTION_COORDS2 = "coords2";

const components = {
    AddressEventField,
    NewBookingHeader,
    FormSection,
    FormSectionField,
    InputField,
    FormModals,
    TimePicker,
    NotificationsList,
    ConfirmModal,
    SiteSelectModal,
    PostSaveModal,
};

const bookingStatusChoices = [
    { value: 2, text: "Pre-Burial Checks" },
    { value: 3, text: "Awaiting-Burial" },
    { value: 4, text: "Post-Burial Checks" },
    { value: 5, text: "Completed" },
    { value: 7, text: "Cancelled" }
];

function data() {
    return {
        eventForm: createForm(eventFormSchema),
        modalForm: {
            name: "FuneralDirectorForm",
            namespaceFields: "",  
            data_id: "",          
            show: false,
        },
        postSaveData: {},
        editMode: true,
        reference: null,
        eventId: "",
        fromCalendar: false,
        showSaveConfirm: false,        
        showSiteSelectConfirm: false,
        showPostSaveModal: false,
        reference_number: null,
        incoming_type: null,
        incoming_site_id: null, //hack to allow site_id passed from calendar to be used?
        plotUUID: null,
        plotRelated: [],
        slotMinTime: "06:00:00",
        slotMaxTime: "19:00:00",
        debug: true,
    };
}

function mounted() {
    //debugger; // eslint-disable-line no-debugger
    if (this.debug) console.log("Event Form Mounted. ");

    this.checkComingFromCalendar(); //check if coming from calendar and set values from query

    this.populateForm();
    if (this.fromCalendar) { //hack to update incoming values after the dynamic form has been built
        //this.eventForm.type = this.incoming_type;
        this.eventForm.fields.type.value = this.incoming_type; //map to the form element not the data() value to force change
        this.eventForm.data.type = this.incoming_type;
    }

    if(this.plotUUID != null){
        this.getPlotRelated(this.plotUUID);
    }

    //TMN: Check id site_id is set and call time range
    if (this.incoming_site_id) this.setFormTimeRange(this.incoming_site_id).then(r => //this only works when coming from calendar, need to grab current site_id from vuex?
        console.log("Min/Max Time Set. Event Form Mounted. " + this.slotMinTime + " " + this.slotMaxTime)); //should probably force refresh of form if possible?
}

function beforeUnmount() {
    this.updateNewBooking(false);
    this.clearPrevSiteId();
    this.resetEventForm(); 
}

const methods = {
    postSaveData: {},
    ...mapActions(["selectSite", "requestFuneralDirectors", "addNotification", "requestMeetingLocations", "requestMapSections"]),
    ...mapActions("booking", ["createEvent", "getEvent", "updateEvent", "getSettings"]),
    ...mapMutations(["changeCurrentSiteId", "updateNewBooking", "clearPrevSiteId", "changePrevCurrentSiteId","addselectedMapSection"]),
    ...mapMutations("booking", ["cleanUpCurrentBooking"]),


    /**
     * 
     * @param {*} isFieldValid 
     * @param {*} errorType 
     * @param {*} fieldName 
     * @param {*} fieldId 
     */
    validEventForm(isValid, errorTypes, value, fieldSchema) {
        this.eventForm.validateField(fieldSchema.id, isValid);
    },
    /**
     * Gets the current Min/Max time from the calendar settings and sets the
     * slotMin/SlotMax variables for the time select components.
     * @param site_id
     * @returns {Promise<void>}
     */
    async setFormTimeRange(site_id) {

        let settings_fetched = [];
        try {
            settings_fetched = await this.getSettings({"site_id": parseInt(site_id), "module_name": "calendar"}); //use the same time settings as calendar
            if (this.debug) console.log("EVENT FORM SETTINGS: ");
            console.log(settings);
        } catch (error) {
            console.log("Error Getting Time Settings In Event Form. " + error);
        }

        if (settings_fetched.length) {
            var settings = settings_fetched[0].preferences; //point to payload for convenience
            if (this.debug) console.log(settings);
            try {
                this.slotMaxTime = settings.slotMaxTime;
                this.slotMinTime = settings.slotMinTime;
            } catch (error) {
                console.log("Error applying event form settings. " + error);
            }
        }
    },


    handlePostSaveModal: function() { //shows the post save modal
        //console.log("Handle Post Save Modal Called. ");
        this.showPostSaveModal = true; //show the modal ashes/burial select form
    },

    /**
     * 
     */
    async submitEventForm() {
        if(this.currentSite) {
            const eventPayload = parsePayload(
                this.eventForm.data,
                this.eventForm.fields,              
            );
            if(this.eventForm.data.burial.coffin_length === undefined && this.eventForm.data.burial.coffin_width === undefined &&
                this.eventForm.data.burial.coffin_height === undefined){

                this.eventForm.data.burial.coffin_units = undefined;
            }
            if(this.eventForm.data.person.age === undefined){
                this.eventForm.data.person.age_type = undefined;
            }   
            /*Validate required form fields. Should probably be broken out into method.*/         
            if (this.eventForm.data.type === undefined || (this.eventForm.data.person.first_names === undefined || this.eventForm.data.person.first_names === "") || (this.eventForm.data.person.last_name === undefined || this.eventForm.data.person.last_name === "")|| this.eventForm.data.funeral_director_id === undefined){
                if (this.eventForm.data.type === undefined){
                    this.addNotification({
                        type: "error",
                        message: "ERROR: Booking Type field is required."
                    }); 
                }
                if (this.eventForm.data.person.first_names === undefined || this.eventForm.data.person.first_names === ""){
                    this.addNotification({
                        type: "error",
                        message: "ERROR: Deceased First Name field is required."
                    }); 
                }
                if  (this.eventForm.data.person.last_name === undefined || this.eventForm.data.person.last_name === ""){
                    this.addNotification({
                        type: "error",
                        message: "ERROR: Deceased Last Name field is required."
                    }); 
                }            
                if  (this.eventForm.data.funeral_director_id === undefined){
                    this.addNotification({
                        type: "error",
                        message: "ERROR: Funeral Director field is required."
                    });     
                }            
            }
            else{
                if (this.isUpdatingEvent) {
                    try {
                        await this.updateEvent({ eventId: this.eventId, eventPayload });
                        this.showAlert();
                        this.editMode = false;
                        this.updateNewBooking(false);
                    }catch (error){
                        this.showAlert(error);
                    }

                } else {
                    let savedEvent = false;
                    try {
                        //debugger; // eslint-disable-line no-debugger
                        savedEvent = await this.createEvent(eventPayload);
                        this.showAlert();
                        this.reference = savedEvent?.calendar_event?.reference ?? null;
                        this.reference_number = savedEvent?.calendar_event?.reference_number ?? null;
                        this.eventId = savedEvent?.calendar_event?.id;
                        this.editMode = false;
                        this.updateNewBooking(false);

                        //assign values for the post save modal dialog, clunky but works.
                        this.postSaveData.site = this.currentSite.id;
                        this.postSaveData.reference = this.reference_number;
                        this.postSaveData.event = this.eventId;
                        this.postSaveData.date = savedEvent?.calendar_event?.start ?? null;

                        //show the post save modal with data set
                        this.handlePostSaveModal();
                    } catch (error) {
                        this.showAlert(error);
                    }
                }
            }
        }
    },

    /**
     * This method cleans up the form and any reference like if the user is creating a booking from scratch.
     */
    resetEventForm() {
        this.eventForm = createForm(eventFormSchema);
        this.reference = null;
        this.eventId = null;
        this.reference_number = null;
    },

    cleanFormData(object) {
        const eventFormCopyData = _cloneDeep(object);
        Object.keys(eventFormCopyData).forEach(key => {
            const objectValues = eventFormCopyData[key];
            if (_isObject(objectValues)) {
                Object.keys(objectValues).forEach(keyDeep => {
                    if (_isObject(objectValues[keyDeep])) {
                        eventFormCopyData[key][keyDeep] = _omitBy(eventFormCopyData[key][keyDeep], (v) => _isUndefined(v) || _isNil(v) || v === "" || _isEqual(v, {}));
                    }
                });
                eventFormCopyData[key] = _omitBy(eventFormCopyData[key], (v) => _isUndefined(v) || _isNil(v) || v === "" || _isEqual(v, {}));
            }
        });
        return _omitBy(eventFormCopyData, (v) => _isUndefined(v) || _isNil(v) || v === "" || _isEqual(v,{}));
    },

    /**
     * 
     * @param {*} modalName 
     */
    openFormModal(modalName, title, namespaceFields) {        
        this.modalForm.name = modalName;
        this.modalForm.title = title; 
        this.modalForm.namespaceFields = namespaceFields;
        this.modalForm.data_id = ""; //clear data_id in case it is still set from previous edit
        this.modalForm.show = true;
    },


    /**
     * Open a modal form for editing by passing data id.
     */
    openEditFormModal(modalName, title, data_id) {
        this.modalForm.name = modalName;
        this.modalForm.title = title;        
        this.modalForm.data_id = data_id; //the uid of the record to edit      
        this.modalForm.show = true;        
    },

    receiveModalForm(modalForm) {
        if(modalForm){ //this method is called twice the second time with an undefined form. 
            this.eventForm.fields.detailsFuneralDirector.value = modalForm.id;
            this.eventForm.data.funeral_director_id = modalForm.id;
        }
        switch (this.modalForm.name) {
        case "AddressForm":
        case "PostcodeForm":
            _merge(this.eventForm, modalForm);
            break;
        case "FuneralDirectorForm":
            break;
        }
    },

    openSaveConfirm() {
        this.showSaveConfirm = true;
    },
    /**
     * 
     */
    openSiteMapForGrave() {
        debugger; // eslint-disable-line no-debugger
        if(this.eventForm.fields.newBurialGrave.value !== undefined && this.eventForm.fields.newBurialGrave.value !== null) {
            const cachedForm = this.encodeFormCache();
            const queriesParams = {};
            
            queriesParams[ADMIN_DOMAIN] = encodeURIComponent(window.location.origin);
            queriesParams[SITE_SELECTED_QUERY] = this.currentSite?.id || "";
            queriesParams[FORM_CACHE_QUERY] = cachedForm;
            if (this.eventForm.fields.newBurialGrave.value === false) { //look for existing graves
                queriesParams[OPEN_SEARCH_GRAVE_QUERY] = true;
            } else { //look for open graves
                queriesParams[FILTER_PLOTS_QUERY] = true;
                //debugger; // eslint-disable-line no-debugger
                //const sectionItem = this.getSelectedMapCoords();
                //const coords = sectionItem.centrepoint.coordinates;
                //var count = 1;

                //queriesParams[FORM_SECTION_ZOOM] = true; //request map zoom

                //pass the section_id to the map to zoom to
                let section_id = this.eventForm.fields.detailsMapSection.value;
                if(section_id){
                    queriesParams[FORM_SECTION_ID] = section_id.toString();
                }

                //let section = this.getSectionById(parseInt(section_id));
                //debugger; // eslint-disable-line no-debugger
                //if(section){
                //    queriesParams[FORM_SECTION_ID] = section.id.toString();
                //}

                /*
                for(const ele of coords){
                    if(count == 1){
                        queriesParams[FORM_SECTION_COORDS] = ele.toString();
                        count = 2;
                    }
                    else if (count == 2){
                        queriesParams[FORM_SECTION_COORDS2] = ele.toString();
                    }
                    
                }*/
            }

            const baseURL = this.currentSite?.domain_url;
            if(baseURL) {           
                const encodeQueries = urlQueries(queriesParams);
                const siteMapURL = `${baseURL}/mapmanagement/#/?${encodeQueries}`;

                // Opening the mapmanagement
                // we are not using vue router because that other route
                // is handle by the server instead of vue router
                window.location.assign(siteMapURL);
            }
        } else {
            this.eventForm.fields.detailsGraveNumber.value = "";
        }
    },

    changeSelectedSection(){
        this.addselectedMapSection(this.eventForm.fields.detailsMapSection.value);
    },

    async populateForm() {
        const formCache = this.decodeFormCache();
        const queries = this.$router.currentRoute?.value?.query || {};
        const siteId = queries[SITE_SELECTED_QUERY];
        const eventDate = queries[EVENT_DATE_QUERY];
        const eventId = queries[EVENT_ID_QUERY];
        const curSiteId = this.currentSite?.id ?? "";

        if(eventId){
            this.updateNewBooking(false);
        }
        else{
            this.updateNewBooking(true);           
            this.changePrevCurrentSiteId(curSiteId);
        }

        if(!_isNil(formCache)) {
            Object.keys(formCache).forEach(fieldName => {
                //if(fieldName === "type"){
                //debugger; // eslint-disable-line no-debugger}}
                //}


                const field = this.eventForm.fields[fieldName] || {};
                const dataName = field.name;
                const validObj = this.eventForm.validFields[fieldName];
                const fieldValue = formCache[fieldName];
                field.value = fieldValue;

                if(dataName) {
                    _set(this.eventForm.data, dataName, fieldValue);
                }
                
                if (validObj && field.value) {
                    validObj.valid = true;
                }
            });
        }

        if(siteId) {
            this.changeCurrentSiteId(parseInt(siteId));
            // await this.selectSite(parseInt(siteId));
        }

        if(this.currentSite) {
            this.requestFuneralDirectors(siteId);
            this.requestMeetingLocations(siteId);
            this.requestMapSections(siteId);
            if(formCache.detailsBurialUUID) {
                this.plotUUID = formCache.detailsBurialUUID;
                this.plotRelated = [];
            }
            if(eventId) await this.addEventToForm(eventId);
        }

        if (eventDate) {
            const dataMatch = {
                [CALENDAR_FIELD]: {
                    start: eventDate
                }
            };
            const formSchemaWithEventDate =  unparseEventDate(eventFormSchema, dataMatch);
            const form = createForm(formSchemaWithEventDate);
            this.eventForm = form;
        }

        // adding addresses
        _set(this.eventForm.data, "person.residence_address", formCache.deceaseAddress);
        _set(this.eventForm.data, "person.other_address", formCache.otherAddress);
        
        _set(this.eventForm.data, "next_of_kin_person.address", formCache.kinAddress);
        if (formCache && formCache.eventId) {
            this.eventId = formCache.eventId;
            this.reference = formCache.reference;
            this.reference_number = formCache.reference_number;
        }
        //debugger; // eslint-disable-line no-debugger
        if (formCache && formCache.type) {
            _set(this.eventForm.data, "type", formCache.type);
            this.eventForm.fields.type.value = formCache.type; //map to the form element not the data() value to force change
            this.eventForm.data.type = formCache.type;
        }
    },

    async addEventToForm(eventId) {

        const eventData = await this.getEvent(eventId);

        if (eventData) {
            debugger; // eslint-disable-line no-debugger
            const unparsed = unparsePayload(eventFormSchema, eventData);
            const form = matchForm(unparsed, eventData);
            this.reference = eventData?.calendar_event?.reference ?? null;
            this.reference_number = eventData?.calendar_event?.reference_number ?? null;
            this.eventId = eventId;
            this.eventForm = form;
            this.editMode = false;
        }
    },

    /**
     * 
     */
    decodeFormCache() {
        /** */
        debugger; // eslint-disable-line no-debugger
        const queries = this.$router.currentRoute?.value?.query || {};
        const formCacheQuery = queries[FORM_CACHE_QUERY];
        let formCache = {};

        if (formCacheQuery) {
            formCache = JSON.parse(atob(formCacheQuery));

            if(formCache.eventId) {
                this.eventId = formCache.eventId;
            }
            if(formCache.detailsBurialUUID) {
                this.plotUUID = formCache.detailsBurialUUID;
                this.plotRelated = [];
            }
        }
        return formCache;        
    },

    /**
     * 
     */
    encodeFormCache() {
        //debugger; // eslint-disable-line no-debugger
        const { fields } = this.eventForm;
        const valueFields = Object.keys(fields)
            .reduce((acc, fieldName) => {
                const field = fields[fieldName];
                const fieldValue = field?.value;

                if(fieldValue !== "" && !_isEqual(fieldValue,{})){
                    acc[fieldName] = fieldValue;
                }

                return acc;
            }, {});
        //debugger; // eslint-disable-line no-debugger
        if(this.eventId) {
            valueFields["eventId"] = this.eventId;
            valueFields["reference"] = this.reference;
            valueFields["reference_number"] = this.reference_number;
        }

        // addresses are computed
        // keep them on fields either way
        valueFields["deceaseAddress"] = this.eventForm.data?.person?.residence_address;
        valueFields["otherAddress"] = this.eventForm.data?.person?.other_address;
        // valueFields["meetingLocation"] = this.eventForm.data?.meeting_location;
        valueFields["kinAddress"] = this.eventForm.data?.next_of_kin_person?.address;
        //debugger; // eslint-disable-line no-debugger
        const jsonForm = JSON.stringify(valueFields);
        const encode = btoa(jsonForm);

        return encode;
    },

    goToStatusPage(){
      
        if (this.eventId=== ""){
            this.openSaveConfirm();        
        }
        else{
            this.$router?.push({ name: BOOKING_STATUS_NAME });
        }
        
    },
  

    formatAddress(address) {
        return address
            ? Object.values(address)
                .filter(value => !!value)
                .join(", ")
            : "";
    },

    addAddressFor(propertyPath, addressData) {
        _set(this.eventForm.data, propertyPath, addressData);
    },
    
    removePlaceOfDeathAsAddressIfNotExists(){
        if (!this.eventForm.data?.person?.residence_address) {
            _set(this.eventForm.fields, "deceasePlaceOfDeath.value", false);
            if (this.eventForm.data?.person?.place_of_death) {
                _set(this.eventForm.data, "person.other_address", undefined);
                _set(this.eventForm.data, "person.place_of_death", false);
            }
        }
    },

    /**
     * 
     * @param {*} sectionName 
     * @returns 
     */
    filterFieldsSection(sectionName) {
        //debugger; // eslint-disable-line no-debugger
        const fields = Object.values(this.eventForm?.fields) || [];
        const filterFields = fields.find(({ section, value }) =>
            section === sectionName && value
        );

        return filterFields;
    },

    checkComingFromCalendar() {
        //debugger; // eslint-disable-line no-debugger  
        const queries = this.$router.currentRoute?.value?.query || {};
        //const calendarDate = queries[CALENDAR_DATE];
        const siteid_sent = queries["siteId"];
        const from_calendar = queries["fc"];
        if(from_calendar) {
            this.fromCalendar = true;
            this.incoming_type = queries["type"];
            this.incoming_site_id = siteid_sent;
        }
    },

    goToCalendarPostSave(site_id, event_date) {
        //const eventDate = this.eventForm.fields.date.value;
        const query = {
            siteId: site_id,
            calendarDate: event_date,
        };
        //this.$router?.push({ name: BOOKING_CALENDAR, query: query });
    },

    goToCalendar() {
        const eventDate = this.eventForm.fields.date.value;
        const query = {
            calendarDate: eventDate,
        };
        this.$router?.push({ name: BOOKING_CALENDAR, query });
    },

    resetCurrentGraveNumber(){
        this.eventForm.fields.detailsGraveNumber.value = "";
        this.eventForm.fields.newBurialGrave.value = undefined;
        this.eventForm.fields.detailsBurialUUID.value = "";
        this.plotUUID = null;
        this.plotRelated = [];

    },

    getStatusText(status) {

        if (status) {
            for (let itr = 0; itr < bookingStatusChoices.length;itr++){
                if (bookingStatusChoices[itr].value == status)
                    return bookingStatusChoices[itr].text;
            }      
        }
        return "";
    },

    showAlert(error=undefined) {
        if (typeof error === "undefined"){
            this.addNotification({
                type: "success",
                message: "The event was successfully saved."
            });
        }
        else{
            let error_message = "";
            if (error.response && error.response.data && error.response.data.detail)
                error_message = error.response.data.detail;
            else
                error_message = error.message;
            this.addNotification({
                type: "error",
                message: error_message
            });
        }
    },
    getPlotRelated(newValue){
        debugger; // eslint-disable-line no-debugger
        let current = store.getters.currentSite;
        let baseURL = current?.domain_url;

        console.log("BASE URL: " + baseURL);
        if (baseURL != null) {
            const plotRelatedURL = baseURL + "/mapmanagement/relatedBurials/?graveplot_uuid=" + newValue;
            axios.get(plotRelatedURL)
                .then(response => {
                    debugger; // eslint-disable-line no-debugger
                    this.plotRelated = response;
                })
                .catch(response => {
                    console.warn("Couldn't get data from server: " + response);
                });
        }
    }
};

const computed = {
    ...mapGetters(["currentSite", "funeralDirectors", "currentSiteId", "meetingLocations", "mapSections"]),
    ...mapGetters(["getSectionById"]),
    
    /**
     * Validate if of required fields have value
     * or validate if the user is editing one event created
     * 
     * @return {Boolean} - if the form is valid
     */
    isEventFormValid() {
        return !this.eventForm.fieldsToValidate.find(fieldName =>
            !this.eventForm.validFields[fieldName].valid
        ) || !!this.eventId;
    },

    /**
     * 
     */
    funeralDirectorOptions() {
        return this.funeralDirectors.map((director) => ({
            value: director.id,
            label: (director.company_name? director.company_name + ": ":"") + (director.first_names) + " " + (director.last_name)                    
        }));        
    },

    isUpdatingEvent() {
        return !!this.eventId;
    },

    fullDeceasedAddress() {
        return this.formatAddress(this.eventForm.data?.person?.residence_address);
    },

    fullDetailsAddress() {
        const location = this.eventForm.data?.meeting_location;
        let address;

        if(typeof location === "string") {
            address = location;
        } else if(typeof location === "object") {
            address = this.formatAddress(location);
        }

        return address;
    },

    fullKinAddress() {
        return this.formatAddress(this.eventForm.data?.next_of_kin_person?.address);
    },

    fullOtherAddress(){
        return this.formatAddress(this.eventForm.data?.person?.other_address);
    },

    isEmptyDetailsSection() {
        return !(this.filterFieldsSection("details") || this.eventForm.data?.burial?.location);
    },

    isEmptyKinSection() {
        //debugger; // eslint-disable-line no-debugger
        return !(this.filterFieldsSection("kin") || this.eventForm.data?.next_of_kin_person?.address);
    },

    isEmptyAuthSection() {
        //debugger; // eslint-disable-line no-debugger
        return !(this.filterFieldsSection("auth"));
    },

    isEmptyCommentsSection() {
        //debugger; // eslint-disable-line no-debugger
        return !(this.filterFieldsSection("comments"));
    },

    isAsAddressDisabled() {
        return !this.editMode || !this.fullDeceasedAddress;
    },

    disabledExistingGraveNumber(){
        return !this.editMode || (this.editMode && this.eventForm.fields.detailsGraveNumber.value !== "");
    },

    getbookingStatusChoices() {
        return this.getStatusText(this.eventForm.fields.status?.value);
    },
    meetingLocationOptions(){
        return this.meetingLocations.map((location) => ({
            value: location.id,
            label: location.location_address
        }));
    },
    mapSectionOptions(){
        return this.mapSections.map((section) => ({
            value: section.id,
            label: section.section_name
        }));
    },
    selectedMapCoords(){

    }

};

const watch = {
    currentSite(newValue, oldValue) {
        /** 
         * Refreshing or coming to this page with data(like redirect)
         * Load event and funeral dir. list after get all site list
         */
        if(oldValue === null && !this.funeralDirectors.length) {
            const queries = this.$router.currentRoute?.value?.query || {};
            const siteId = queries[SITE_SELECTED_QUERY];
            const eventId = queries[EVENT_ID_QUERY];
            if (siteId) this.requestFuneralDirectors(siteId);
            //if (siteId) this.setFormTimeRange(siteId).then(r => ); //get the min/max time from calendar
            if (eventId) this.addEventToForm(eventId);
        }
        //when currentSite changes always fetch the calendar time settings
        if (this.currentSiteId) this.setFormTimeRange(this.currentSiteId).then(r =>
            console.log("Min/Max Time Set. SiteId Watch Method." + this.slotMinTime + " " + this.slotMaxTime));

    },
    plotUUID(newValue, oldValue) {
        debugger; // eslint-disable-line no-debugger
        //if the plot_uuid changes then load any related burials
        this.getPlotRelated(newValue);
    },

};

export default {
    name: "new-event-form",
    data,
    computed,
    components,
    methods,
    mounted,
    beforeUnmount,
    watch,
};
