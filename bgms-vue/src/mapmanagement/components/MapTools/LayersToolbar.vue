<template>
  <div id="layersAccordion" class="layers-right-button">
    <button class="btn btn-bgms btn-right-toolbar" aria-label="Left Align" data-toggle="collapse" title="Map Layers" data-parent="#layersAccordion" href="#collapseLayers" @click="togglePanelLayers('#collapseLayers')" :disabled="!(displayGroups && Object.keys(displayGroups).length > 0)">
      <span class="icon-Map-Layers-Outline" aria-hidden="true"></span>
      <span class="icon-Map-Layers-Filled" aria-hidden="true"></span>
    </button>

    <div id="collapseLayers" class="panel-collapse collapse" v-if="displayGroups && Object.keys(displayGroups).length > 0">
      <div id="collapseLayersBody" class="panel-body narrow-body">
        <div class="row layer-buttons" v-if="aerialLayerInUse || plansLayerInUse">
          <div :class="[{'col-xs-4': aerialLayerInUse, 'col-xs-6': !aerialLayerInUse}]" v-if="plansLayerInUse">
            <label class="btn btn-bgms-layer plans" :class="{ active : selectedBaseLayer===baseLayersEnum.PLANS }">
              <input type="checkbox" v-model="displayGroups.plans.layerGroup.visible" @change="toggleLayerButton(baseLayersEnum.PLANS)" hidden> {{displayGroups.plans.layerGroup.display_name || 'Plans'}}
            </label>
          </div>
          <div :class="{'col-xs-4': plansLayerInUse, 'col-xs-6': !plansLayerInUse}" v-if="aerialLayerInUse">
            <label class="btn btn-bgms-layer aerial" :class="[{ active : selectedBaseLayer===baseLayersEnum.AERIAL }, $store.state.MapLayers.disableClass]">
              <input type="checkbox" v-model="displayGroups.aerial.layerGroup.visible" @change="toggleLayerButton(baseLayersEnum.AERIAL)" :disabled="$store.state.MapLayers.disableAerial" hidden> {{displayGroups.aerial.layerGroup.display_name || 'Aerial'}}
            </label>
          </div>
          <div :class="{'col-xs-4': (aerialLayerInUse && plansLayerInUse), 'col-xs-6': !(aerialLayerInUse && plansLayerInUse)}">
            <!-- class: active for default button selected -->
            <label class="btn btn-bgms-layer base" :class="{ active : selectedBaseLayer===baseLayersEnum.BASE }">
              <input type="checkbox" v-model="displayGroups.base.layerGroup.visible" @change="toggleLayerButton(baseLayersEnum.BASE);realClikBase()" hidden> {{displayGroups.base.layerGroup.display_name}}
            </label>
          </div>
        </div>

        <div id='scrollUpLayers' hidden>
          <button class="btn btn-bgms-scroll" @mouseover="scrollUp()" @mouseleave="stopScroll()">
            <span class="glyphicon glyphicon-chevron-up" style="vertical-align:middle"></span>
          </button>
        </div>

        <div class="collapse-menu-layers">
          <div id="collapseLayersInner" class="row">
            <div class="panel-group" id="accordion">
              <div class="collapse-menu-layers">
                <!--Layer groups ordered by hierarchy -->
                <div v-for="displayGroup in getFilteredAndSortedLayerGroups()" :key="displayGroup.layerGroup.name">
                  <div class="panel panel-default" :id="displayGroup.layerGroup.name" :style="displayGroup.isPanelDisplayed?{}:{'display': 'None'}">
                    <div class="panel-heading narrow-heading" role="tab" :id="displayGroup.layerGroup.name + 'heading'">
                      <h4 class="panel-title">
                        <div class="row">
                          <div class="col-xs-4">
                            <div class="slideThree" @click="displayGroup.layerGroup.visibility = !displayGroup.layerGroup.visibility; displayGroup.visibility=!displayGroup.visibility; visibilityToggle(displayGroup.layerGroup.name + '_group_id', displayGroup.layerGroup.visibility)" v-show="displayGroup.layerGroup.switch_on_off">
                              <input :ref="displayGroup.layerGroup.name + '_group_id'" :id="displayGroup.layerGroup.name + '_group_id'" type="checkbox" :checked="displayGroup.layerGroup.visibility" hidden>
                              <label :for="displayGroup.layerGroup.name + '_group_id'" @click.stop></label>
                            </div>
                          </div>
                          <div class="col-xs-8">
                            <a class="collapsed" data-toggle="collapse" data-parent="#accordion" :href="'#' + displayGroup.layerGroup.name + 'collapse'" aria-expanded="false" :aria-controls="displayGroup.layerGroup.name + 'collapse'" @click="togglePanel()">
                              {{displayGroup.layerGroup.display_name}}
                            </a>
                          </div>
                        </div>
                      </h4>
                    </div>
                    <div :id="displayGroup.layerGroup.name + 'collapse'" class="panel-collapse collapse in" role="tabpanel" :aria-labelledby="displayGroup.layerGroup.name + 'heading'">
                      <div class="panel-body narrow-body subgroup-layer">

                        <!-- MapLayers -->
                        <div v-for="displayLayer in displayGroup.layerGroup.layers" :key="displayLayer.name">
                          <div class="row" v-if="displayLayer.show_in_toolbar">
                            <div class="col-xs-1 no-padding">
                              <div class="roundedOne">
                                <input :id="displayLayer.name + '_id'" type="checkbox" :checked="displayLayer.visible" @change="displayLayer.visibility = !displayLayer.visibility;" hidden>
                                <label :for="displayLayer.name + '_id'" v-show="displayLayer.switch_on_off" title="Visibility"/>
                              </div>
                            </div>
                            <div class="col-xs-1 no-padding">
                              <div class="layerButton">
                                <label class="btn btn-bgms" :title="isOnline? 'Feature Management' : 'Feature Management: disabled while offline'" :class="{ active: selectedLayer===displayLayer }" v-show="displayLayer.attributes_exist || displayLayer.surveys_exist" @click="openFeatureManagement(displayLayer)" :disabled="!isOnline">
                                  <span class="fa fa-info"></span>
                                </label>
                              </div>
                            </div>
                            <div class="col-xs-4">
                              <div :class="'key '+displayLayer.name+'_key'"></div>
                            </div>
                            <div class="col-xs-6">
                              {{displayLayer.display_name}}
                            </div>
                          </div>
                        </div>

                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
            <div id='scrollDownLayers' hidden>
            <button class="btn btn-bgms-scroll" @mouseover="scrollDown()" @mouseleave="stopScroll()">
              <span class="glyphicon glyphicon-chevron-down" style="vertical-align:middle"></span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <FeatureSelection v-if="selectedLayer" :selectionLayer="selectedLayer" :key="selectedLayer.name" @close-tool="closeFeatureAttributes"/>

  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import VueRouter from 'vue-router';
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'

