<template>
  <div :id="componentName" v-if="componentData && !loadingDetails">
    <ScrollButtons :heightChangedFlag="heightChangedFlag">
      <form class="form-horizontal form-box-inside management-tool-form" action="" @submit.prevent="onSubmit">
        
        <FormButtons v-if="siteAdminOrSiteWarden" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="true" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>

        <div class="blank-form-placeholder" v-if="!(editFlag || componentData.feature_id || componentData.user_generated || componentData.inscription || componentData.description)">No memorial details recorded.</div>
        <div v-else>  
          <section>
            <SelectInputRow label="Memorial type" v-model="componentData.feature_type" :editFlag="editFlag" :options="memorialLayers" :optionValueName="'layer_code'" :optionKeyName="'layer_id'" :optionLabelName="'display_name'"/>
          </section>

          <StandardInputRow :label="'Inscription'" v-model="componentData.inscription" :inputType="'textarea'" :attributes="{ maxlength:400 }" :editFlag="editFlag"/>
          <StandardInputRow :label="'Description'" v-model="componentData.description" :inputType="'textarea'" :attributes="{ maxlength:300 }" :editFlag="editFlag"/>
        
          <h2> Geometry </h2>        
          <SelectInputRow v-if="featureType && featureType===featureTypesEnum.memorial" label="Shape" v-model="shape" :editFlag="editFlag" :options="[{value:shapesEnum.CIRCLE},{value:shapesEnum.RECTANGLE}]" :optionValueName="'value'" :optionKeyName="'value'" :optionLabelName="'value'"/>

          <StandardInputRow v-if="shape===shapesEnum.CIRCLE" :label="'Diameter'" :editFlag="editFlag" :readonlyOption="true" v-model.number="length" :inputType="'number'" :attributes="{ step:0.01, min:0.01, max:5 }" :unit="' m'"/>

          <StandardInputRow v-if="shape===shapesEnum.RECTANGLE" :label="'Length'" :editFlag="editFlag" :readonlyOption="true" v-model.number="length" :inputType="'number'" :attributes="{ step:0.01, min:0.01, max:5 }" :unit="' m'"/>

          <StandardInputRow v-if="shape===shapesEnum.RECTANGLE" :label="'Width'" :editFlag="editFlag" :readonlyOption="true" v-model.number="width" :inputType="'number'" :attributes="{ step:0.01, min:0.01, max:5 }" :unit="' m'"/>

          <StandardInputRow v-if="shape===shapesEnum.RECTANGLE" :label="'Rotation'" :editFlag="editFlag" :readonlyOption="true" v-model.number="roundedRotation" :inputType="'number'" :attributes="{ step:0.1 }" showFalsyValue="true" :unit="'°'"/>

          <section>

            <StandardInputRow :label="'Feature ID'" v-model="componentData.feature_id" :editFlag="false" :readonlyOption="true"/>
            <StandardInputRow :label="'User generated'" :value="componentData.user_generated ? 'Yes' : 'No'" :editFlag="false" :readonlyOption="true"/>
            <div>
              <div class="row field-row">
                <label for="feature-id" class="col-xs-4 control-label" style="font-weight:200;">Feature ID:</label>
                <div id="feature-id" class="col-xs-8 no-padding">
                  <input placeholder="Feature ID" class="form-control" style="color:#828282;" :value="componentData.feature_id"><!---->
                </div>
              </div>
            </div>
            <div>
              <div class="row field-row pb-1">
                <label for="user-generated" class="col-xs-4 control-label" style="font-weight:200;">User generated:</label>
                <div id="user-generated" class="col-xs-8 no-padding">
                  <input :value="componentData.user_generated ? 'Yes' : 'No'" style="color:#828282;" placeholder="User generated" class="form-control"><!---->
                </div>
              </div>
            </div>
          </section>

        </div>

      
      <FormButtons v-if="siteAdminOrSiteWarden" :editFlag="editFlag" :saving="saving" :fieldChanged="fieldChanged" :showEdit="true" @toggle-edit="appendToOrModifyItemInQuery('edit', $event)"/>
      </form>

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
import Component, { mixins } from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator';
import axios from 'axios'
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin'
import StandardInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/StandardInputRow.vue';
import FormButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/FormButtons.vue';
import ScrollButtons from '@/mapmanagement/components/ManagementTool/FormHelperComponents/ScrollButtons.vue';
import SelectInputRow from '@/mapmanagement/components/ManagementTool/FormHelperComponents/SelectInputRow.vue';
import FeatureTools from '@/mapmanagement/mixins/featureTools';
import { getCenter } from 'ol/extent';
import LineString from 'ol/geom/LineString';
import Circle from 'ol/geom/Circle';
import Polygon from 'ol/geom/Polygon';
import MultiPolygon from 'ol/geom/MultiPolygon';
import GeoJSON from 'ol/format/GeoJSON';
import { messages } from '@/global-static/messages.js';
import constants, {FEATURE_TYPES_ENUM} from '@/global-static/constants';

enum SHAPES { CIRCLE="CIRCLE", RECTANGLE="RECTANGLE" }

