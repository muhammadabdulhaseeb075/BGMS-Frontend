<template>
  <div :id="componentName" v-if="componentData">
    <ScrollButtons :heightChangedFlag="heightChangedFlag">
      <form class="form-horizontal form-box-inside management-tool-form" @submit.prevent="onSubmit" v-if="!linkBurials">

        <FormButtons v-if="siteAdminOrSiteWarden" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="true" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>

        <div class="blank-form-placeholder" v-if="!(editFlag || componentData.status || componentData.state || componentData.type || componentData.size || componentData.depth || componentData.perpetual || componentData.consecrated || componentData.remarks || componentData.memorial_comment || componentData.grave_number || componentData.section_id || componentData.subsection_id)">No grave details recorded.</div>
        <div v-else>
          <section>

            <GraveRef
                    :editFlagProp="editFlag"
                    :componentData="componentData"
                    :componentDataSaved="componentDataSaved"
                    v-model="componentData.grave_number"
                    :saving="saving"
                    v-on:onLoadData="updateChangesFromVerify($event)"
                    v-on:onVerify="updateSuccessVerification()"/>

            <div class="row field-row" v-if="(editFlag || componentData.status) && $store.state.ManagementTool.statusList && $store.state.ManagementTool.statusList.length > 0">
              <label :class="labelColumnClasses" for="grave-status">Status:</label>
              <div id="grave-status" :class="fieldColumnClasses">
                <select :disabled="!editFlag" class="form-control" v-model="componentData.status" @keyup.enter="validateGraveNumber">
                  <option :value="null"></option>
                  <option v-for="status in $store.state.ManagementTool.statusList" :value="status.id" :key="status.id">
                    {{ status.status }}
                  </option>
                </select>
              </div>
            </div>
            <div class="row field-row" v-if="(editFlag || componentData.state) && $store.state.ManagementTool.stateList && $store.state.ManagementTool.stateList.length > 0">
              <label :class="labelColumnClasses" for="grave-state">State:</label>
              <div id="grave-state" :class="fieldColumnClasses">
                <select :disabled="!editFlag" class="form-control" v-model="componentData.state" @keyup.enter="validateGraveNumber">
                  <option :value="null"></option>
                  <option v-for="state in $store.state.ManagementTool.stateList" :value="state.id" :key="state.id">
                    {{ state.state }}
                  </option>
                </select>
              </div>
            </div>
            <div class="row field-row" v-if="(editFlag || componentData.type) && $store.state.ManagementTool.typeList && $store.state.ManagementTool.typeList.length > 0">
              <label :class="labelColumnClasses" for="grave-type">Type:</label>
              <div id="grave-type" :class="fieldColumnClasses">
                <select :disabled="!editFlag" class="form-control" v-model="componentData.type" @keyup.enter="validateGraveNumber">
                  <option :value="null"></option>
                  <option v-for="type in $store.state.ManagementTool.typeList" :value="type.id" :key="type.id">
                    {{ type.type }}
                  </option>
                </select>
              </div>
            </div>
            <div class="row field-row" v-if="editFlag || componentData.size">
              <label :class="labelColumnClasses" for="size">Overall Size:</label>
              <div v-if="!editFlag" id="size" :class="fieldColumnClasses">
                <input readonly type="text" class="form-control" :value="componentData.size + (componentData.size_units ? ' ' + componentData.size_units : '')">
              </div>
              <div v-if="editFlag" id="size" class="col-xs-5 no-padding">
                <input :readonly="!editFlag" type="text" class="form-control" placeholder="Size" maxlength="15" v-model="componentData.size">
              </div>
              <div v-if="editFlag" id="size_units" class="col-xs-3 no-padding">
                <input type="text" class="form-control" placeholder="Units" maxlength="15" v-model="componentData.size_units">
              </div>
            </div>
            <div class="row field-row" v-if="editFlag || componentData.depth">
              <label :class="labelColumnClasses" for="depth">Overall Depth:</label>
              <div v-if="!editFlag" id="depth" :class="fieldColumnClasses">
                <input readonly type="text" class="form-control" :value="componentData.depth + (componentData.depth_units ? ' ' + componentData.depth_units : '')">
              </div>
              <div v-if="editFlag" id="depth" class="col-xs-5 no-padding">
                <input type="number" step="0.01" min="0" class="form-control" :placeholder="editFlag ? 'Depth' : 'None'" maxlength="15" v-model.number="componentData.depth">
              </div>
              <div v-if="editFlag" id="depth_units" class="col-xs-3 no-padding">
                <input type="text" class="form-control" placeholder="Units" maxlength="15" v-model="componentData.depth_units">
              </div>
            </div>

            <StandardInputRow :label="'Perpetual'" v-model="componentData.perpetual" :inputType="'checkbox'" :readonlyOption="true" :editFlag="editFlag"/>
            <StandardInputRow :label="'Consecrated'" v-model="componentData.consecrated" :inputType="'checkbox'" :readonlyOption="true" :editFlag="editFlag"/>

          </section>

          <StandardInputRow :label="'Remarks'" v-model="componentData.remarks" :inputType="'textarea'" :attributes="{ maxlength:400 }" :editFlag="editFlag"/>
          <StandardInputRow :label="'Memorial Comment'" v-model="componentData.memorial_comment" :inputType="'textarea'" :attributes="{ maxlength:400 }" :editFlag="editFlag"/>
          <h2 v-if="feature"> Geometry </h2>        
          <SelectInputRow v-if="featureType && featureType===featureTypesEnum.memorial" label="Shape" v-model="shape" :editFlag="editFlag" :options="[{value:shapesEnum.CIRCLE},{value:shapesEnum.RECTANGLE}]" :optionValueName="'value'" :optionKeyName="'value'" :optionLabelName="'value'"/>

          <StandardInputRow v-if="shape===shapesEnum.CIRCLE" :label="'Diameter'" :editFlag="editFlag" :readonlyOption="true" v-model.number="length" :inputType="'number'" :attributes="{ step:0.01, min:0.01, max:5 }" :unit="' m'"/>

          <StandardInputRow v-if="shape===shapesEnum.RECTANGLE" :label="'Length'" :editFlag="editFlag" :readonlyOption="true" v-model.number="length" :inputType="'number'" :attributes="{ step:0.01, min:0.01, max:5 }" :unit="' m'"/>

          <StandardInputRow v-if="shape===shapesEnum.RECTANGLE" :label="'Width'" :editFlag="editFlag" :readonlyOption="true" v-model.number="width" :inputType="'number'" :attributes="{ step:0.01, min:0.01, max:5 }" :unit="' m'"/>

          <StandardInputRow v-if="shape===shapesEnum.RECTANGLE" :label="'Rotation'" :editFlag="editFlag" :readonlyOption="true" v-model.number="roundedRotation" :inputType="'number'" :attributes="{ step:0.1 }" showFalsyValue="true" :unit="'°'"/>

          <FormButtons v-if="siteAdminOrSiteWarden" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="false" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>

        </div>
      </form>

      <LinkBurialsToGraveOrMemorial
        v-else-if="linkBurials"
        :message="`You have changed the grave number to ${componentData.grave_number}. The following transcribed and unlinked persons have been assigned this same grave number. Would you like to link them to this grave and any linked memorials?`"
        :distinctPersonsOrBurials="linkBurials"
        :linkToGrave="true"
        :addToMemorialsLinkedToGrave="true"
        :graveplotUUID="id"
        @linksMadeSuccessfully="updateComponentData()"
        @closeComponent="linkBurials = null">
      </LinkBurialsToGraveOrMemorial>

    </ScrollButtons>    
  </div>
  <div v-else class="loading-placeholder">
    <div class="loading-placeholder-contents">
      <i class="fa fa-spinner fa-spin"/>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component, { mixins } from 'vue-class-component';