Vue.use(Vuex);
Vue.use(VueRouter);

enum BASE_LAYERS { PLANS, AERIAL, BASE }

/**
 * The layer toolbar controls the visibility of LayerGroup and Layer objects in layers.
 * @extends Vue
 */
@Component({
  components: {
    FeatureSelection: () => import('@/mapmanagement/components/MapTools/FeatureSelection.vue')
  }
})
export default class LayersToolbar extends Vue {

  layerGenerator = this.$store.getters.layerGenerator;
  mapService = this.$store.getters.mapService;

  accordionTools = {
    collapseTools: false,
    layers: false
  };

  amountToScroll = '';

  selectedLayer = null;
  selectedOriginalVisibility = null;
  unwatchLayerGenerated = null;

  baseLayersEnum = BASE_LAYERS;
  selectedBaseLayer: BASE_LAYERS = this.baseLayersEnum.BASE;

  /**
   * Set up jquery events to communicate with AngularJS (temp)
   */
  mounted() {
    // Checking if it should only show the available plots
    // based on the query parameter
    const filterAvailablePlots = this.$router.currentRoute.query.filterAvailablePlots;
    if(filterAvailablePlots) {
        const layers = this.getFilteredAndSortedLayerGroups();
        // take the plot group layer
        const plotLayer = layers.find(({ layerGroup }) => layerGroup.display_name === "Plot");
        if(plotLayer) {
            // disabling all plot-type layers, except available plots
            const { displayedLayers, layerGroup } = plotLayer;
            Object.keys(displayedLayers).forEach((plotGroupName) => {
                if(plotGroupName !== "available_plot") {
                    const layer = layerGroup.layers[plotGroupName];
                    if(layer) layer.visibility = false;
                }
            });
            
        }
    }

    (window as any).jQuery(window).on("resize.doResize", () => {
      // alert(window.innerWidth);
      this.addScrollBarToLayersSide();
      this.resizeMap();
    });

    (window as any).jQuery(document).on('triggerToggleLayerButtonBase', this.triggerToggleLayerButtonBase);
    (window as any).jQuery(document).on('triggerToggleLayerButtonAerial', this.triggerToggleLayerButtonAerial);
  }

