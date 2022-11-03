import http from "src/services/http";
import store from "../../../store/index";

function getSiteDomain() {
    //debugger; // eslint-disable-line no-debugger      
    //console.log("Index: getSiteDomain called. ");
    const site = store.getters.currentSite;
    if (site) {
        return site.domain_url;
    } else {
        throw new Error("There is no site selected");
    }
}

/**
 * Get the domain for a site given the site id.
 * @param {*} site_id Id of the site
 * @returns 
 */
function getSiteDomainById(site_id) {
    //debugger; // eslint-disable-line no-debugger      
    //console.log("Index: getSiteDomainById called for Id=" + site_id + ".");
    //const site = store.getters.getSiteById(site_id);    
    const site = store.getters['getSiteById'](site_id)
    if (site) {
        return site.domain_url;
    } else {
        throw new Error("No valid site id was passed. Can't get domain.");
    }
}

/**
 * 
 * @param {*} eventPayload 
 */
export async function createEventBySite(eventPayload) {
    try {
        const siteDomain = getSiteDomain();
        const response = await http.post(
            `${siteDomain}/cemeteryadmin/funeralEvent/`,
            eventPayload
        );

        return response.data;

    } catch(error) {
        console.error("ERROR: ", error);

        throw error;
    }
    
}

export async function fetchSiteSettings(site_id, module_name="") {
    try {
        const siteDomain = getSiteDomainById(site_id);
        const response = await http.get(
            `${siteDomain}/cemeteryadmin/settings/${module_name}/`,
        );
        return response.data;
    } catch (error) {
        console.error("ERROR: ", error);
        throw error;
    }
}

export async function getEventBySite(eventId="") {
    try {
        const siteDomain = getSiteDomain();
        const response = await http.get(
            `${siteDomain}/cemeteryadmin/funeralEvent/${eventId}/`,
        );

        return response.data;
    } catch (error) {
        console.error("ERROR: ", error);

        throw error;
    }
}

/**
 * Gets events for site for a given date range.
 * @param {*} startDate Start date to get events for.
 * @param {*} endDate End date to get events for.
 * @param {*} site_id Id of the site to get events for.
 * @returns 
 */
export async function getEventsBySiteAndRange(startDate, endDate, site_id) {
    //debugger; // eslint-disable-line no-debugger      
    try {
        const siteDomain = getSiteDomainById(site_id);
        const response = await http.get(
            // i.e. cemeteryadmin/calendarEvents/2021-3-1/2021-05-31/
            `${siteDomain}/cemeteryadmin/calendarEvents/${startDate}/${endDate}/`,
        );

        return response.data;
    } catch(error) {
        console.error("Error: ", error);
        throw error;
    }
}

/* Original function that got events by current site not provided site id.
export async function getEventsBySiteAndRange(startDate, endDate) {
    debugger; // eslint-disable-line no-debugger      
    try {
        const siteDomain = getSiteDomain();
        const response = await http.get(
            // i.e. cemeteryadmin/calendarEvents/2021-3-1/2021-05-31/
            `${siteDomain}/cemeteryadmin/calendarEvents/${startDate}/${endDate}`,
        );

        return response.data;
    } catch(error) {
        console.error("Error: ", error);

        throw error;
    }
}*/

export async function patchEventBySite(eventId, eventPayload) {
    try {
        const siteDomain = getSiteDomain();
        const response = await http.patch(
            `${siteDomain}/cemeteryadmin/funeralEvent/${eventId}/`,
            eventPayload
        );

        return response.data;
    } catch (error) {
        console.error("ERROR: ", error);

        throw error;
    }
}
//+ "&llave2=" + preID
export async function patchPreburial(preburialId, datapre, postburialId, dataPost, cancelburialId, dataCancel) {
  try {
    
    const siteDomain = getSiteDomain();
    let data = {'predata' : datapre,
                'postdata': dataPost,
                'canceldata' : dataCancel };

    const response = await http.patch(
      //`${siteDomain}/cemeteryadmin/preburialCheck/?preburialid=${preburialId}&postburialid=${postburialId}&cancelburialid=${cancelburialId}`,
      `${siteDomain}/cemeteryadmin/preburialCheck/${preburialId}/${postburialId}/${cancelburialId}/`,
      data
    );

    return response.data;
  } catch (error) {
    console.error("ERROR: ", error);

    throw error;
  }
}