import { Prop, Watch } from 'vue-property-decorator';
import axios from 'axios';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';
import FormButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/FormButtons.vue';
import StandardInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/StandardInputRow.vue';
import GraveRef from '@/mapmanagement/components/ManagementTool/Components/GraveRef.vue';
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';
import NotificationMixin from "@/mixins/notificationMixin";
import {messages} from "@/global-static/messages";
import SelectInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/SelectInputRow.vue';
import { getCenter } from 'ol/extent';
import LineString from 'ol/geom/LineString';
import Circle from 'ol/geom/Circle';
import Polygon from 'ol/geom/Polygon';
import MultiPolygon from 'ol/geom/MultiPolygon';
import GeoJSON from 'ol/format/GeoJSON';
import constants, {FEATURE_TYPES_ENUM} from '@/global-static/constants';
import FeatureTools from '@/mapmanagement/mixins/featureTools';

enum SHAPES { CIRCLE="CIRCLE", RECTANGLE="RECTANGLE" }

/**
 * Class representing GraveDetails component
 * @extends mixins: ManagementToolsMixin
 */
@Component({
  components: {
    FormButtons,
    StandardInputRow,
    GraveRef,
    ScrollButtons,
    SelectInputRow,
    LinkBurialsToGraveOrMemorial: () => import('@/mapmanagement/components/ManagementTool/Components/LinkBurialsToGraveOrMemorial.vue'),
  }
})
export default class GraveDetails extends mixins(NotificationMixin, ManagementToolsMixin, FeatureTools){

