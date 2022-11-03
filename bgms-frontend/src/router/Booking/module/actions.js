import {
    createEventBySite,
    getEventBySite,
    getEventsBySiteAndRange,
    patchEventBySite,
    getFilterEvents,
    cancelEventBySite,
    createFuneralDirector,
    findAddressByPostcode,
    patchPreburial,
    patchPostburial,
    patchCancelburial,
    patchFuneralDirector,
    fetchSiteSettings, createStatusBySite,
} from "./../repository";


export async function getSettings(_, { site_id, module_name }) {
    //debugger; // eslint-disable-line no-debugger     
    const settings = await fetchSiteSettings(site_id, module_name);
    return settings;
}

/**
 * 
 * @param {*} context 
 * @param {*} eventData 
 */
export async function createEvent({ commit }, eventData) {
    try{
        const savedEvent = await createEventBySite(eventData);
        commit("addCurrentBooking", savedEvent);

        return savedEvent;
    }catch(error){
        throw error;
    }
}

/**
 * 
 * @param {*} _ 
 * @param {*} eventId 
 * @returns 
 */
export async function getEvent({ commit  }, eventId) {
    try{
        const event = await getEventBySite(eventId);
        commit("addCurrentBooking",event);

        return event;
    }
    catch (error) {
        throw error;
    }
}

/**
 * 
 * @param {*} _ 
 * @param {*} param1 
 * @returns 
 */
export async function getEventsByDate(_, { start, end, site_id }) {
    //debugger; // eslint-disable-line no-debugger     
    const events = await getEventsBySiteAndRange(start, end, site_id);
    return events;
}

/**
 * 
 * @param {*} _ 
 * @param {*} param1 
 * @returns 
 */
export async function updateEvent(_, {eventId, eventPayload}) {
    try {
        const updatedEvent = await patchEventBySite(eventId, eventPayload);
        return updatedEvent;
    }
    catch (error) {
        throw error;
    }

}

export async function updateStatus(_, { preburialId, dataPre, postburialId, dataPost, cancelburialId, dataCancel }) {
  const updatedStatus = await patchPreburial(preburialId, dataPre, postburialId, dataPost, cancelburialId, dataCancel);

  return updatedStatus;
}

export async function updatePostBurial(_, { postburialId, dataPost }) {
  const updatedPostBurial = await patchPostburial(postburialId, dataPost);

  return updatedPostBurial;
}

export async function updateCancelBurial(_, { cancelburialId, dataCancel }) {
  const updatedCancelBurial = await patchCancelburial(cancelburialId, dataCancel);

  return updatedCancelBurial;
}

/**
 * 
 */
export async function removeEvent(_, eventId) {
    const eventRef = await cancelEventBySite(eventId);

    return eventRef;
}

/**
 * 
 * @param {*} searchCriteria 
 */
export async function searchForEvents({ commit }, { filtersCriteria, searchPaginationArguments }) {
    const eventsSearched = await getFilterEvents(filtersCriteria, searchPaginationArguments);
    commit("addEventSerchResult", eventsSearched);
    commit("addEventSearchCriteria", filtersCriteria);

    return eventsSearched;
}

/**
 * 
 * @param {*} param0 
 */
export function cleanSearchEvents({ commit }) {
    commit("addEventSerchResult", []);
}

export async function createStatus(_, eventData) {
    const savedEvent = await createStatusBySite(eventData);
    return savedEvent;
}
/**
 * 
 * @param {*} param0 
 * @param {*} directorData 
 * @returns 
 */
export async function submitNewFuneralDirector(_, directorData) {    
    const newDirector = await createFuneralDirector(directorData);
    return newDirector;
}

/* Update an exiting Funeral Director. */
export async function updateFuneralDirector(_, payload) {
    try {
        const updatedDirector = await patchFuneralDirector(_, payload);
        return updatedDirector;
    }
    catch (error) {
        throw error;
    }
}

/**
 * 
 * @param {*} _ 
 * @param {*} postcode 
 * @returns 
 */
export async function findAddressPostcode(_, postcode) {
    try{
        const addresses = await findAddressByPostcode(postcode);
        return addresses;
    }catch (error) {
        throw error;
    }

}