export async function patchPostburial(postburialId, data) {
  try {
    const siteDomain = getSiteDomain();
    const response = await http.patch(
      `${siteDomain}/cemeteryadmin/postburialCheck/${postburialId}/`,
      data
    );

    return response.data;
  } catch (error) {
    console.error("ERROR: ", error);

    throw error;
  }
}

export async function patchCancelburial(cancelburialId, data) {
  try {
    const siteDomain = getSiteDomain();
    const response = await http.patch(
      `${siteDomain}/cemeteryadmin/cancelburial/${cancelburialId}/`,
      data
    );

    return response.data;
  } catch (error) {
    console.error("ERROR: ", error);

    throw error;
  }
}

export async function createStatusBySite(eventPayload) {
  try {
    const siteDomain = getSiteDomain();
    const response = await http.post(
      `${siteDomain}/cemeteryadmin/preburialCheck/`,
      eventPayload
    );

    return response.data;

  } catch (error) {
    console.error("ERROR: ", error);

    throw error;
  }

}

/**
 * 
 * @param {*} eventPayload 
 */
export async function getFilterEvents(searchPayload, searchPaginationArguments) {
    //debugger; // eslint-disable-line no-debugger
    // @TODO do the actual call to the service to look for events here
    try {
        
        //Site list is a comma separated string. Convert to an array but leave original as is for repeat requests.
        var site_list = []; //if no site pass an empty array to search all sites
        if(searchPayload.site){ //check if a site has been selected
            site_list = searchPayload.site.split(",").map(function(item) {
                return item.trim();
            });
        }

        // clean site for the request without mutating the state. (Copies the payload with site: set to blank.)
        const searchPayloadCopy = {
            ...searchPayload,
            site: undefined
        }

        // building query parameters
        const searchQuery = {
            limit: searchPaginationArguments?.limit ?? 10,
            offset: searchPaginationArguments?.offset ?? 0,
            order_desc: true,
            order_by: "start_date",
            //site_ids: JSON.stringify(siteId ? [siteId] : []),
            site_ids: site_list ? site_list : [],
            filters: JSON.stringify(searchPayloadCopy),
        };

        /** 
         * @NOTE for development/local environment
         * If you make a request without sites data in your local
         * you will have respone errors because there is not data to relation for all sites
         * Make sure to select one site with data available in your local
         * 
         */
        const response = await http.post(
            "/cemeteryadminpublic/funeralEvents/",
            searchQuery,
        );

        return response.data;
    } catch (error) {
        console.error("ERROR: ", error);

        throw error;
    }
}

export async function cancelEventBySite(eventId) {
    try {
        const siteDomain = getSiteDomain();
        const response = await http.put(
            `${siteDomain}/cemeteryadmin/funeralEvent/${eventId}/cancel/`
        );

        return response.data;
    } catch (error) {
        console.error("ERROR: ", error);

        throw error;
    }
}

export async function createFuneralDirector(payload) {
    try {
        const site = store.getters.currentSite;

        if (site) {
            const response = await http.post(
                `${site.domain_url}/cemeteryadmin/funeralDirector/`,
                payload
            );

            return response.data;
        } else {
            throw new Error("There is no site selected");
        }

    } catch (error) {
        console.error("ERROR: ", error);

        throw error;
    }
}

/*Update an exiting Funeral Director via a PATCH request. */
export async function patchFuneralDirector(_, payload) {
    try {
        const site = store.getters.currentSite;
        if (site) {
            const response = await http.patch(
                `${site.domain_url}/cemeteryadmin/funeralDirector/${payload.update_id}/`,
                payload.data
            );
            return response.data;
        } else {
            throw new Error("There is no site selected");
        }
    } catch (error) {
        console.error("ERROR: ", error);
        throw error;
    }
}