  @Prop() id;
  @Prop() layer;
  saving: boolean = false;

  linkBurials = null;
  verified: boolean = false;

  geometryHelperService = this.$store.getters.geometryHelperService;
  loading: boolean = true;

  feature = null;
  featureCenterPoint = null;

  width = -10;
  length = -10;
  rotation = -10;

  shapesEnum = SHAPES;
  shape: SHAPES = null;
  originalShape: SHAPES = null;

  featureTypesEnum = constants.FEATURE_TYPES;
  featureType: FEATURE_TYPES_ENUM;
validateGraveNumber: (payload: KeyboardEvent) => void;

  /**
   * Vue mounted lifecycle hook
   * - Loads option for select boxes
   */
  mounted() {
    debugger; //eslint-disable-line no-debugger
    this.componentName = "grave_details";
    this._id = this.id;

    this.editableFields = ['coordinates', 'status', 'state', 'type', 'size', 'size_units', 'depth', 'depth_units', 'perpetual', 'consecrated', 'memorial_comment', 'remarks', 'grave_number'];

    let featureID = this.id;

    if (this.layer==='available_plot') {
      featureID = this.$route.params.availablePlotID;
    }

    this.loading = true;
    
    this.getFeatureFromLayer(featureID, this.layer)
    .then(value => {
      this.feature = value;
      
      debugger; //eslint-disable-line no-debugger
      // get coordinates and store
      let geometry = null;
      if(this.feature){
        geometry = this.feature.getGeometry();  
      }
      //const geometry = this.feature.getGeometry();
      let coordinates = null;
      if(geometry!= null){
        coordinates = geometry.getCoordinates()[0][0];
        // load data
        this.loadData('/mapmanagement/graveDetails/?graveplot_uuid=', this.id, { coordinates: coordinates });
        this.originalShape = this.shape = this.getPolygonShape(coordinates);      
        this.calculatePolygonGeometry();
      }else{
        this.loadData('/mapmanagement/graveDetails/?graveplot_uuid=', this.id)
      }
    });

    if (this.isRouteActive(constants.MEMORIAL_MANAGEMENT_PATH))
      this.featureType = this.featureTypesEnum.memorial;
    else if (this.isRouteActive(constants.GRAVE_MANAGEMENT_PATH))
      this.featureType = this.featureTypesEnum.grave;
    
    // if lists have not yet been loaded into vuex, load them
    if (!this.$store.state.ManagementTool.statusList
      && !this.$store.state.ManagementTool.stateList
      && !this.$store.state.ManagementTool.typeList) {

      axios.get('/mapmanagement/allGravePlotOptions')
      .then(response => {
        this.$store.commit('setGraveDetailLists', response.data);
      })
      .catch(response => {
        console.warn('Couldn\'t get grave details lists (status, state, type):', response);
      });
    }
    //this.loading = false;
  }
  destroyed() {
    if (this.editFlag) {
      this.feature.getGeometry().setCoordinates([[this.componentDataSaved.coordinates]]);
      this.geometryHelperService.stopRotateFeature();
    }
  }

  updateChangesFromVerify(data){

    // get coordinates and store
    const geometry = this.feature.getGeometry();
    const coordinates = geometry.getCoordinates()[0][0];
    Object.assign(data, coordinates);

    this.$store.commit('setCurrentInformation', { componentName: this.componentName, data: data });
    this.componentData = this.$store.state.ManagementTool.currentInformation[this.componentName];
    this.updateSuccessVerification();
  }

  updateSuccessVerification(){
    this.verified = true;
  }

  /**
   * Computed property: gets rounded rotation in degrees
   */
  get roundedRotation() {
    return Math.round(this.rotation * (180 / Math.PI) * 10) / 10;
  }
  set roundedRotation(value) {
    this.rotation = value * Math.PI / 180;
  }

