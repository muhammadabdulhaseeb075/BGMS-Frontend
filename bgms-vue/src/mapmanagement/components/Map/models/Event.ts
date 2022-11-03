import store from '@/mapmanagement/store/index';
import { getOlLayers, getOLFeatures } from '@/mapmanagement/components/Map/models/Layer';
  
const DELAYLENGTHSHORT: number = 50

/**
 * @description
 * A very basic representation of an event, loosely linked via directive to ol.MapEvent
 * @param {string} name - unique name for identification
 * @param {string} group - if it belongs to a user action eg draw, layerswitch, personselect etc
 * @param {Array<string>=} layerGroup - the layergroup it affects, (optional, can be an array of layergroup names)
 * @param {string} type - 'click', 'singleclick', 'dblclick', 'pointerdrag', 'pointermove', 'postrender' or 'moveend'
 * @param {function} handler - handler_function(event, featuresAtEvent, layernames)
*/
export default class MapEvent {

  name;
  group;
  type;
  handler;
  layers;
  layerGroups;
  layerNames;
  olLayers = null;
  bindedHandlerFunction;

  constructor(eventConstructorObject) {
    this.name = eventConstructorObject.name;
    this.group = eventConstructorObject.group;
    this.type = eventConstructorObject.type;
    this.handler = eventConstructorObject.handler;
    this.layers = [];
    /**
     * @description
     * Array to store layer groups so that when a group is refreshed, the
     * events can be updated to include the updated layers
     */
    this.layerGroups = eventConstructorObject.layerGroup || [];
    /**
     * @description
     * Array to store layer names so that when a group is refreshed, the
     * events can be updated to include the updated layers
     */
    this.layerNames = eventConstructorObject.layerNames || [];
    
    this.createLayers();

    this.bindedHandlerFunction = this.handlerFunction.bind(this);
  }

  handlerFunction(event){

    let delayLength: number = 0;

    const hoverPointerMoveEvent = this.type==='pointermove' && this.name.indexOf("hover")===0;

    // For pointermove events with a name begining with 'hover'
    // add a 150ms delay. This pervents the event being called excessively.
    // Tiny delay if previous coord was over a feature.
    if (hoverPointerMoveEvent) {
      store.commit('setHoverCurrentCoordinate', event.coordinate);
      delayLength = store.getters.getLastHoverFeatures.length ? DELAYLENGTHSHORT : 150;

      window.setTimeout(function() {
        // the mouse mustn't have moved during the duration of the timeout
        if (delayLength === DELAYLENGTHSHORT || event.coordinate === store.getters.getHoverCurrentCoordinate) {
          this.processEvent(event, delayLength);
          
        }
      }.bind(this), delayLength);
    }
    else
      this.processEvent(event, delayLength);
  }

  processEvent(event, delayLength) {
    if(this.type != 'pointerdrag' && event.dragging){
      return;
    } 
    else if(this.type === 'pointerdrag' && event.dragging){
        // stop map moving on drag
        event.preventDefault();
    }

    let callback = this.handler;
    let layers = this.olLayers;
    let coordinate = event.coordinate;
    let resolution = event.frameState.viewState.resolution;

    if (layers) {
      let featuresAtCoordinate = getOLFeatures(layers, coordinate, event.pixel, resolution, this.name.substring(0,16) === "memorial-capture");
      let features = featuresAtCoordinate[0];
      let layerNames = featuresAtCoordinate[1];

      if (delayLength) {
        // if previously hovering over a feature, only highlight new feature if coordinates haven't changed during delay
        if (features.length && delayLength === DELAYLENGTHSHORT && event.coordinate !== store.getters.getHoverCurrentCoordinate && JSON.stringify(features[0]) !== JSON.stringify(store.getters.getLastHoverFeatures[0]))
          features = [];

          store.commit('setLastHoverFeatures', features);
      }

      callback(event, features, layerNames);
    }
  }

  updateOlLayers() {
    this.olLayers = getOlLayers(this.layers, true);
  }

  addEventToMap() {
    this.updateOlLayers();
    (window as any).OLMap.on(this.type, this.bindedHandlerFunction);
  }

  removeEventFromMap() {
    (window as any).OLMap.un(this.type, this.bindedHandlerFunction);
  }

  public createLayers() {
    this.layers = [];
    if(this.layerGroups){
      if(typeof this.layerGroups === 'string'){
        let layerGroup = store.getters.getLayerGroupByName(this.layerGroups);
        if (layerGroup)
          this.layers.push.apply(this.layers, Object.keys(layerGroup.getAllLayers()));
      } else if(this.layerGroups.constructor === Array){
        for(var index in this.layerGroups){
          let layerGroup = store.getters.getLayerGroupByName(this.layerGroups[index]);
          if (layerGroup)
            this.layers.push.apply(this.layers, Object.keys(layerGroup.getAllLayers()));
        }
      }
    }
    if (this.layerNames){
      if (typeof this.layerNames === 'string'){
        this.layers.push(this.layerNames);
      } 
      else if (this.layerNames.constructor === Array) {
        for(let index in this.layerNames){
          this.layers.push(this.layerNames[index]);
        }          
      }
    }
  }
  
  addLayerNames(layerNames) {
    if(layerNames){
      if (typeof layerNames === 'string') {
        this.layers.push(layerNames);
        this.layerNames.push(layerNames);
      } 
      else if (layerNames.constructor === Array) {
        for(let index in this.layerNames){
          this.layers.push(layerNames[index]);
          this.layerNames.push(layerNames[index]);
        }          
      }
    }
  }
  
  removeAllLayers() {
    this.layers = [];      
  }
}