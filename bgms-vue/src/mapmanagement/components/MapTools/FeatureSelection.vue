<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import axios from 'axios'
import { Prop, Watch } from 'vue-property-decorator';
import NotificationMixin from '@/mixins/notificationMixin';
import FeatureTools from '@/mapmanagement/mixins/featureTools';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import Text from 'ol/style/Text';
import constants from '@/global-static/constants.ts';

/**
 * Class representing FeatureSelection component.
 * Moves burial and person records to another grave or memorial
 * @extends NotificationMixin
 */
@Component({
  render() {
    // i.e. renderless
    return this.$slots.default
  }
})
export default class FeatureSelection extends mixins(NotificationMixin, FeatureTools) {

  @Prop() selectionLayer;

  eventService = this.$store.getters.eventService;
  toolbarService = this.$store.getters.toolbarService;
  addGraveService = this.$store.getters.addGraveService;
  memorialService = this.$store.getters.memorialService;

  notice;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    let v = this;

    let horizontalToolsAccordion = document.getElementById('horizontalToolsAccordion');
    if (horizontalToolsAccordion)
      horizontalToolsAccordion.style.display = "none";

    let layersToolbarContainer = document.getElementById('layersToolbarContainer');
    if (layersToolbarContainer)
      layersToolbarContainer.style.display = "none";

    v.featureLabels(true);

    // show permanent notice with close button
    v.notice = v.createPermanentInfoNotification(`Select a ${v.selectionLayer.display_name}.`, true, 
      () => {
        v.$emit('close-tool');
      }, 'Stop'
    );

    // remove current ol events
    v.toolbarService.removeEvents();

    // create event handler for highlighting features on mouseover
    v.eventService.pushEvent({
      group: 'feature_management',
      name: 'feature_management_hover',
      layerNames: [v.selectionLayer.name],
      type: 'pointermove',
      handler: v.featureManagementHover
    });

    // create event handler for clicking on feature
    v.eventService.pushEvent({
      group: 'feature_management',
      name: 'feature_management_click',
      layerNames: [v.selectionLayer.name],
      type: 'click',
      handler: v.featureClickHandler
    });
  }

  /**
   * Vue destroyed lifecycle hook
   */
  destroyed() {
    this.eventService.removeEventsByGroup("feature_management");
    this.toolbarService.restoreEvents();
    this.notice.remove();
    
    this.featureLabels(false);

    let horizontalToolsAccordion = document.getElementById('horizontalToolsAccordion');
    if (horizontalToolsAccordion)
      horizontalToolsAccordion.style.display = "inline-flex";

    let layersToolbarContainer = document.getElementById('layersToolbarContainer');
    if (layersToolbarContainer)
      layersToolbarContainer.style.display = "block";
  }

  /*** Computed ***/
  get managementToolOpenedClosed() {
    return this.$store.state.ManagementTool.managementToolOpen;
  }

  /*** Watchers ***/
  /**
   * Watcher: When the management tool is closed, close this tool
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('managementToolOpenedClosed')
  onManagementToolOpenedClosed(val: any, oldVal: any) {
    if (!val) {
      this.$emit('close-tool');
    }
  }
  
  /*** Methods ***/

  /**
   * Event when hovering over a feature
   */
  featureManagementHover(evt, features) {
    let feature = features[0];

    // show pointer while hovering over a feature
    if (feature) {
      this.togglePointerOverFeature(evt.map, true);
        
      this.highlightFeatures('feature_management', 'feature_management_' + this.selectionLayer.name, [{ featureID: feature.getId(), layerName: feature.values_.marker_type }], this.$store.state.MapLayers.layerStyles.selectedStyleFunction, this.selectionLayer.name);
    }
    else {
      this.togglePointerOverFeature(evt.map, false);
      this.highlightFeatures('feature_management', 'feature_management_' + this.selectionLayer.name);
    }
    
  }

  /**
   * Called when a feature has been selected by the user on the map
   */
  featureClickHandler(evt, features) {
    if (features[0]) {
      const route = this.selectionLayer.attributes_exist ? 'attributes' : null;//constants.FEATURE_MANAGEMENT_CHILD_ROUTES.surveys;
      this.featureSelected({ featureID: features[0].getId(), layerName: features[0].values_.marker_type }, route);
    }
  }

  featureLabels(showLabels: boolean) {
    let styleLayer;
    let layerName = this.selectionLayer.name;

    // Get all the features in the layer
    let features = null;
    const layers = (window as any).OLMap.getLayers().getArray();

    for (let i in layers) {
      if(layers[i].get('name') === layerName) {
        features = layers[i].getSource().getFeatures();
        break;
      }
    }
    
    const textColor = 'black';

    for (var j = 0; j < features.length; j++) {

      let feature = features[j];
      let id = features[j].get('id');

      if(showLabels && feature.get('label')) {
        if (typeof this.$store.state.MapLayers.layerStyles[layerName] === "function") {
          styleLayer = this.$store.state.MapLayers.layerStyles[layerName](feature)[0];
        } else {
          styleLayer = this.$store.state.MapLayers.layerStyles['default'](feature)[0];
        }

        // Add label to style if label exists
        const text = feature.get('label');

        let textStyle = new Text({
          text: text,
          font: '900 13px Verdana',
          fill: new Fill({
            color: textColor,
          }),
          stroke: new Stroke({
            color: 'white',
            width: 3,
          }),
          overflow: true
        });

        styleLayer.setText(textStyle);

        this.highlightFeatures('feature_labels', 'feature_labels_' + feature.getId(), [{ featureID: feature.getId(), layerName: feature.values_.marker_type }], styleLayer, this.selectionLayer.name);
      }
      else if (!showLabels)
        this.highlightFeatures('feature_labels', 'feature_labels_' + feature.getId());
    }
  }
}
</script>