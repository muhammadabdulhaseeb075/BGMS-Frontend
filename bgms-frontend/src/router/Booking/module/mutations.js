
/**
 * 
 * @param {*} state 
 * @param {*} searchedEvents 
 */
export function addEventSerchResult(state, payload) {
    state.searchedEvents = payload["events"];
    state.totalRows = payload["total_rows"];
}

export function addEventSearchCriteria(state, eventSearchCriteria){
    state.searchCriteria = eventSearchCriteria;
}

export function addCurrentBooking(state, currentBooking){
    state.currentBooking = currentBooking;
}

export function cleanUpCurrentBooking(state) {
    state.currentBooking = null;
}