  destroyed() {
    // remove handlers added earlier
    (window as any).jQuery(window).off("resize.doResize");
    (window as any).jQuery(window).off("triggerToggleLayerButtonBase");
    (window as any).jQuery(window).off("triggerToggleLayerButtonAerial");
  }

  /*** Computed ***/

  get displayGroups() {
    return this.$store.state.MapLayers.displayGroups;
  }

  /**
   * @returns True if this site has an aerial layer
   */
  get aerialLayerInUse(): boolean {
    return this.$store.state.MapLayers.aerialLayer && this.displayGroups.aerial;
  }

  /**
   * @returns True if this site has a plans layer
   */
  get plansLayerInUse(): boolean {
    return this.$store.state.MapLayers.plansLayer && this.displayGroups.plans;
  }
  
  get isOnline(): boolean {
    return this.$store.state.Offline.online;
  }

  /*** Methods ***/

  /**
   * Toggle layer buttons (Aerial, Map)
   * @param {BASE_LAYERS} option [represents the button pressed]
   */
  toggleLayerButton(option: BASE_LAYERS){
    switch (option) {
      case this.baseLayersEnum.AERIAL: {
        if(!this.displayGroups.aerial.layerGroup.visibility){
          this.showAerialPlansLayers();
          if(this.displayGroups.memorial_cluster)
            this.displayGroups.memorial_cluster.isPanelDisplayed = false;
          this.toggleLayerButtonUpdateUI(option, this.displayGroups.aerial.layerGroup.visibility, this.displayGroups);
          this.displayGroups.aerial.layerGroup.visibility = !this.displayGroups.aerial.layerGroup.visibility;
          this.$store.commit('setWasAerialVisible', true);
          
          if (this.displayGroups.plans && this.displayGroups.plans.layerGroup.visibility)
            this.displayGroups.plans.layerGroup.visibility = false;
        }
      break;
      }
      case this.baseLayersEnum.PLANS: {
        if(!this.displayGroups.plans.layerGroup.visibility){
          this.showAerialPlansLayers();
          if(this.displayGroups.memorial_cluster)
            this.displayGroups.memorial_cluster.isPanelDisplayed = false;
          this.toggleLayerButtonUpdateUI(option, this.displayGroups.plans.layerGroup.visibility, this.displayGroups);
          this.displayGroups.plans.layerGroup.visibility = !this.displayGroups.plans.layerGroup.visibility;
          this.$store.commit('setWasAerialVisible', false);

          if (this.displayGroups.aerial && this.displayGroups.aerial.layerGroup.visibility)
            this.displayGroups.aerial.layerGroup.visibility = false;
        }
      break;
      }
      case this.baseLayersEnum.BASE: {
        let isactive = this.selectedBaseLayer===option;
        if(!isactive){
          this.showMapLayers();
          if (this.displayGroups.aerial && this.displayGroups.aerial.layerGroup.visibility)
            this.displayGroups.aerial.layerGroup.visibility = false;
          if (this.displayGroups.plans && this.displayGroups.plans.layerGroup.visibility)
            this.displayGroups.plans.layerGroup.visibility = false;
        }

        if(this.displayGroups.memorial_cluster)
          this.displayGroups.memorial_cluster.isPanelDisplayed = false;

        this.toggleLayerButtonUpdateUI(option, isactive, this.displayGroups);

        break;
      }
      default: {
        break;
      }
    }
    this.addScrollBarToLayersSide();
  }