/**
 * Class representing MemorialDetails component
 * @extends mixins: ManagementToolsMixin
 */
@Component({
  components: {
    FormButtons,
    StandardInputRow,
    ScrollButtons,
    SelectInputRow
  }
})
export default class MemorialDetails extends mixins(ManagementToolsMixin, FeatureTools){

  @Prop() id;
  @Prop() layer;

  editFlag: boolean = false;
  saving: boolean = false;
  loadingDetails: boolean = false;

  geometryHelperService = this.$store.getters.geometryHelperService;
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
  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    this.editableFields = ['feature_id', 'description', 'user_generated', 'inscription', 'feature_type', 'coordinates'];
    this.componentName = "memorial_details";
    this._id = this.id;

    if (!this.$store.state.memorialLayers) {
      this.loadingDetails = true;

      // Get the memorial layers from server
      this.$store.dispatch('populateMemorialLayers')
      .finally(() => {
        this.loadingDetails = false;
      });
    }


    let featureID = this.id;
    if (this.layer==='available_plot') {
      featureID = this.$route.params.availablePlotID;
    }
    
    this.getFeatureFromLayer(featureID, this.layer)
    .then(value => {
      this.feature = value;
      
      // get coordinates and store
      const geometry = this.feature.getGeometry();
      const coordinates = geometry.getCoordinates()[0][0];
      // this.storeData({ coordinates: coordinates });
      // load data
      this.loadData('/mapmanagement/memorialDetails/?memorial_uuid=', this._id, {coordinates:coordinates});  

      this.originalShape = this.shape = this.getPolygonShape(coordinates);
      
      this.calculatePolygonGeometry();
    });

    if (this.isRouteActive(constants.MEMORIAL_MANAGEMENT_PATH))
      this.featureType = this.featureTypesEnum.memorial;
    else if (this.isRouteActive(constants.GRAVE_MANAGEMENT_PATH))
      this.featureType = this.featureTypesEnum.grave;
    


  }

  destroyed() {
    if (this.editFlag) {
      this.feature.getGeometry().setCoordinates([[this.componentDataSaved.coordinates]]);
      this.geometryHelperService.stopRotateFeature();
    }
  }

  /*** Computed ***/

  /**
   * Computed property: Get the available memorial layers
   * @returns {any} memorial layers
   */
  get memorialLayers() {
    return this.$store.state.memorialLayers;
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
    if (this.loadingDetails || !val || oldVal===-10)
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
    if (this.loadingDetails || !val || oldVal===-10)
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
    if (this.loadingDetails || !val || oldVal===-10)
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
        this.feature.getGeometry().setCoordinates([[this.componentDataSaved.coordinates]]);
        
        this.loadingDetails = true;
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

    this.loadingDetails = true;
    let coordinates;
    if (this.componentData){
       coordinates = this.componentData.coordinates;
    }
    else{
       coordinates = this.feature.getGeometry().getCoordinates()[0][0];
    }
    
    
    // get center point of feature
    const geometry = this.feature.getGeometry();
    this.featureCenterPoint = getCenter(geometry.getExtent());

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

    this.loadingDetails = false;
  }

  /**
   * Works out if polygon is a rectangle or a square
   */
  getPolygonShape(coordinates): SHAPES {
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
      //newPolygon = Polygon.fromCircle(new Circle(this.featureCenterPoint, this.length / 2));
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
    this.saving = true;

    let data = this.getChangedData();

    axios.patch('/mapmanagement/memorialDetails/', data)
      .then((response) => {
        // updated saved version
        this.updateSavedVersion();
        this.appendToOrModifyItemInQuery('edit', null);
        this.saving = false;
        this.notificationHelper.createSuccessNotification('Memorial details saved successfully');

        if (data['feature_type']) {
          // update memorial's layer on map
          this.changeFeatureLayer(this.layer, data['feature_type'], this.id)
          .then(() => {
            // update layer param
            this.$router.replace({ name: this.$route.name, params: { layer: data['feature_type'] }, query: { refresh: 'true' } });
          });
        }
      })
      .catch((response) => {
        this.saving = false;
        console.warn('Couldn\'t save memorial details:', response);
        this.notificationHelper.createErrorNotification("Couldn't save memorial details");
      });

  // Saving the Geometry Form

  // Feature might not be exactly right if rotation by RotateFeatureInteraction (it's not as accurate).
    // This makes sure it is correct.
    this.updatePolygonCoordinates();

    //http post to save plot, which send as response a geojson of only that plot
    const oldLayerName = this.feature.get('marker_type');

    // save updated memorial type name
    this.feature.set('marker_type',`${data['feature_type']}`);

    const geoJSONFeature = new GeoJSON().writeFeature(this.feature);
  
    let url = null;

    if (this.featureType===this.featureTypesEnum.memorial)
      url = '/mapmanagement/updateMemorial/';
    else if (this.featureType===this.featureTypesEnum.grave)
      url = '/mapmanagement/updatePlot/';

    axios.post(url, {
          'geojsonFeature': geoJSONFeature,
          'oldlayerName':oldLayerName
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
}
</script>
