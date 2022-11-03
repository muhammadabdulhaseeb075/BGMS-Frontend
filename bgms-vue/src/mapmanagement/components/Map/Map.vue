<template>
  <div>
    <div id="map" class="map-test-class" ref="map" @click="mapClicked"></div>
    <div :key="key">
      <div v-for="marker in markers" :id="marker.id" :key="marker.index" class="resize-class">
        <div v-show="marker.message" :class="marker.class" v-html="marker.message"></div>
        <component v-if="marker.template" :is="marker.template.component" :scope="marker.template.scope"></component>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import axios from 'axios';
import proj4 from 'proj4'
import {defaults as defaultControls, ScaleLine, MousePosition, Attribution} from 'ol/control';
import {default as OLMap} from 'ol/Map';
import View from 'ol/View';
import {register} from 'ol/proj/proj4'
import { get as getProj } from 'ol/proj'
import TileLayer from 'ol/layer/Tile';
import WMTS from 'ol/source/WMTS';
import WMTSTileGrid from 'ol/tilegrid/WMTS';
import 'ol/ol.css';
import { getLayerFromMap } from '@/mapmanagement/components/Map/models/Layer';
import BasicDetailsMarker from '@/mapmanagement/components/Map/Markers/BasicDetailsMarker.vue';
import DisplayNameMarker from '@/mapmanagement/components/Map/Markers/DisplayNameMarker.vue';

proj4.defs("EPSG:27700", "+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy +towgs84=446.448,-125.157,542.06,0.15,0.247,0.842,-20.489 +units=m +no_defs");
register(proj4);
let projection = getProj('EPSG:27700');
projection.setExtent([1393.0196, 13494.9764, 671196.3657, 1230275.0454]);


const MEMORIALSOURCEURL = '/mapmanagement/getMemorialLayers/?layer=';

class LayerCounter {
  
  numLayers = null;
  layerNames = null;
  callback = null;

  constructor(layerNames, callback) {
    this.layerNames = layerNames;
    this.callback = callback;
  }

  counter() {
    if (!this.numLayers)
      this.numLayers = this.layerNames.number_of_layers;
    this.numLayers--;
    if (this.numLayers === 0) {
      this.postLayersLoaded();
    }
  }

  postLayersLoaded() {
    //reposition layers correctly
    (window as any).setTimeout(() => {
      //finished creating layer groups
      this.callback();
    });
  }
}

@Component({
  components: {
    ClusterDetailsMarker: () => import('@/mapmanagement/components/Map/Markers/ClusterDetailsMarker.vue'),
    AddMemorialToolbarMarker: () => import('@/mapmanagement/components/Map/Markers/AddMemorialToolbarMarker.vue'),
    AddGraveToolbarMarker: () => import('@/mapmanagement/components/Map/Markers/AddGraveToolbarMarker.vue'),
    HoverDetailsMarker: () => import('@/mapmanagement/components/Map/Markers/HoverDetailsMarker.vue'),
    DisplayNameMarker,
    BasicDetailsMarker,
  }
})
export default class Map extends Vue {

  key: number = 0;
  layerNames = null;

  layerCounter: LayerCounter = null;
  
  unwatchMemorialService = null;