  toggleLayerButtonUpdateUI(option: BASE_LAYERS, visibility, layersGroups) {
    if(!visibility)
      this.selectedBaseLayer = option;

    //Hide Aerial groups and show Map groups
    //ac: needs to be done in addition to setting display as none
    for (let key in layersGroups) {
      if(!layersGroups[key].isPanelDisplayed)
        (window as any).jQuery("#"+key).hide();
      else
        (window as any).jQuery("#"+key).show();
    }
  }

  /**
   * Show Aerial layers in toolbar, when aerial is shown
   * @param none
   */
  showAerialPlansLayers() {
    let temp = this.displayGroups;
    for (let key in this.displayGroups) {
      let displayGroup = this.displayGroups[key];
      if(displayGroup.layerGroup.name!='aerial' && displayGroup.layerGroup.name!='memorials' && displayGroup.layerGroup.name!='memorial_cluster' && displayGroup.layerGroup.name!='plots' && displayGroup.layerGroup.name!='base'){
        // remember current visibilities of layers for each group we hide
        for (let name in displayGroup.layerGroup.layers) {
          displayGroup.displayedLayers[name] = displayGroup.layerGroup.layers[name].visibility;
        }
        //turn off vegetation group layers so its not visible in Aerial mode only in Map vector mode:
        //  reason: vegetation on top of memorials
        //          memorials on top of aerial
        //therefore: vegetation on top aerial
        if(displayGroup.layerGroup.name=='vegetation')
          displayGroup.layerGroup.visibility = false;

        displayGroup.isPanelDisplayed = false;
      }
      else {
        displayGroup.isPanelDisplayed = true;
      }
    }
  }

  /**
   * Show Map vector layers in toolbar, when aerial imagery is hidden
   * @param none
   */
  showMapLayers(){
    for (let key in this.displayGroups) {
      let displayGroup = this.displayGroups[key];
      if(displayGroup.layerGroup.name!='aerial'){
        //use remembered visibilities to display layers
        if(displayGroup.layerGroup.name!='memorials' && displayGroup.layerGroup.name!='memorial_cluster'  && displayGroup.layerGroup.name!='plots' && displayGroup.layerGroup.name!='base')
          for (let name in displayGroup.layerGroup.layers) {
            displayGroup.displayedLayers[name] = displayGroup.layerGroup.layers[name].visibility;
          }
        displayGroup.isPanelDisplayed = true;
      } 
      else
        displayGroup.isPanelDisplayed = false;
    }
  }

  realClikBase() {
    this.$store.commit('setWasAerialVisible', false); //only when click the button
  }

  //Simulate clicks for map and aerial buttons. They are triggered when the extra zoom level is reached
  triggerToggleLayerButtonBase(event) {
    if(this.displayGroups.aerial){
        this.toggleLayerButton(this.baseLayersEnum.BASE);
    }
  }
  triggerToggleLayerButtonAerial(event) {
    if(this.displayGroups.aerial){
        this.toggleLayerButton(this.baseLayersEnum.AERIAL);
    }
  }

  togglePanel() {
    this.addScrollBarToLayersSide();
  }

