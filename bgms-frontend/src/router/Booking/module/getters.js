/**
 *
 */
import {DateTime} from "luxon";

export function searchResultEvent(state) {
    return state.searchedEvents;
}

export function searchEventCriteria(state) {
    return state.searchCriteria;
}

export function currentBooking(state){
    return state.currentBooking;
}

export function totalRows(state) {
    return state.totalRows;
}

//Methods for split-view pagination
export function totalViews(state) {
    return state.slideCount;
}
export function viewAddedEvent(state) {
    return state.slides;
}

export function statusFromCurrentBooking(state, getters){
    return {
        pre: getters.currentBooking?.preburial_check || null,
        post: getters.currentBooking?.postburial_check || null,
      cancel: getters.currentBooking?.cancelburial || null,
    };
}

export function currentBookingDate(state, getters){
    const currentBooking = getters.currentBooking;
    const createdDate = currentBooking?.calendar_event?.created_date;
    const dateTimeParsed = DateTime.fromISO(createdDate);
    return dateTimeParsed.isValid ? dateTimeParsed.toFormat("yyyy-MM-dd") : undefined;
}