  /**
   * Return true if we need to display the RotateFeatureInteraction
   */
  get showRotateFeatureInteraction() {
    return this.editFlag && this.shape===this.shapesEnum.RECTANGLE;
  }

  /*** Watchers ***/
  
  /**
   * Event when shape is changed
   */
  @Watch('shape')
  onShapeChanged(val: any, oldVal: any) {

    if (!oldVal)
      return;

    this.updatePolygonCoordinates();
  }
  
  /**
   * Event when length is changed
   */
  @Watch('length')
  onLengthChanged(val: any, oldVal: any) {

    // oldVal === -10 initially
    if (this.loading || !val || oldVal===-10)
      return;
    
    if (val > 5) {
      this.length = 5;
      return;
    }

    this.updatePolygonCoordinates();
  }

  /**
   * Event when width is changed
   */
  @Watch('width')
  onWidthChanged(val: any, oldVal: any) {

    // oldVal === -10 initially
    if (this.loading || !val || oldVal===-10)
      return;
    
    if (val > 5) {
      this.width = 5;
      return;
    }

    this.updatePolygonCoordinates();
  }

  /**
   * Event when rotation is changed
   */
  @Watch('rotation')
  onRotationChanged(val: any, oldVal: any) {

    // oldVal === -10 initially
    if (this.loading || !val || oldVal===-10)
      return;
    
    this.geometryHelperService.rotate.setAngle(-val);
    this.componentData.coordinates = this.feature.getGeometry().getCoordinates()[0][0];
  }
  
  /**
   * Watcher: When edit in router query is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('editFlag')
  onEditFlagChanged(val: any, oldVal: any) {
    if (!val) {
      if (!this.saving) {
        // revert coorinates
        this.shape = this.originalShape;
        if(this.feature){
          this.feature.getGeometry().setCoordinates([[this.componentDataSaved.coordinates]]);
        }
        this.loading = true;
        this.length = -10;
        this.width = -10;
        this.rotation = -10;

        window.setTimeout(() => {
          // refreshes length, width and rotation
          this.calculatePolygonGeometry();
        });
      }
      else
        this.saving = false;
    }
  }
  
  /**
   * Watcher: When edit in router query is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('showRotateFeatureInteraction')
  onShowRotateFeatureInteractionChanged(val: any, oldVal: any) {
    if (val) {
      this.geometryHelperService.rotateFeature(this.feature,-this.rotation);
      this.geometryHelperService.rotate.on('rotateend', evt => {
        this.rotation = -evt.angle;
      });
    }
    else
      this.geometryHelperService.stopRotateFeature();
  }

  /*** Methods ***/

  /**
   * Calculates the shapes length,width,rotation using it's coordinates
   */
  calculatePolygonGeometry() {
debugger; //eslint-disable-line no-debugger
    this.loading = true;

    let coordinates;
    if (this.componentData){
       coordinates = this.componentData.coordinates;
    }
    else{
       coordinates = this.feature.getGeometry().getCoordinates()[0][0];
    }

    // get center point of feature
    let geometry = null;
    if(this.feature){
      geometry = this.feature.getGeometry();
    }
    //const geometry = this.feature.getGeometry();
    if(geometry != null){
      this.featureCenterPoint = getCenter(geometry.getExtent());
    }
    if (this.shape===this.shapesEnum.CIRCLE) {
      this.length = this.width = this.distanceBetweenPoints(this.featureCenterPoint, coordinates[0]) * 2;
      this.rotation = 0;
    }
    else if (this.shape===this.shapesEnum.RECTANGLE) {
      let highestPoint = null;

      // get the longest width, shortest width and first distance
      for (let i=0; i<4; i++) {
        const distance = this.distanceBetweenPoints(coordinates[i], coordinates[i+1]);

        if (this.width===-10 || distance < this.width)
          this.width = distance;

        if (this.length===-10 || distance > this.length)
          this.length = distance;

        if (highestPoint==null || coordinates[i][1] > coordinates[highestPoint][1])
          highestPoint = i;
      }

      let rotation = 0;

      // Calculate rotation - angle between longest side and north
      const firstDistance = this.distanceBetweenPoints(coordinates[highestPoint], coordinates[highestPoint+1]);
      let horizontalDistance = 0;
      let verticalDistance = 0;

      let clockwise = coordinates[highestPoint][0] <= coordinates[highestPoint+1][0] ? true : false;

      if (firstDistance===this.length) {
        highestPoint = highestPoint===0 ? 4 : highestPoint;
        horizontalDistance = coordinates[highestPoint][0] - coordinates[highestPoint-1][0];
        verticalDistance = coordinates[highestPoint][1] - coordinates[highestPoint-1][1];
      }
      else {
        highestPoint = highestPoint===4 ? 0 : highestPoint;
        horizontalDistance = coordinates[highestPoint+1][0] - coordinates[highestPoint][0];
        verticalDistance = coordinates[highestPoint+1][1] - coordinates[highestPoint][1];
      }

      if (!verticalDistance) // its at 0 degrees
        rotation = 0;
      else if (firstDistance===this.width || Math.abs(horizontalDistance / this.width)) { //(clockwise)
        // cos A = adjacent / hypotenuse
        rotation = Math.abs(Math.acos(verticalDistance / this.width)); // rotation in radians

        if (clockwise)
          rotation = rotation - (Math.PI / 2);
      }
      else {
        // sin A = opposite / hypotenuse
        rotation = Math.abs(Math.asin(horizontalDistance / this.width)); // rotation in radians

        if (clockwise)
          rotation = (Math.PI / 2) + rotation;
        else
          rotation = (Math.PI / 2) - rotation;
      }

      this.rotation = rotation;
    }

    this.loading = false;
  }

