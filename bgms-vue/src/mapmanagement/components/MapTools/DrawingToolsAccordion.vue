<template>
<!--<div></div>-->

  <div id="v-VueDrawingToolsController">
    <div id="drawingToolsAccordion">
      <label class="btn btn-bgms group-drawingtools" title="Drawing Tools" data-toggle="collapse" data-parent="#drawingToolsAccordion" href="#drawingTools">
        <input type="radio" autocomplete="off" checked hidden>
        <span class="icon-Map-Measurement-Tools-Outline"></span>
        <span class="icon-Map-Measurement-Tools-Filled"></span>
      </label>
      <div id="drawingTools" class="btn-group panel-collapse collapse" role="group">
        <label class="btn btn-bgms" aria-label="Measure Distance" title="Measure Distance" :class="{active: drawLineFlag}">
        <input type="checkbox" name="drawline" :value="drawLineFlag" autocomplete="off" @click="addInteraction('draw_line')" checked hidden>
        <span class="icon-Measure-Distance-02"></span>
        </label>
        <label class="btn btn-bgms" aria-label="Measure Area" title="Measure Area" :class="{active: drawPolygonFlag}">
          <input type="checkbox" name="drawpolygon" :value="drawPolygonFlag" autocomplete="off" @click="addInteraction('draw_polygon')" checked hidden>
          <span class="icon-Measure-Area-Filled"></span>
        </label>
        <label class="btn btn-bgms"  aria-label="Modify" title="Modify Drawings" :class="{active: modifyDrawingFlag}">
          <input type="checkbox" name="modify" :value="modifyDrawingFlag" autocomplete="off" @click="addInteraction('modify_drawing')" checked hidden>
          <span class="icon-Edit-Drawing-Filled"></span>
        </label>
        <label class="btn btn-bgms"  aria-label="Delete" title="Delete Drawings" :class="{active: deleteDrawingFlag}">
          <input type="checkbox" name="delete" :value="deleteDrawingFlag" autocomplete="off" @click="addInteraction('delete_drawing')" checked hidden>
          <span class="icon-Delete-Filled"></span>
        </label>
      </div>
    </div>
  </div>

</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'

import { unByKey } from 'ol/Observable';
import { getArea, getLength } from 'ol/sphere';
import { click } from 'ol/events/condition';

Vue.use(Vuex);


/*
The draw toolbar adds the following interactions:
  drawPolygon - draw(drawstart, drawend, onfeaturechange), pointer(pointermove)
  drawLine - draw(drawstart, drawend, onfeaturechange), pointer(pointermove)
  select - select(onselectstart, onselectend)
  modify - modify, select
  delete - select

It adds the following layers:
  draw-layer

It adds the following overlays:
  drawPolygon - measurement-overlay#uniqueId, drawing-message-overlay
  drawLine - measurement-overlay#uniqueId, drawing-message-overlay
  select - drawing-message-overlay
  modify - measurement-overlay#uniqueId (only modifies this), drawing-message-overlay
  delete - drawing-message-overlay
*/


const interactionGroupName = 'draw';
const interactionLayer = 'draw';

const startDrawingMessage = "Click to start Drawing.";
const continueDrawingMessage = "Click to continue Drawing.<br/>Double-click to stop Drawing.";
const startModifyMessage = "Click on drawing to select it for modification.";
const continueModifyMessage = "Drag to modify.";
const startDeleteMessage = "Click on drawing to delete.";

/**
 * Class representing DrawingTools component
 * @extends Vue
 */
@Component
export default class DrawingTools extends Vue{

  drawingInProgress: boolean = false;
  modificationInProgress: boolean = false;

  permanentNotification: any = null;

  listenerKey;
  lengthMarker = null;

  toolbarService: any = this.$store.getters.toolbarService;
  interactionService: any = this.$store.getters.interactionService;
  styleService: any = this.$store.getters.styleService;
  markerService: any = this.$store.getters.markerService;
  notificationHelper: any = this.$store.getters.notificationHelper;

   /**
    * Vue mounted lifecycle hook
    */
  mounted() {
    //registers jQuery event to listen for stop drawing command
    (window as any).jQuery(document).on('stopDrawing', this.stopDrawing);
  }

  /*** Computed ***/

  /**
   * Computed property:
   * @returns {boolean} True if draw line tool has been selected
   */
  get drawLineFlag(): boolean {
    return this.toolbarService.toggle["draw_line"];
  }

  /**
   * Computed property:
   * @returns {boolean} True if draw polygon tool has been selected
   */
  get drawPolygonFlag(): boolean {
    return this.toolbarService.toggle["draw_polygon"];
  }

