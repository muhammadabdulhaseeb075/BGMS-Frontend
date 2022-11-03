/**
 * @module eventService
 *
 * @description
 * A model-service used to register all the events that we want the map to listen for. Supports all openlayers events:
 * 'click', 'singleclick', 'dblclick', 'pointerdrag', 'pointermove', 'postrender' and 'moveend'
 */
angular.module('bgmsApp.map').service('eventService', [function(){

	/**
	 * @function
	 * @description
	 * Method to obtain a reference to event store.
	 * @returns {Array<MapEvent>} Entire event store
	 */
	this.getEvents = function(){
		return window.MapEvents;
	};

	/**
	 * @function
	 * @description Function returning an array of index positions of the events matching the key:value pair.
	 * @param {string} key - any MapEvent property name
	 * @param {string} value - the value to search for
	 * @returns {Array<number>} Array of indices of the events matching the key:value pair
	 */
	this.getEventPositionInStack = function(key, value){
 		var positions = [-1];
		console.log(this.getEvents());
		var i = 0;
		angular.forEach(this.getEvents(), function(event, index) {
				if(event[key] === value){
						positions[i++] = index;
				}
		});
		return positions;
	};

	/**
	 * @function
	 * @description Function to register an event
	 * @param {MapEvent} event
	 * @returns undefined
	 */
	this.pushEvent = function(eventObj){
		jQuery(document).trigger('pushEvent', eventObj);
	};

	/**
	 * @function
	 * @description Function to de-register an event by its name
	 * @param {string} event name
	 * @returns {MapEvent|undefined} the event if found, otherwise returns undefined
	 *
	 */
	this.removeEventByName = function(eventName){
		let events = this.getEventsByName(eventName);
		jQuery(document).trigger('removeEventByName', eventName);
		return events;
	};

	/**
	 * @function
	 * @description Function to de-register all events belonging to a group
	 * @param {string} eventGroup
	 * @returns {Array<MapEvent>|undefined} the events if found, otherwise returns undefined
	 */
	this.removeEventsByGroup = function(eventGroup){
		let events = this.getEventsByGroup(eventGroup);
		jQuery(document).trigger('removeEventsByGroup', eventGroup);
		return events;
	};

	/**
	 * @function
	 * @description Function to de-register all events belonging to a group that are of a certain type
	 * @param {string} eventGroup
	 * @param {string} eventType
	 * @returns {Array<MapEvent>|undefined} the events if found, otherwise returns undefined
	 */
	this.removeEventsByGroupAndType = function(eventGroup, eventType){
		const events = this.getEventsByGroupAndType({ eventGroup: eventGroup, eventType: eventType });
		jQuery(document).trigger('removeEventsByGroupAndType', { eventGroup: eventGroup, eventType: eventType });
		return events;
	};
	
	/**
	 * @function
	 * @description Function to get all events belonging to a group
	 * @param {string} eventGroup
	 * @returns {Array<MapEvent>|undefined} the events if found, otherwise returns undefined
	 */
	this.getEventsByGroup = function(eventGroup){
		return this.getEventsByGroupAndType({ eventGroup: eventGroup });
	};
	
	/**
	 * @function
	 * @description Function to get all events belonging to a group and optional type
	 * @param {object} { eventGroup, eventType = null }
	 * @returns {Array<MapEvent>|undefined} the events if found, otherwise returns undefined
	 */
	this.getEventsByGroupAndType = function({ eventGroup, eventType = null }){
		var positions = this.getEventPositionInStack('group', eventGroup);
		if(positions[0] != -1){
			var groupEvents = [];
			for(var i=0; i<positions.length; i++){
				const event = this.getEvents()[positions[i]];
				if (!eventType || event.type === eventType)
					groupEvents.push(event);
			}
			return groupEvents;
		}
		else
			console.log('event of group ' + eventGroup + ' could not be found');
	};
	
	/**
	 * @function
	 * @description Function to get all events by name
	 * @param eventName
	 */
	this.getEventsByName = function(eventName){
		var positions = this.getEventPositionInStack('name', eventName);
		if(positions[0] != -1){
			var events = [];
			for(var i=0; i<positions.length; i++){
				const event = this.getEvents()[positions[i]];
				events.push(event);
			}
			return events;
		}
		else
			console.log('event of name ' + eventName + ' could not be found');
	};
}]);
