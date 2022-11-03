import store from '@/mapmanagement/store/index';
import MapEvent from '@/mapmanagement/components/Map/models/Event';

// add jquery events do be used in angularjs
(window as any).jQuery(document).on("pushEvent", (e,eventObj) => {
  store.commit('pushEvent', eventObj);
});
(window as any).jQuery(document).on("removeEventsByGroup", (e,eventGroup) => {
  store.dispatch('removeEventsByGroup', eventGroup);
});
(window as any).jQuery(document).on("removeEventByName", (e,eventName) => {
  store.dispatch('removeEventByName', eventName);
});
(window as any).jQuery(document).on("removeEventsByGroupAndType", (e,eventGroupAndType) => {
  store.dispatch('removeEventsByGroupAndType', eventGroupAndType);
});

/**
 * @function
 * @description Function returning an array of index positions of the events matching the key:value pair.
 * @param {string} key - any MapEvent property name
 * @param {string} value - the value to search for
 * @returns {Array<number>} Array of indices of the events matching the key:value pair
 */
function getEventPositionInStack (key, value) {
  let positions = [-1];
  let i = 0;

  store.getters.getEvents.forEach((event, index) => {
    if(event[key] === value)
      positions[i++] = index;
  });
  return positions;
}

const state = {
    events: [],
    hoverCurrentCoordinate: null,
    lastHoverFeatures: [],
    currentPixel: null,
    featuresAtPixel: {}
  }
  
  // getters
  const getters = {
    getEvents: (state) => {
      return state.events;
    },
    getHoverCurrentCoordinate: (state) => {
      return state.hoverCurrentCoordinate;
    },
    getLastHoverFeatures: (state) => {
      return state.lastHoverFeatures;
    },
    getEventPositionInStack: (state) => (key, value) => {
      return getEventPositionInStack(key, value);
    },
    getCurrentPixel: (state) => {
      return state.currentPixel;
    },
    getFeaturesAtPixel: (state) => {
      return state.featuresAtPixel;
    },
  
    /**
    * @description Function to get all events belonging to a group and optionally type
	  * @param {string} eventGroup
	  * @param {string} eventType (optional)
	  * @returns {Array<MapEvent>|undefined} the events if found, otherwise returns undefined
    */
    getEventsByGroupAndType: (state) => ({ eventGroup, eventType = null }) => {
      let positions = getEventPositionInStack('group', eventGroup);
      if (positions[0] != -1) {
        let groupEvents = [];
        for (let i=0; i<positions.length; i++){
          const event = state.events[positions[i]];
          if(!eventType || event.type===eventType)
            groupEvents.push(event);
        }
        return groupEvents;
      }
      else {
          console.log('event of group '+eventGroup+' could not be found');
      }
    }
  }
  
  // actions
  const actions = {
  
    /**
    * @description Function to de-register event at specified position
    * @param {number} position
    * @returns {Array<MapEvent>|undefined} the event
    */
    updateOlLayers({ state }) {
      state.events.forEach(event => {
        event.updateOlLayers();
      });
    },
  
    /**
    * @description Function to de-register event at specified position
    * @param {number} position
    * @returns {Array<MapEvent>|undefined} the event
    */
    removeEventByPosition({ state }, { position }) {
      state.events[position].removeEventFromMap();
      state.events.splice(position, 1);
    },
  
    /**
    * @description Function to de-register an event by its name
    * @param {string} event name
    * @returns {MapEvent|undefined} the event if found, otherwise returns undefined
    */
    removeEventByName({ dispatch }, eventName) {
      let positions = getEventPositionInStack('name', eventName);
      if (positions[0] != -1) {
        dispatch('removeEventByPosition', { position: positions[0] });
      }
      else {
        console.log('event of type ' + eventName + ' could not be found');
      }
    },
  
    /**
    * @description Function to de-register all events belonging to a group
    * @param {string} eventGroup
    * @returns {Array<MapEvent>|undefined} the events if found, otherwise returns undefined
    */
    removeEventsByGroup({ dispatch }, eventGroup) {
      dispatch('removeEventsByGroupAndType', { eventGroup: eventGroup });
    },
  
    /**
    * @description Function to de-register all events belonging to a group that are of a certain type
	  * @param {string} eventGroup
	  * @param {string} eventType
    */
    removeEventsByGroupAndType({ state, dispatch }, { eventGroup, eventType = null }) {
      let positions = getEventPositionInStack('group', eventGroup);
      if (positions[0] != -1) {
        for(var i=positions.length-1; i>=0; i--){
          const event = state.events[positions[i]];
          if(!eventType || event.type===eventType)
            dispatch('removeEventByPosition', { position: positions[i] })[0];
        }
      }
      else {
          console.log('event of group '+eventGroup+' could not be found');
      }
    }
  }
  
  // mutations
  const mutations = {

    /**
     * @description Function to register an event
     * @param {MapEvent} event
     * @returns undefined
     */
    pushEvent(state, eventObj) {  
      //the if-statement is quick-fix for controller being called twice, needs to be fixed
      if (getEventPositionInStack('name', eventObj.name)[0]===-1) {
        let event;
        if(eventObj.constructor===MapEvent)
          event = eventObj;
        else
          event = new MapEvent(eventObj);

        state.events.push(event);
        event.addEventToMap();
      } 
      else {
        console.log('event cannot be added because event of name '+eventObj.name+' already exists in group '+eventObj.group);
        console.log(state.events);
      }
    },

    setHoverCurrentCoordinate(state, coordinate) {
      state.hoverCurrentCoordinate = coordinate;
    },
    setLastHoverFeatures(state, features) {
      state.lastHoverFeatures = features;
    },
    setCurrentPixel(state, currentPixel) {
      state.currentPixel = currentPixel;
    },
    setFeaturesAtPixel(state, features) {
      state.featuresAtPixel = features;
    }
  }
  
  export default {
    state,
    getters,
    actions,
    mutations
  };

  (window as any).MapEvents = state.events;