  /**
   * Computed property:
   * @returns {boolean} True if modify drawing tool has been selected
   */
  get modifyDrawingFlag(): boolean {
    return this.toolbarService.toggle["modify_drawing"];
  }

  /**
   * Computed property:
   * @returns {boolean} True if delete drawing tool has been selected
   */
  get deleteDrawingFlag(): boolean {
    return this.toolbarService.toggle["delete_drawing"];
  }


  /*** Methods ***/

  /**
   * Adds interaction to Map
   * @param eventType
   */
  addInteraction(eventType) {

    let v = this;

    switch (eventType) {
      case 'draw_line':
        v.toolbarService.toggle[eventType] = !v.drawLineFlag;
        v.toolbarService.toggle_option(eventType).then(function(is_enabled){
          if(is_enabled) {
            v.drawLineInteraction();
            v.permanentNotification = v.notificationHelper.createPermanentInfoNotification(startDrawingMessage);
          }
        });
        break;
      case 'draw_polygon':
        v.toolbarService.toggle[eventType] = !v.drawPolygonFlag;
        v.toolbarService.toggle_option(eventType).then(function(is_enabled){
          if(is_enabled) {
            v.drawPolygonInteraction();
            v.permanentNotification = v.notificationHelper.createPermanentInfoNotification(startDrawingMessage);
          }
        });
        break;
      case 'modify_drawing':
        v.toolbarService.toggle[eventType] = !v.modifyDrawingFlag;
        v.toolbarService.toggle_option(eventType).then(function(is_enabled){
          if(is_enabled) {
            v.modifyInteraction();
            v.permanentNotification = v.notificationHelper.createPermanentInfoNotification(startModifyMessage);
          }
        });
        break;
      case 'delete_drawing':
        v.toolbarService.toggle[eventType] = !v.deleteDrawingFlag;
        v.toolbarService.toggle_option(eventType).then(function(is_enabled){
          if(is_enabled) {
            v.deleteInteraction();
            v.permanentNotification = v.notificationHelper.createPermanentInfoNotification(startDeleteMessage);
          }
        });
        break;
      default:
        return;
     }
  }

  /**
   * Create new ol interaction to draw a line
   */
  drawLineInteraction() {
    this.$store.commit('pushInteraction', {
      group: interactionGroupName,
      type: 'draw',
      parameters: {
        type: 'LineString',
        layer: interactionLayer,
        style: this.styleService.drawInteractionStyleFunction
      },
      handlers: {
        drawstart: (evt) => {
          let calculateLength = this.calculateLength;
          let featureChangeHandler = () => { this.featureChangeHandler(calculateLength, evt); };
          this.startDrawing(featureChangeHandler, evt);
        },
        drawend: (evt) => {
          this.finishDrawing(evt);
          this.toolbarService.simulated_click('draw_line');
        }
      }
    });
  }

  /**
   * Create new ol interaction to draw a polygon
   */
  drawPolygonInteraction() {
    this.interactionService.pushInteraction({
      group: interactionGroupName,
      type: 'draw',
      parameters: {
        type: 'Polygon',
        layer: interactionLayer,
        style: this.styleService.drawInteractionStyleFunction
      },
      handlers: {
        drawstart: (evt) => {
          let calculateArea = this.calculateArea;
          let featureChangeHandler = () => { this.featureChangeHandler(calculateArea, evt); };
          this.startDrawing(featureChangeHandler, evt);
        },
        drawend: (evt) => {
          this.finishDrawing(evt);
            this.toolbarService.simulated_click('draw_polygon');
        }
      }
    });
  }

  /**
   * Create new ol interaction to modify a drawing
   */
  modifyInteraction() {
    this.interactionService.pushInteraction({
      group: interactionGroupName,
      type: 'select',
      parameters: {
        condition: click,
        layer: interactionLayer,
        style: this.styleService.drawInteractionStyleFunction
      },
      handlers: {
        handleSelect: (feature) => {
          this.startModifyDrawing(feature);
        },
        handleUnselect: (feature) => {
          this.stopModifyDrawing(feature);
          this.toolbarService.simulated_click('modify_drawing');
        }
      }
    });
    this.interactionService.pushInteraction({
      group: interactionGroupName,
      type: 'modify',
      parameters: {
        selectFeatures: 'select',
        style: this.styleService.drawInteractionStyleFunction
      }
    });
  }