  /**
   * Works out if polygon is a rectangle or a square
   */
  getPolygonShape(coordinates): SHAPES {
    debugger; //eslint-disable-line no-debugger
    let uniqueCoordinatesCount = 0;

    // Get number of unique coordinates in shape. Needed because rectangles can have 5 or 6 points.
    // 4 = rectangle
    // >4 = circle
    for (let i=0; i<coordinates.length;i++) {
      let foundDuplicate = false;
      // search for duplicate in previous coordinates
      for (let j=0; j<i;j++) {
        if (coordinates[i][0] === coordinates[j][0] && coordinates[i][1] === coordinates[j][1]) {
          foundDuplicate = true;
          break;
        }
      }
      
      if (!foundDuplicate) {
        uniqueCoordinatesCount += 1;
        
        if (uniqueCoordinatesCount > 4)
          // break if more than 4 as it must be a circle
          break;
      }
    }

    if (uniqueCoordinatesCount===4)
      return this.shapesEnum.RECTANGLE;
    else if (uniqueCoordinatesCount>4)
      return this.shapesEnum.CIRCLE;
    else
      this.notificationHelper.createErrorNotification('Feature of unknown shape.');
  }

  /**
   * Creates new coordinates based on shapes length, size and rotation
   */
  updatePolygonCoordinates() {

    let newPolygon = null;

    if (this.shape===this.shapesEnum.RECTANGLE) {
      const halfLength = this.length / 2;
      const halfWidth = this.width / 2;

      let newCoordinate = [
        [this.featureCenterPoint[0]-halfWidth, this.featureCenterPoint[1]+halfLength],
        [this.featureCenterPoint[0]+halfWidth, this.featureCenterPoint[1]+halfLength],
        [this.featureCenterPoint[0]+halfWidth, this.featureCenterPoint[1]-halfLength],
        [this.featureCenterPoint[0]-halfWidth, this.featureCenterPoint[1]-halfLength],
        [this.featureCenterPoint[0]-halfWidth, this.featureCenterPoint[1]+halfLength]
      ];
      
      newPolygon = new Polygon([newCoordinate]);
      newPolygon.rotate(-this.rotation, this.featureCenterPoint);
    }
    else if (this.shape===this.shapesEnum.CIRCLE) {
      // newPolygon = Polygon.fromCircle(new Circle(this.featureCenterPoint, this.length / 2));
    }
    
    this.componentData.coordinates = newPolygon.getCoordinates()[0];
    this.feature.setGeometry(new MultiPolygon([newPolygon.getCoordinates()]));
  }

  /**
   * Calculate the distance between two points
   */
  distanceBetweenPoints(coord1, coord2) {
    const line = new LineString([coord1, coord2]);
    return Math.round(line.getLength() * 100) / 100;
  }