  mounted() {

    axios.get('/mapmanagement/mapInitialisation')
    .then(response => {
      let data = response.data;

      const dataExtent = JSON.parse(data.extent);
      this.$store.commit('setMapDataExtend', dataExtent)

      // increase move tolerance on touch screens
      const moveTolerance = (('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.maxTouchPoints > 0)) ? 10 : 1;

      console.log('REFSS MAP', this.$refs.map);

      let map = new OLMap({
        target: 'map',
        moveTolerance: 10,
        view: new View({
          center: [(dataExtent[0] + dataExtent[2]) / 2, (dataExtent[1] + dataExtent[3]) / 2],
          zoom: 1,
          extent: dataExtent,
          constrainOnlyCenter: true,
          resolutions: [6.999999999999999, 2.8, 1.4, 0.7, 0.28, 0.14, 0.07, 0.028, 0.014, 0.007, 0.0028],
        }),
        layers: [
          new TileLayer({
            preload: 1,
            source: new WMTS({
              attributions: `<a href="http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/" target="_blank">Contains OS data © Crown copyright and database rights (${new Date().getFullYear()})</a>`,
              format: 'image/png',
              requestEncoding: 'REST',
              crossOrigin: 'anonymous',
              url: data.baseMapUrl,
              layer: 'OSBasemap',
              matrixSet: 'OSbasemap_grid',
              style: 'default',
              tileGrid: new WMTSTileGrid({
                resolutions: JSON.parse(data.resolutions),
                matrixIds: JSON.parse(data.matrixIds),
                extent: [10161.0, 7823.0, 655619.0, 1214318.0],
              })
            })
          }),
        ],
        controls: defaultControls({attribution: false}).extend([
          new ScaleLine({
            units: 'metric'
          }),
          new MousePosition({
            className: 'olex-mouse-position',
            coordinateFormat: coordinateArray => {
            return (Math.round(coordinateArray[0]) +', '+ Math.round(coordinateArray[1]))
            }
          }),
          new Attribution({
            collapsible: false,
            className: this.$store.state.authenticatedSession ? "ol-attribution" : "ol-attribution full-logo"
          })
        ]),
      });

      (window as any).OLMap = map;
      //map.getView().fit(dataExtent, map.getSize());

      if (!this.$store.state.authenticatedSession)
        this.createWatermark(map, dataExtent);

      this.createLayerGroups(map, data, dataExtent);

      this.$emit('map-loaded', dataExtent);
    });
  }

  get markers() {
    let markers = this.$store.state.MapMarkers.markers;
    let index = 0;

    markers.forEach(marker => {
      index += marker.index;
    });
  
    this.key = index;

    return this.$store.state.MapMarkers.markers;
  }

  /**
   * Creates a watermark over the extent containing the AG logo.
   * Used for public access.
   */
  createWatermark(map, dataExtent) {
    const groupConstructorObject = {
      name: 'watermark',
      display_name: 'Watermark',
      switch_on_off: false,
      hierarchy: 999
    };

    this.$store.commit('createLayerGroupAndAdd', groupConstructorObject);

    const watermarkExtent = [dataExtent[0]-20, dataExtent[1]-20, dataExtent[2]+20, dataExtent[3]+20]

    const geojsonObject = {
      'type': 'FeatureCollection',
      'crs': {
        'type': 'name',
        'properties': {
          'name': 'EPSG:27700'
        }
      },
      'features': [{
        'type': 'Feature',
        'geometry': {
          'type': 'Polygon',
          'coordinates': [[
            [watermarkExtent[0], watermarkExtent[1]], [watermarkExtent[0], watermarkExtent[3]], [watermarkExtent[2], watermarkExtent[3]], [watermarkExtent[2], watermarkExtent[1]], [watermarkExtent[0], watermarkExtent[1]]
            ]]
        }
      }]
    }

    const layerProperties = {
      name: 'watermark', 
      display_name: 'Watermark', 
      index: 999,
      geojsonObject: geojsonObject,
      visibility: true,
      group: 'watermark', 
      minResolution: 0, 
      maxResolution: 100, 
      show_in_toolbar: false, 
      switch_on_off: false, 
      layer_type: 'VectorImage', 
      attributes_exist: false, 
      surveys_exist: false,
      layer_group_name: groupConstructorObject.name
    };
    
    this.$store.commit('createGeoJSONLayerAndAdd', layerProperties);
  }

  createLayerGroups(map, mapScope, dataExtent) {
    let topIndexlayer = 0;
    this.getLayerNames()
    .then(layerGroups => {

      this.layerCounter = new LayerCounter(layerGroups, () => {
        // load memorials details once layers have all been loaded
        this.unwatchMemorialService = this.$store.watch((state) => state.AngularMapController.angularMapController, (newValue, oldValue) => {
          if (newValue) {
            this.$store.getters.memorialService.loadMemorialsFromJSON('/mapmanagement/getMemorials/');

            window.setTimeout(() => {
              // remove watcher once memorials are loading
              this.unwatchMemorialService();
            });
          } 
        }, { immediate: true });

        this.$store.commit('setLayersGenerated', true);
      });

      layerGroups.layer_groups.forEach((group, index) => {
        if (group.group_code === 'memorials') {
          this.createMemorialLayers(group);
          return;
        }

        let groupConstructorObject = {
          name: group.group_code,
          display_name: group.display_name,
          switch_on_off: group.switch_on_off,
          hierarchy: group.hierarchy
        };

        const filterAvailablePlots = this.$router.currentRoute.query.filterAvailablePlots;
        this.$store.commit('createLayerGroupAndAdd', groupConstructorObject)

        group.layers.forEach((layer, index) => {
          //Get higher Index Layer to assign it later to drawing layer
          if(layer.hierarchy > topIndexlayer){
            topIndexlayer = layer.hierarchy;
          }
          var LayerVisibility = layer.initial_visibility;         
          if(filterAvailablePlots) {
            LayerVisibility = false;
          }

          if (layer.layer_type === 'vector') {
            if (layer.layer_code == 'plot') {
              var layerProperties = {
                name: layer.layer_code, 
                display_name: layer.display_name, 
                index: layer.hierarchy,
                url: '/mapmanagement/getGraveplots/',
                visibility: LayerVisibility,
                group: group.group_code, 
                minResolution: layer.min_resolution, 
                maxResolution: layer.max_resolution, 
                show_in_toolbar: layer.show_in_toolbar, 
                switch_on_off: group.switch_on_off, 
                layer_type: 'Vector', 
                attributes_exist: layer.attributes_exist, 
                surveys_exist: layer.surveys_exist,
                layer_group_name: groupConstructorObject.name
              };
              this.$store.commit('createGeoJSONLayerAndAdd', layerProperties);
              this.layerCounter.counter();
            } 
            else {
              if (layer.layer_code == 'reserved_plot') {
                let layerProperties = {
                  name: layer.layer_code, 
                  display_name: layer.display_name, 
                  index: layer.hierarchy,
                  url: '/mapmanagement/getReservedGraveplots/',
                  visibility: LayerVisibility,
                  group: group.group_code, 
                  minResolution: layer.min_resolution, 
                  maxResolution: layer.max_resolution, 
                  show_in_toolbar: layer.show_in_toolbar, 
                  switch_on_off: group.switch_on_off, 
                  layer_type: 'Vector', 
                  attributes_exist: layer.attributes_exist, 
                  surveys_exist: layer.surveys_exist,
                  layer_group_name: groupConstructorObject.name
                };                    
                this.$store.commit('createGeoJSONLayerAndAdd', layerProperties);
                this.layerCounter.counter();
              } 
              else {
                //Vector image layers
                var layer_type_p = 'Vector';
                if(layer.layer_code == 'tree_canopy' || layer.layer_code == 'hedge' || layer.layer_code == 'woodland' || layer.layer_code == 'bush' || layer.layer_code == 'grass' || layer.layer_code == 'shrubland' || layer.layer_code == 'carpark' || layer.layer_code == 'path'){
                  layer_type_p = 'VectorImage';
                }
                const DEFAULT_LAYER_REQUEST_URL = '/geometries/getLayer/?layer=';
                const LAYER_SOURCE_URL = layer.layer_code == 'path' ? '/geometries/getLayer/?layer=' : DEFAULT_LAYER_REQUEST_URL;

                let layerProperties = {
                  name: layer.layer_code, 
                  display_name: layer.display_name, 
                  index: layer.hierarchy,
                  url: LAYER_SOURCE_URL + layer.layer_code,
                  visibility: layer.initial_visibility,
                  group: group.group_code, 
                  minResolution: layer.min_resolution, 
                  maxResolution: layer.max_resolution, 
                  show_in_toolbar: layer.show_in_toolbar, 
                  switch_on_off: group.switch_on_off, 
                  layer_type: layer_type_p, 
                  attributes_exist: layer.attributes_exist, 
                  surveys_exist: layer.surveys_exist,
                  layer_group_name: groupConstructorObject.name
                };                    
                this.$store.commit('createGeoJSONLayerAndAdd', layerProperties);
                this.layerCounter.counter();
              }
            }
          }
          else if (layer.layer_type === 'cluster') {

            let layerProperties = {
              name: layer.layer_code,  
              display_name: layer.display_name,
              index: layer.hierarchy,
              group: group.group_code,
              url: MEMORIALSOURCEURL + layer.layer_code,
              distance: 40,
              minResolution: layer.min_resolution, 
              maxResolution: layer.max_resolution, 
              show_in_toolbar: layer.show_in_toolbar, 
              switch_on_off: group.switch_on_off, 
              visibility: true,
              layer_group_name: groupConstructorObject.name
            };

            this.$store.commit('createClusterLayerAndAdd', layerProperties);
            this.layerCounter.counter();
          } 
          else if (layer.layer_type === 'raster') {
            if (layer.layer_code === 'base') {
              // this layer is inserted earlier...
              this.layerCounter.counter();
            }
            else if (layer.layer_code === 'aerial') {
              if (mapScope.aerialURL) {
                const aerialLayerConstructor = {            
                  group: 'aerial',
                  name: 'aerial',
                  index: layer.hierarchy,
                  visibility: false,
                  show_in_toolbar: false,
                  extent: dataExtent,
                  source: {
                    type: 'TileWMTS',
                    url: mapScope.aerialURL,
                    layer: mapScope.layer,
                    matrixSet: (mapScope.layer + "_grid").toLowerCase(),
                    style: mapScope.style,
                    tileGrid: {
                      resolutions: JSON.parse(mapScope.resolutions),
                      matrixIds: JSON.parse(mapScope.matrixIds),
                      extent: dataExtent,
                    },
                  },
                  minResolution: 0.028,
                  maxResolution: 699.9999999999999,
                  layer_group_name: 'aerial'
                };

                this.$store.commit('createLayerAndAdd', aerialLayerConstructor);
                this.$store.commit('setAerialLayer', true);

                // Update aerial or map buttons depending zoom level
                this.$store.commit('pushEvent', {
                  group: 'map',
                  name: 'moveend',
                  type: 'moveend',
                  handler: (mapEvent) => {
                    //Case 1: Aerial activated, reach extra zoom level
                    if(mapEvent.map.getView().getResolution() < 0.028){
                      this.$store.commit('toggleAerial', true);
                      //needs to chnage the layer button in case aerial is activated
                      if(this.$store.state.MapLayers.layers.aerial 
                        && this.$store.state.MapLayers.layers.aerial.visibility
                        && this.$store.state.MapLayers.wasAerialVisible)
                      {
                        // TODO remove this once LayerToolbar is moved to being a child component of Map
                        (window as any).jQuery(document).trigger('triggerToggleLayerButtonBase');
                      }
                    }
                    else {
                      //Case 2: Zooming out from extra zoom level
                      if(mapEvent.map.getView().getResolution() >= 0.028){
                        this.$store.commit('toggleAerial', false);
                        if(this.$store.state.MapLayers.wasAerialVisible)
                          // TODO remove this once LayerToolbar is moved to being a child component of Map
                          (window as any).jQuery(document).trigger('triggerToggleLayerButtonAerial');
                      }
                    }
                  },
                });
              }

              this.layerCounter.counter();
            }
            else if (layer.layer_code === 'plans') {
              if (mapScope.plansURL) {
                const plansLayer = mapScope.layer + "plans";
                const plansLayerConstructor = {
                  group: 'plans',
                  name: 'plans',
                  index: layer.hierarchy,
                  visibility: false,
                  show_in_toolbar: false,
                  extent: dataExtent,
                  source: {
                    type: 'TileWMTS',
                    url: mapScope.plansURL,
                    layer: plansLayer,
                    matrixSet: (plansLayer + "_grid").toLowerCase(),
                    style: mapScope.style,
                    tileGrid: {
                      resolutions: JSON.parse(mapScope.resolutions),
                      matrixIds: JSON.parse(mapScope.matrixIds),
                      extent: dataExtent,
                    },
                  },
                  maxResolution: 699.9999999999999,
                  layer_group_name: 'plans'
                };

                this.$store.commit('createLayerAndAdd', plansLayerConstructor);
                this.$store.commit('setPlansLayer', true);
              }

              this.layerCounter.counter();
            }
          }
        });
      });

      /* Add empty layer for drawing and add-memorial */
      this.addEditableLayers(topIndexlayer);
    });
  }

  async getLayerNames() {
    if (!this.layerNames) {
      await axios.get('/geometries/getLayerNames/')
      .then(response => {
        this.layerNames = response.data;
      })
      .catch(() => {
        console.log('could not load layer names');
      });
    }
    return this.layerNames;
  }

  createMemorialLayers(group) {
    let groupConstructorObject = {
      name: group.group_code,
      display_name: group.display_name,
      switch_on_off: group.switch_on_off,
      visibility: group.initial_visibility,
      hierarchy: group.hierarchy
    };

    this.$store.commit('createLayerGroupAndAdd', groupConstructorObject)

    group.layers.forEach((layer_data, index) => {
      if (layer_data.layer_type === 'vector') {
        /**
         * temporary changes for the demo on 27/01/2016 - to be removed and display name
         * fixed in db once the arcgis template is changed. Also merge coffin tombs &
         * table tombs in a migration, and remove from create memorial list.
         */
        // if(layer_data.layer_code === 'bench')
        //   layer_data.display_name = 'Memorial Bench';
        // else if(layer_data.layer_code === 'table_tomb')
        //   layer_data.display_name = 'Chest Tomb';
        // else if(layer_data.layer_code === 'pavestone')
        //   layer_data.display_name = 'Grave Slab';
        /**
         * end temporary change
         */

        // features in multiple groups including memorials
        if (layer_data.layer_code === 'bench' || layer_data.layer_code === 'lych_gate' || layer_data.layer_code === 'mausoleum')
          layer_data.layer_code = group.group_code + '_' + layer_data.layer_code;
        

        let layerProperties = {
          name: layer_data.layer_code, 
          display_name: layer_data.display_name, 
          index: layer_data.hierarchy,
          url: MEMORIALSOURCEURL + layer_data.layer_code,
          visibility: layer_data.initial_visibility,
          group: group.group_code, 
          minResolution: layer_data.min_resolution, 
          maxResolution: layer_data.max_resolution, 
          show_in_toolbar: layer_data.show_in_toolbar, 
          switch_on_off: group.switch_on_off, 
          layer_type: 'VectorImage', 
          attributes_exist: layer_data.attributes_exist, 
          surveys_exist: layer_data.surveys_exist,
          layer_group_name: groupConstructorObject.name
        };                    
        this.$store.commit('createGeoJSONLayerAndAdd', layerProperties);
        this.layerCounter.counter();
      }
    });
  }

  addEditableLayers(layerCount) {

    this.$store.commit('createLayerAndAdd', {
      name: 'draw',
      visibility: true,
      source: {
        type: 'EmptyVector'
      },
      index: layerCount,
      style: this.$store.getters.drawLayerStyleFunction
    });

    this.$store.commit('createLayerAndAdd', {
      group: 'user-memorials',
      name: 'add-memorials',
      visibility: true,
      source: {
        type: 'EmptyVector'
      },
      index: layerCount + 1,
      style: this.$store.state.Styles.addedStyleFunction
    });

    this.$store.commit('createLayerAndAdd', {
      group: 'user-memorials',
      name: 'add-plots',
      visibility: true,
      source: {
        type: 'EmptyVector'
      },
      index: layerCount + 2,
      style: this.$store.state.Styles.addedStyleFunction
    });
  }

  mapClicked() {
    //(document.getElementsByClassName('navbar')[0] as HTMLElement).focus();
    (document.activeElement as HTMLElement).blur()
  }
}
</script>

<style scoped>
#map {
  /* navbar is 50px (should probably use a variable) */
  height:calc(100vh - 50px);
  width:100%;
}
</style>