  /**
   * Create new ol interaction to delete a drawing
   */
  deleteInteraction() {
    this.interactionService.pushInteraction({
      group: interactionGroupName,
      type: 'select',
      parameters: {
        condition: click,
        layer: interactionLayer
      },
      handlers: {
        handleSelect: (feature) => {
          this.deleteDrawing(feature);
          this.toolbarService.simulated_click('delete_drawing');
        }
      }
    });
  }

  /**
   * Called when user clicks on map to start drawing
   */
  startDrawing(featureChangeFunction, evt) {
    this.listenerKey = evt.feature.on('change', featureChangeFunction);
    console.log('startDrawing');
    this.drawingInProgress = true;
    this.permanentNotification.update({
      title: continueDrawingMessage
    });
  }

  /**
   * Called when user clicks on map to finish drawing
   */
  finishDrawing(evt) {
    this.drawingInProgress = false;
    // TODO: Remove change handler from feature
    if(this.listenerKey)
      unByKey(this.listenerKey);
    // TODO: make a drawing cache to saving the drawings
    var randomId = Math.random();
    evt.feature.setId(randomId);
    if(this.lengthMarker){
      this.lengthMarker.group = 'feature-measurement';
      this.lengthMarker.class = 'tooltip tooltip-static';
      this.lengthMarker.name = randomId;
    }
    this.stopDrawing();
  }

  /**
   * Stops the drawing tool
   */
  stopDrawing() {
    this.$store.commit('removeInteractionsByGroup', interactionGroupName);
    this.$store.dispatch('removeEventsByGroup', interactionGroupName);
    this.$store.commit('removeMarkersByGroup', interactionGroupName);
    this.lengthMarker = null;

    if (this.permanentNotification) {
      this.notificationHelper.removePermanentInfoNotification(this.permanentNotification);
      this.permanentNotification = null;
    }
  }

  /**
   * Called when user clicks on map to modify a drawing
   */
  startModifyDrawing(element) {
    this.modificationInProgress = true;
    const id = element.element.getId();
    let marker = this.markerService.getMarkerByName(id);
    marker.class = 'tooltip tooltip-measure';
    this.listenerKey = element.element.on('change', (feature) => {
      var geometry = feature.target.getGeometry();
      if(geometry.getType() == 'LineString')
        marker.message = this.calculateLength(geometry)
      else if(geometry.getType() == 'Polygon')
        marker.message = this.calculateArea(geometry)
    });

    this.permanentNotification.update({
      title: continueModifyMessage
    });
  }

  /**
   * Called when user clicks on map to stop modifing a drawing
   */
  stopModifyDrawing(element) {
    const id = element.element.getId();
    let marker = this.markerService.getMarkerByName(id);
    marker.class = 'tooltip tooltip-static';

    if(this.listenerKey)
      unByKey(this.listenerKey);
    this.modificationInProgress = false;
    this.stopDrawing();
  }

  /**
   * Called when user clicks on map to delete a drawing
   */
  deleteDrawing(feature) {
    let v = this;

    console.log('delete');

    (window as any).OLMap.getLayers().forEach(function(element){
      if(element.get('name') === interactionLayer){
        const featureId = feature.element.getId();
        v.markerService.removeMarkerByName(featureId);
        element.getSource().removeFeature(feature.element);
        feature.target.remove(feature.element);
      }
    });

    v.stopDrawing();
  }

  featureChangeHandler(measureFunction, evt) {
    var geometry = evt.feature.getGeometry();
    var coordinate = geometry.getLastCoordinate();
    console.log('this.featureChangeHandler');
    if(this.drawingInProgress){
      //show continue drawing overlay
      if(!this.lengthMarker){
        this.lengthMarker = this.markerService.pushMarker({
          group: 'draw',
          name: 'draw-area',
          class: 'tooltip tooltip-measure',
          positioning: ['bottom-center', 'bottom-center'],
                  offset: {
                    "bottom-center": [0, -15]
                  },
          position: coordinate,
          message: measureFunction(geometry)
        });
      } else{
        this.lengthMarker.position = coordinate;
        this.lengthMarker.message = measureFunction(geometry);
      }
    }
  }

  /**
   * Calculates area of polygon
   */
  calculateArea(polygon) {
    var area = getArea(polygon);
    var output;
    output = (Math.round(area * 100) / 100) +
      ' ' + 'm<sup>2</sup>';
    return output;
  }

  /**
   * Calculates length of line
   */
  calculateLength(line) {
    var length = Math.round(getLength(line) * 100) / 100;
    var output;
      output = (Math.round(length * 100) / 100) + ' ' + 'm';
    return output;
  }
}
</script>