  togglePanelLayers(panel) {
    if(this.accordionTools.layers){
      this.accordionTools.layers = false;
    }
    else{
      this.accordionTools.layers = true;
    }

    this.relocateParentAccordion();
  }

  relocateParentAccordion() {
    if(this.accordionTools.layers == false && this.accordionTools.collapseTools == false){
      (window as any).jQuery('#parentAccordion').css({ 'width' : '45px'});
      (window as any).jQuery('.panel-heading.narrow-heading.icons-right').css({ 'margin-left' : '0%'});
      (window as any).jQuery('#scrollDownLayers').hide();
    }
    else{
      (window as any).jQuery('#parentAccordion').css({ 'width' : '250px'});
      (window as any).jQuery('.panel-heading.narrow-heading.icons-right').css({ 'margin-left' : '80%'});

      window.setTimeout(() => {
        this.addScrollBarToLayersSide();
      });
    }
  }

  addScrollBarToLayersSide() {
    if((window as any).jQuery('#accordion').innerHeight() > window.innerHeight-265){
      (window as any).jQuery('#collapseLayersInner').css({'height':(window.innerHeight-265)+'px'});
      (window as any).jQuery('#scrollDownLayers').show();
      (window as any).jQuery('#scrollUpLayers').show();
    }
    else{
      (window as any).jQuery('#collapseLayersInner').css({'height': 'auto'});
      (window as any).jQuery('#scrollDownLayers').hide();
      (window as any).jQuery('#scrollUpLayers').hide();
    }
  }

  scrollUp() {
    this.amountToScroll = '-=10';
    this.scroll();
  }

  scrollDown() {
    this.amountToScroll = '+=10';
    this.scroll();
  }

  stopScroll() {
    this.amountToScroll = '';
  }

  scroll() {
    let v = this;

    (window as any).jQuery('#collapseLayersInner').animate({
        scrollTop: v.amountToScroll
      }, 100, 'linear',() => {
        if (v.amountToScroll != '') {
          v.scroll();
        }
      });
  }

  openFeatureManagement(displayLayer) {
    this.selectedLayer = this.selectedLayer!==displayLayer ? displayLayer : null;
    this.selectedOriginalVisibility = displayLayer.visibility;
    displayLayer.visibility = true;
  }

  closeFeatureAttributes(displayLayer) {
    this.selectedLayer.visibility = this.selectedOriginalVisibility;
    this.selectedLayer=null;
  }

  /**
   * @returns array containing filtered layer groups, sorted by hierarchy
   */
  getFilteredAndSortedLayerGroups(): any[] {
    let result = [];
    Object.keys(this.displayGroups).forEach(key => {
      if (key != 'base' && key != 'aerial' && key != 'plans') {
        result.push(this.displayGroups[key]);
      }
    });

    result.sort((a, b) => b.layerGroup.hierarchy - a.layerGroup.hierarchy);

    // Checking if it should only show the available plots
    // based on the query parameter
    const filterAvailablePlots = this.$router.currentRoute.query.filterAvailablePlots;
    if (filterAvailablePlots) {
      const layers = result;
      // take the plot group layer
      const plotLayer = layers.find(
        ({ layerGroup }) => layerGroup.display_name === "Plot"
      );

      if (plotLayer) {
        // disabling all plot-type layers, except available plots
        const { displayedLayers, layerGroup } = plotLayer;
        Object.keys(displayedLayers).forEach((plotGroupName) => {
          if (plotGroupName !== "available_plot") {
            const layer = layerGroup.layers[plotGroupName];
            if (layer) layer.visibility = false;
          }
        });
      }
    }

    return result;
  }

  resizeMap() {
    //Set size of the map according to the size of the screen
    (window as any).OLMap.setSize([window.innerWidth, window.innerHeight - (window as any).jQuery('header').height() - 2]);
    (window as any).OLMap.updateSize();
  }

  visibilityToggle(ref, checked) {
    this.$refs[ref][0].checked = checked;
  }
}
</script>