export async function findAddressByPostcode(postcode) {
    /** @TODO Move this API KEY to another place  */
    /** considere move this endpoint to the backend and hide this API KEY */
    // i.e. https://api.ideal-postcodes.co.uk/v1/postcodes/PO167GZ?api_key=iddqd

    //var dummy_result = {"result":[{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 61","po_box":"","department_name":"","organisation_name":"","udprn":28255608,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1A","line_1":"Apartment 61","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 61, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504967","dataset":"paf","id":"paf_28255608","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 62","po_box":"","department_name":"","organisation_name":"","udprn":28255609,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1B","line_1":"Apartment 62","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 62, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504968","dataset":"paf","id":"paf_28255609","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 63","po_box":"","department_name":"","organisation_name":"","udprn":28255610,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1D","line_1":"Apartment 63","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 63, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504969","dataset":"paf","id":"paf_28255610","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 64","po_box":"","department_name":"","organisation_name":"","udprn":28255611,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1E","line_1":"Apartment 64","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 64, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504970","dataset":"paf","id":"paf_28255611","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 65","po_box":"","department_name":"","organisation_name":"","udprn":28255612,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1F","line_1":"Apartment 65","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 65, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504971","dataset":"paf","id":"paf_28255612","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 66","po_box":"","department_name":"","organisation_name":"","udprn":28255613,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1G","line_1":"Apartment 66","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 66, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504972","dataset":"paf","id":"paf_28255613","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 67","po_box":"","department_name":"","organisation_name":"","udprn":28255614,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1H","line_1":"Apartment 67","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 67, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504973","dataset":"paf","id":"paf_28255614","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 68","po_box":"","department_name":"","organisation_name":"","udprn":28255615,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1J","line_1":"Apartment 68","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 68, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504974","dataset":"paf","id":"paf_28255615","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 69","po_box":"","department_name":"","organisation_name":"","udprn":28255616,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1L","line_1":"Apartment 69","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 69, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504975","dataset":"paf","id":"paf_28255616","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 70","po_box":"","department_name":"","organisation_name":"","udprn":28255617,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1N","line_1":"Apartment 70","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 70, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504976","dataset":"paf","id":"paf_28255617","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 71","po_box":"","department_name":"","organisation_name":"","udprn":28255618,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1P","line_1":"Apartment 71","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 71, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504977","dataset":"paf","id":"paf_28255618","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 72","po_box":"","department_name":"","organisation_name":"","udprn":28255619,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1Q","line_1":"Apartment 72","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 72, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504978","dataset":"paf","id":"paf_28255619","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 73","po_box":"","department_name":"","organisation_name":"","udprn":28255620,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1R","line_1":"Apartment 73","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 73, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504979","dataset":"paf","id":"paf_28255620","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 74","po_box":"","department_name":"","organisation_name":"","udprn":28255621,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1S","line_1":"Apartment 74","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 74, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504980","dataset":"paf","id":"paf_28255621","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 75","po_box":"","department_name":"","organisation_name":"","udprn":28255622,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1T","line_1":"Apartment 75","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 75, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504981","dataset":"paf","id":"paf_28255622","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 76","po_box":"","department_name":"","organisation_name":"","udprn":28255623,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1U","line_1":"Apartment 76","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 76, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023512526","dataset":"paf","id":"paf_28255623","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 77","po_box":"","department_name":"","organisation_name":"","udprn":28255624,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1W","line_1":"Apartment 77","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 77, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10024264920","dataset":"paf","id":"paf_28255624","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 78","po_box":"","department_name":"","organisation_name":"","udprn":28255625,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1X","line_1":"Apartment 78","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 78, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504982","dataset":"paf","id":"paf_28255625","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 79","po_box":"","department_name":"","organisation_name":"","udprn":28255626,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1Y","line_1":"Apartment 79","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 79, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504983","dataset":"paf","id":"paf_28255626","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 80","po_box":"","department_name":"","organisation_name":"","udprn":28255627,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"1Z","line_1":"Apartment 80","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 80, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504984","dataset":"paf","id":"paf_28255627","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 81","po_box":"","department_name":"","organisation_name":"","udprn":28255628,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2A","line_1":"Apartment 81","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 81, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504985","dataset":"paf","id":"paf_28255628","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 82","po_box":"","department_name":"","organisation_name":"","udprn":28255629,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2B","line_1":"Apartment 82","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 82, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504986","dataset":"paf","id":"paf_28255629","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 83","po_box":"","department_name":"","organisation_name":"","udprn":28255630,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2D","line_1":"Apartment 83","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 83, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504987","dataset":"paf","id":"paf_28255630","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 84","po_box":"","department_name":"","organisation_name":"","udprn":28255631,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2E","line_1":"Apartment 84","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 84, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504988","dataset":"paf","id":"paf_28255631","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 85","po_box":"","department_name":"","organisation_name":"","udprn":28255632,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2F","line_1":"Apartment 85","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 85, Westside Two, 20","longitude":-1.9016023,"latitude":52.4763491,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504989","dataset":"paf","id":"paf_28255632","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 86","po_box":"","department_name":"","organisation_name":"","udprn":28255633,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2G","line_1":"Apartment 86","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 86, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504990","dataset":"paf","id":"paf_28255633","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 87","po_box":"","department_name":"","organisation_name":"","udprn":28255634,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2H","line_1":"Apartment 87","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 87, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504991","dataset":"paf","id":"paf_28255634","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 88","po_box":"","department_name":"","organisation_name":"","udprn":28255635,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2J","line_1":"Apartment 88","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 88, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023512527","dataset":"paf","id":"paf_28255635","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 89","po_box":"","department_name":"","organisation_name":"","udprn":28255636,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2L","line_1":"Apartment 89","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 89, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504992","dataset":"paf","id":"paf_28255636","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 90","po_box":"","department_name":"","organisation_name":"","udprn":28255637,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2N","line_1":"Apartment 90","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 90, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504993","dataset":"paf","id":"paf_28255637","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 91","po_box":"","department_name":"","organisation_name":"","udprn":28255638,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2P","line_1":"Apartment 91","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 91, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504994","dataset":"paf","id":"paf_28255638","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 92","po_box":"","department_name":"","organisation_name":"","udprn":28255639,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2Q","line_1":"Apartment 92","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 92, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504995","dataset":"paf","id":"paf_28255639","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 93","po_box":"","department_name":"","organisation_name":"","udprn":28255640,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2R","line_1":"Apartment 93","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 93, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504996","dataset":"paf","id":"paf_28255640","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 94","po_box":"","department_name":"","organisation_name":"","udprn":28255641,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2S","line_1":"Apartment 94","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 94, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504997","dataset":"paf","id":"paf_28255641","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 95","po_box":"","department_name":"","organisation_name":"","udprn":28255642,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2T","line_1":"Apartment 95","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 95, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504998","dataset":"paf","id":"paf_28255642","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 96","po_box":"","department_name":"","organisation_name":"","udprn":28255643,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2U","line_1":"Apartment 96","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 96, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023504999","dataset":"paf","id":"paf_28255643","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 97","po_box":"","department_name":"","organisation_name":"","udprn":28255644,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2W","line_1":"Apartment 97","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 97, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505000","dataset":"paf","id":"paf_28255644","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 98","po_box":"","department_name":"","organisation_name":"","udprn":28255645,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2X","line_1":"Apartment 98","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 98, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505001","dataset":"paf","id":"paf_28255645","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 99","po_box":"","department_name":"","organisation_name":"","udprn":28255646,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2Y","line_1":"Apartment 99","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 99, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505002","dataset":"paf","id":"paf_28255646","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 100","po_box":"","department_name":"","organisation_name":"","udprn":28255647,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"2Z","line_1":"Apartment 100","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 100, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505003","dataset":"paf","id":"paf_28255647","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 101","po_box":"","department_name":"","organisation_name":"","udprn":28255648,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3A","line_1":"Apartment 101","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 101, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505004","dataset":"paf","id":"paf_28255648","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 102","po_box":"","department_name":"","organisation_name":"","udprn":28255649,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3B","line_1":"Apartment 102","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 102, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505005","dataset":"paf","id":"paf_28255649","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 103","po_box":"","department_name":"","organisation_name":"","udprn":28255650,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3D","line_1":"Apartment 103","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 103, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505006","dataset":"paf","id":"paf_28255650","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 104","po_box":"","department_name":"","organisation_name":"","udprn":28255651,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3E","line_1":"Apartment 104","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 104, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505007","dataset":"paf","id":"paf_28255651","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 105","po_box":"","department_name":"","organisation_name":"","udprn":28255652,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3F","line_1":"Apartment 105","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 105, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505008","dataset":"paf","id":"paf_28255652","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 106","po_box":"","department_name":"","organisation_name":"","udprn":28255653,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3G","line_1":"Apartment 106","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 106, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505009","dataset":"paf","id":"paf_28255653","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 107","po_box":"","department_name":"","organisation_name":"","udprn":28255654,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3H","line_1":"Apartment 107","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 107, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505010","dataset":"paf","id":"paf_28255654","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 108","po_box":"","department_name":"","organisation_name":"","udprn":28255655,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3J","line_1":"Apartment 108","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 108, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505011","dataset":"paf","id":"paf_28255655","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 109","po_box":"","department_name":"","organisation_name":"","udprn":28255656,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3L","line_1":"Apartment 109","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 109, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505012","dataset":"paf","id":"paf_28255656","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 110","po_box":"","department_name":"","organisation_name":"","udprn":28255657,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3N","line_1":"Apartment 110","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 110, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505013","dataset":"paf","id":"paf_28255657","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 111","po_box":"","department_name":"","organisation_name":"","udprn":28255658,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3P","line_1":"Apartment 111","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 111, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505014","dataset":"paf","id":"paf_28255658","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 112","po_box":"","department_name":"","organisation_name":"","udprn":28255659,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3Q","line_1":"Apartment 112","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 112, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505015","dataset":"paf","id":"paf_28255659","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 113","po_box":"","department_name":"","organisation_name":"","udprn":28255660,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3R","line_1":"Apartment 113","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 113, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505016","dataset":"paf","id":"paf_28255660","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 114","po_box":"","department_name":"","organisation_name":"","udprn":28255661,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3S","line_1":"Apartment 114","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 114, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023512525","dataset":"paf","id":"paf_28255661","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 115","po_box":"","department_name":"","organisation_name":"","udprn":28255662,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3T","line_1":"Apartment 115","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 115, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505017","dataset":"paf","id":"paf_28255662","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 116","po_box":"","department_name":"","organisation_name":"","udprn":28255663,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3U","line_1":"Apartment 116","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 116, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505018","dataset":"paf","id":"paf_28255663","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 117","po_box":"","department_name":"","organisation_name":"","udprn":28255664,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3W","line_1":"Apartment 117","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 117, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505019","dataset":"paf","id":"paf_28255664","country_iso":"GBR"},{"postcode":"B1 1LY","postcode_inward":"1LY","postcode_outward":"B1","post_town":"BIRMINGHAM","dependant_locality":"","double_dependant_locality":"","thoroughfare":"Suffolk Street Queensway","dependant_thoroughfare":"","building_number":"20","building_name":"Westside Two","sub_building_name":"Apartment 118","po_box":"","department_name":"","organisation_name":"","udprn":28255665,"umprn":"","postcode_type":"S","su_organisation_indicator":"","delivery_point_suffix":"3X","line_1":"Apartment 118","line_2":"Westside Two","line_3":"20 Suffolk Street Queensway","premise":"Apartment 118, Westside Two, 20","longitude":-1.9016008,"latitude":52.4763464,"eastings":406780,"northings":286494,"country":"England","traditional_county":"Warwickshire","administrative_county":"","postal_county":"West Midlands","county":"West Midlands","district":"Birmingham","ward":"Ladywood","uprn":"10023505020","dataset":"paf","id":"paf_28255665","country_iso":"GBR"}],"code":2000,"message":"Success","limit":100,"page":0,"total":58};
    //return dummy_result?.result;

    try {
        const API_KEY = "ak_kn5f6vojZBfJZE9dSPl4LvwNjYtGc";
        const baseEndpoint = `https://api.ideal-postcodes.co.uk`;
        const endpointURL = `${baseEndpoint}/v1/postcodes/${postcode}`;
        //const endpointURL = `${baseEndpoint}/v1/postcodes/${"ID11QD"}`;
        //const endpointURL = process.env.NODE_ENV === 'development'
        //    ? `${baseEndpoint}/v1/postcodes/${"ID11QD"}`
            // for testing hardcode/use this postcode 'ID11QD'
            // in this way it doesn't consume account balance
            //: `${baseEndpoint}/v1/postcodes/${postcode}`;
        const response = await fetch(
            `${endpointURL}?api_key=${API_KEY}`,
            //`https://api.ideal-postcodes.co.uk/v1/postcodes/${postcode}?api_key=${API_KEY}`,
            // {
            //     cors: true,
            // }
        );
        var data;
        if (response.status <= 300){
            data = await response.json();
            return data?.result || [];
        }
        throw response;

    } catch (error) {
        console.error("ERROR: ", error);
        throw error;
    }
}