  /**
   * Saves an edit
   */
  onSubmit() {
    const changedData = this.getChangedData();
    if (this.verified || changedData['grave_number'] === undefined) {
      this.updateGraveDetails(changedData);
    } else {
       this.notificationHelper.createWarningNotification(messages.toolbar.plot.linkGraveRef.verify.title);
    }

    // Geometry Submit
    this.saving = true;

    // Feature might not be exactly right if rotation by RotateFeatureInteraction (it's not as accurate).
    // This makes sure it is correct.
    this.updatePolygonCoordinates();

    //http post to save plot, which send as response a geojson of only that plot
    const oldLayerName = this.feature.get('marker_type');
    const geoJSONFeature = new GeoJSON().writeFeature(this.feature);
  
    let url = null;

    if (this.featureType===this.featureTypesEnum.memorial)
      url = '/mapmanagement/updateMemorial/';
    else if (this.featureType===this.featureTypesEnum.grave)
      url = '/mapmanagement/updatePlot/';

    axios.post(url, {
          'geojsonFeature': geoJSONFeature
    })
    .then(response => {
      let data = response.data;
      let text = "";
      if (data['updated_section'] || data['updated_subsection']) {
        text = this.featureType===this.featureTypesEnum.grave ? "Graveplot's " : "Memorial's ";
        let sectionAndSubsection = data['updated_section'] && data['updated_subsection'];
        
        if (data['updated_section']) 
          text += "section";

        if (sectionAndSubsection)
          text += " and ";
        
        if (data['updated_subsection'])
          text += "subsection";

        if (sectionAndSubsection)
          text += " have";
        else
          text += " has";

        text += " been updated for the new location."
      }

      if (this.featureType===this.featureTypesEnum.grave)
        this.notificationHelper.createSuccessNotification(messages.toolbar.plot.save.success.title, text);
      else if (this.featureType===this.featureTypesEnum.memorial)
        this.notificationHelper.createSuccessNotification(messages.toolbar.memorial.save.success.title, text);
      
      this.originalShape = this.shape;
      this.updateSavedVersion();
      this.appendToOrModifyItemInQuery('edit', null);
    })
    .catch(response => {
      let text = "";
      if (response.data['error_updating_section']) {
        text = "There was an error updating the feature's section and/or subsection:\<br>" + response.data['error_updating_section'];
      }
      this.notificationHelper.createErrorNotification(messages.toolbar.plot.save.fail.title, text);
      
      this.saving = false;
      console.warn('Couldn\'t save feature geometry:', response);
    });
  }

  updateGraveDetails(data) {
    this.saving = true;

    this.notificationHelper.createConfirmation(messages.toolbar.plot.linkGraveRef.save.title, messages.toolbar.plot.linkGraveRef.save.text,  () => {

      axios.patch('/mapmanagement/graveDetails/', data)
      .then(response => {

        // updated saved version
        this.updateSavedVersion();
        this.appendToOrModifyItemInQuery('edit', null);
        this.saving = false;
        this.updateComponentData();
        this.notificationHelper.createSuccessNotification('Grave details saved successfully');

        // if the grave number has been changed
        if (data['grave_number']) {
          axios.get("/mapmanagement/unlinkedBurialsWithTranscribedGraveNumber/" + data['grave_number'] + "/")
        .then(response => {
          if (response.data.graveplot_burial_distinct_list && response.data.graveplot_burial_distinct_list.length) {
            const burialLinks = response.data.graveplot_burial_distinct_list;
            this.linkBurials = burialLinks;
          }
        });
        }
      })
      .catch(response => {
        this.saving = false;
        console.warn('Couldn\'t save grave details:', response);
        this.notificationHelper.createErrorNotification("Couldn't save grave details");
      });
     }, () =>  {
        this.saving = false;
        delete this.componentData.unsavedChanges;
        this.$store.commit('componentHasNoUnsavedChanges', this.componentName);
        this.$store.commit('setCurrentInformation', { componentName: this.componentName, data: this.componentDataSaved });
        this.componentData = this.$store.state.ManagementTool.currentInformation[this.componentName];
     });
  }

  /**
   * Called grave number has changed leading to burials being linked
   */
  updateComponentData() {
    // force list of persons to refresh
    let query = JSON.parse(JSON.stringify(this.$route.query));
    query['refresh'] = true;
    query['edit'] = false
    this.$store.commit('setGraveNumber', this.componentData.grave_number);
    this.$router.replace({params: { id: this.id, layer_type: 'plot'} , query: query });
  }
}
</script>
