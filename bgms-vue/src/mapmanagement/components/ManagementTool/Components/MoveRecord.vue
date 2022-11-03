<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import axios from 'axios'
import { Prop } from 'vue-property-decorator';
import NotificationMixin from '@/mixins/notificationMixin';
import FeatureTools from '@/mapmanagement/mixins/featureTools';
import constants, {FEATURE_TYPES_ENUM} from '@/global-static/constants.ts';

/**
 * Class representing MoveRecord component.
 * Moves burial and person records to another grave or memorial
 * @extends NotificationMixin
 */
@Component({
  render() {
    // i.e. renderless
    return this.$slots.default
  }
})
export default class MoveRecord extends mixins(NotificationMixin, FeatureTools) {

  @Prop()  data;
  
  eventService = this.$store.getters.eventService;
  personInteractionService = this.$store.getters.personInteractionService;
  toolbarService = this.$store.getters.toolbarService;
  addGraveService = this.$store.getters.addGraveService;

  notice;

  plotLayerNames = ['plot', 'available_plot', 'reserved_plot'];

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    let v = this;

    // show notice
    this.notice = this.createPermanentInfoNotification(v.infoNoticeText, 
      true, () => {
        v.$emit('close-tool');
      });
    
    if (!this.data.removeFromOriginal || !this.data.burial_id) {
      // Burial can only be in one grave. Only memorials can be moved without removing original.
      // Also, death records with no burials record cannot be moved to a grave.
      v.plotLayerNames = [];
    }

    // remove current ol events
    v.toolbarService.removeEvents();

    // create event handler for highlighting features on mouseover
    v.eventService.pushEvent({
      group: 'move_record',
      name: 'move_record',
      layerNames: v.plotLayerNames,
      layerGroup: ['memorials'],
      type: 'pointermove',
      handler: v.personInteractionService.selectIconsOnHover
    });

    // create event handler for clicking on feature
    v.eventService.pushEvent({
      group: 'move_record',
      name: 'move-record',
      layerNames: v.plotLayerNames,
      layerGroup: ['memorials'],
      type: 'click',
      handler: (evt, features, layerNames) => {
        if (features[0]) {
          v.featureSelectedOnMap(features[0]);
        }
      }
    });
  }

  /**
   * Vue destroyed lifecycle hook
   */
  destroyed() {
    this.eventService.removeEventsByGroup("move_record");
    this.toolbarService.restoreEvents();
    this.notice.remove();
  }

  /*** Computed ***/

  /**
   * Computed property:
   * @returns {string} 
   */
  get infoNoticeText(): string {
    return `Select a ${this.data.removeFromOriginal ? (this.data.burial_id ? "grave or " : "") + "memorial to move" : "memorial to link"} record to.`;  
  }
  
  /*** Methods ***/

  getConfirmationText(featureType: FEATURE_TYPES_ENUM): string {
    let text = `Are you sure you want to ${this.data.removeFromOriginal ? "move" : "link"} record to this ${featureType}${ featureType==='grave' ? ', including any linked memorials' : '' }${ featureType==='memorial' && this.data.removeFromOriginal && this.data.burial_id ? ', including any linked grave' : '' }?`;

    /*if (this.data.removeFromOriginal) {
      text += `\n\nNote: if record is already linked to a ${featureType}, the original link will be removed.`
    }*/
    return text;
  }

  /**
   * Called when a feature has been selected by the user on the map
   */
  featureSelectedOnMap(feature) {

    // is this feature a grave or a memorial
    let featureType: FEATURE_TYPES_ENUM = this.plotLayerNames.indexOf(feature.getProperties().marker_type) > -1 ? constants.FEATURE_TYPES.grave : constants.FEATURE_TYPES.memorial;

    if (featureType===constants.FEATURE_TYPES.grave) {
      // burial record must be included to link to a grave
      if (!this.data.person_id) {
        this.createErrorNotification("Person cannot be linked to a grave as it is missing a burial record.");
        return;
      }
    }
    else if (featureType===constants.FEATURE_TYPES.memorial) {
      // person record must be included to link to a memorial
      if (!this.data.person_id) {
        this.createErrorNotification("Burial cannot be linked to a memorial as it is missing a person record.");
        return;
      }
    }

    this.createConfirmation(
      `${this.data.removeFromOriginal ? "Move" : "Link"} record`, this.getConfirmationText(featureType),
      () => {
        this.moveToFeature(feature, featureType);
      }
    )
  }

  /**
   * Moves record to given feature
   */
  moveToFeature(feature, featureType: FEATURE_TYPES_ENUM) {

    let v = this;

    let postData = this.data;
    let availablePlot = false;
    let reservedPlot = false;

    // graves have an id and memorials have a feature id
    if (featureType===constants.FEATURE_TYPES.grave) {
      availablePlot = feature.getProperties().marker_type==='available_plot';
      reservedPlot = feature.getProperties().marker_type==='reserved_plot';

      if (availablePlot)
        postData['to_available_plot_id'] = feature.getId();
      else
        postData['to_grave_id'] = feature.getId();
    }
    else if (featureType===constants.FEATURE_TYPES.memorial) {
      postData['to_feature_id'] = feature.getProperties().feature_id;
    }

    axios.post('/mapmanagement/moveBurialPersonRecords/', postData)
    .then(function(response) {
      if (availablePlot && response.data.graveplot_uuid) {
        // change selected available plot to a plot
        v.changeFeatureLayer('available_plot', 'plot', feature.getId(), response.data.graveplot_uuid);
      }
      if (reservedPlot && response.data.graveplot_uuid) {
        // change selected reserved plot to a plot
        v.changeFeatureLayer('reserved_plot', 'plot', feature.getId(), response.data.graveplot_uuid);
      }
      if(response.data.layer) {
        // change current plot to an available plot if it has no more burials
        if(response.data.layer==='available_plot') {
          v.changeFeatureLayer('plot', 'available_plot', postData.from_graveplot_uuid, response.data.topopolygon_id)
        }
        else if(response.data.layer==='reserved_plot') {
          v.changeFeatureLayer('plot', 'reserved_plot', postData.from_graveplot_uuid, postData.from_graveplot_uuid)
        }
      }

      v.createSuccessNotification(`${v.data.removeFromOriginal ? "Move" : "Link"} was successful`);
      v.$emit('close-tool', response.data);
    })
    .catch(function(response) {
      v.createErrorNotification(`${v.data.removeFromOriginal ? "Move" : "Link"} failed`);
      console.warn(`${v.data.removeFromOriginal ? "Move" : "Link"} failed: ${response}\n${response.response.data}`);
    });
  }
}
</script>