import Vue from 'vue'
import Component from 'vue-class-component'
import axios from 'axios'
import { containsExtent, getCenter, boundingExtent, buffer } from 'ol/extent';
// import { olGeometry } from 'ol/geom/MultiPolygon'
import { FEATURES_DATA } from '@/global-static/constants';
import constants from '@/global-static/constants';

import { messages } from '@/global-static/messages.js';

@Component
export default class FeatureTools extends Vue {

  featureOverlayService = this.$store.getters.featureOverlayService;
  featureHelperService = this.$store.getters.featureHelperService;
  mapService = this.$store.getters.mapService;
  memorialService = this.$store.getters.memorialService;

  featureOverlays = [];

  /**
   * Removes feature overlays
   */
  destroyed() {
    for (let featureOverlayName of this.featureOverlays) {
      let featureOverlay = this.featureOverlayService.getFeatureOverlay(featureOverlayName);

      if (featureOverlay) {
        featureOverlay.removeAllFeatures();
        // This causes errors. Not sure why.
        //this.featureOverlayService.removeFeatureOverlayByName(overlayName);
      }
    }
  }

  /**
   * @function
   * @description
   * Gets a feature from the specified layer
   * @param {string|number} featureID - the id of the feature to be obtained
   * @param {string} layerName - name of the layer it needs to be obtained from
   * @returns a promise that resolves with the required feature
   */
  getFeatureFromLayer(featureID: string|number, layerName: string): Promise<any> {
    //debugger; //eslint-disable-line no-debugger
    return new Promise<any>(resolve => {
      //debugger; //eslint-disable-line no-debugger
      if((typeof featureID === 'string') && featureID.indexOf(';')!=-1)
      featureID = featureID.substring(featureID.indexOf(';')+1);

      (window as any).OLMap.getLayers().forEach(layer => {
        //debugger; //eslint-disable-line no-debugger
        try{
        if(layer.get('name') === layerName)
          //debugger; //eslint-disable-line no-debugger
          resolve(layer.getSource().getFeatureById(featureID));
        }catch(error){console.log(error);}
      });
    });
  }

  /**
   * Highlights feature with the given id
   * @param { [FEATURES_DATA] } features 
   * @param style The style to be applied
   */
  highlightFeatures(overlayGroup, overlayName, features: [FEATURES_DATA]=null, style=null, layerNames=null) {

    let featureOverlay = this.featureOverlayService.getFeatureOverlay(overlayName);

    if (!features && !featureOverlay)
      return;

    let layerGroup = null;

    if (!layerNames)
      // layerGroup === ['memorials', 'plots'];

    if (this.featureOverlays.indexOf(overlayName)===-1)
      this.featureOverlays.push(overlayName);

    Vue.nextTick(() => {
      if(featureOverlay)
        //clears old search results
        featureOverlay.removeAllFeatures();
      else {
        //creates feature overlay if it doesn't exist
        featureOverlay = this.featureOverlayService.addFeatureOverlay({
          name: overlayName,
          group: overlayGroup,
          layerNames: layerNames,
          layerGroup: layerGroup,
          style: style
        });
      }
      
      if (features) {
        features.forEach(feature => {
          
          const featureObject = {
            name: feature.featureID+feature.layerName+'-'+overlayName,
            feature: feature.featureID,
            layer: feature.layerName,
            isLayerGroup:false
          };

          //adds feature to hightlighted-features overlay
          featureOverlay.addFeature(featureObject);
        });
      }
    });
  }
  
  /**
   * Change cursor to a pointer
   * @param map 
   * @param enable 
   */
  togglePointerOverFeature(map, enable) {
    map.getTarget().style.cursor = enable ? 'pointer' : '';
  }

  /**
   * Pans map to put feature in the centre
   * @param featureID 
   * @param layerName 
   * @param onlyIfOffscreen If true (default), only pans if the feature is offscreen
   */
  panToFeature(featureID, layerName, onlyIfOffscreen: boolean = true) {
    
    this.getFeatureFromLayer(featureID, layerName)
    .then(feature => {

      if (feature) {
        // get extent of feature
        let ext=feature.getGeometry().getExtent();

        let mapView = (window as any).OLMap.getView();

        // get extent of map currently on screen
        let mapExtent = mapView.calculateExtent((window as any).OLMap.getSize());

        // check if selected feature is currently offscreen
        if (!onlyIfOffscreen || !containsExtent(mapExtent, ext)) {
          
          let center=getCenter(ext);

          // pan to the selected feature
          mapView.animate({
            center: center,
            duration: 1000
          });
        }
      }
      else {
        // this feature is not mapped
        let notificationHelper = this.$store.getters.notificationHelper;
        notificationHelper.createErrorNotification(messages.search.unknowLocation.title);
      }
    });
  }
  
  /**
   * @param featureIDs 
   * @returns Array containing centre coordinates for all given features
   */
  getFeaturesCentreCoordinate(featureIDs) {
    let centreCoordinates = [];

    featureIDs.forEach(id => {
      const centreCoord = this.getFeatureCentreCoordinate(id);

      if (centreCoord)
        centreCoordinates.push(centreCoord);
    });

    return centreCoordinates;
  }
  
  /**
   * @param featureID
   * @returns Centre coordinates for feature
   */
  getFeatureCentreCoordinate(featureID) {
    const memorial = this.memorialService.getMemorialById(featureID);

    if (memorial)
      return this.memorialService.getMemorialById(featureID).getCentreCoordinate();
    else
      return null;
  }

  private setExtent(featureIDs) {
    const centreCoordinates = this.getFeaturesCentreCoordinate(featureIDs);
    const newExtent = buffer(boundingExtent(centreCoordinates), 14);

    if (newExtent!==null)
      (window as any).OLMap.getView().fit(newExtent);
  }

  highlightFeaturesAndSetExtent(overlayGroup, overlayName, features: [FEATURES_DATA]=null, style=null) {
    //debugger; // eslint-disable-line no-debugger
    const featureIDs = features.map(feature => feature.featureID);
    this.setExtent(featureIDs);
    this.highlightFeatures(overlayGroup, overlayName, features, style);
  }

  SetExtentSection(coords){
    debugger; // eslint-disable-line no-debugger
    //olGeometry.
    const newExtent = buffer(boundingExtent(coords), 1);

    if (newExtent!==null)
    (window as any).OLMap.getView().fit(newExtent);
  }

  /**
   * Move feature from one layer to another
   * @param fromLayer 
   * @param toLayer 
   * @param featureID 
   */
  changeFeatureLayer(fromLayer, toLayer, featureID, newFeatureID=null) {

    return new Promise<void>((resolve, reject) => {
      this.getFeatureFromLayer(featureID, fromLayer)
        .then((feature) => {
          this.featureHelperService.removeFeatureFromLayer(featureID, fromLayer)
          .then(() => {
          if (newFeatureID)
            feature.setId(newFeatureID);
            feature.values_.id = newFeatureID;
            this.featureHelperService.addFeatureToLayer(feature, toLayer);
            resolve();
          });
        })
        .catch(function(response) {
          console.warn('Couldn\'t change feature layer: ' + response);
          reject();
        });
    });
  }

  /**
   * Get grave or memorial's feature id (i.e. id from Feature model, different from feature_id!)
   * @param layer 
   * @param id memorial_id or graveplot_id 
   */
  getMemorialPlotFeatureID(layer, id) {
    return new Promise((resolve, reject) => {
      this.getFeatureFromLayer(id, layer)
        .then((feature) => {
          resolve(feature.values_.real_feature_id);
        })
        .catch(function(response) {
          console.warn('Couldn\'t get feature: ' + response);
          reject();
        });
    });
  }
  
  /**
   * Call when a different feature is selected in openlayers
   * @param {FEATURES_DATA} featureInfo Object containing featureID & layerName
   */
  featureSelected(featureInfo: FEATURES_DATA, openRoute=null) {
    // don't load if offline
    if (!this.$store.state.Offline.online)
      return;

    let id = featureInfo.featureID;
    let layerName = featureInfo.layerName;

    if (layerName === 'available_plot') {
      // need to get graveplot id for available plots
      axios.get('/mapmanagement/availablePlotGravePlot/?available_plot_id=' + id)
      .then(response => {
        this.$router.replace({ 
          name: openRoute ? constants.GRAVE_MANAGEMENT_CHILD_ROUTES[openRoute] : constants.GRAVE_MANAGEMENT_PATH,
          params: { id: response.data.graveplot_id, layer: layerName, availablePlotID: id },
          query: this.$router.currentRoute.query,
        });
      })
      .catch(response => {
        console.warn('Couldn\'t get data from server: ' + response);
      });
    }
    else if (layerName === 'plot' || layerName === 'pet_grave')
      this.$router.replace({ name: openRoute ? constants.GRAVE_MANAGEMENT_CHILD_ROUTES[openRoute] : constants.GRAVE_MANAGEMENT_PATH, params: { id: id, layer: 'plot' }});
    else if (layerName === 'reserved_plot') 
      this.$router.replace({ name: openRoute ? constants.GRAVE_MANAGEMENT_CHILD_ROUTES[openRoute] : constants.GRAVE_MANAGEMENT_PATH, params: { id: id, layer: layerName }});
    else {
      // check if this feature is a memorial
      const memorialGroup = this.$store.getters.getLayerByName(layerName).groupName === 'memorials';

      if (memorialGroup)
        // memorial feature
        this.$router.replace({ name: openRoute ? constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES[openRoute] : constants.MEMORIAL_MANAGEMENT_PATH, params: { id: id, layer: layerName }});
      else
        // any other feature
        this.$router.replace({ name: openRoute ? constants.FEATURE_MANAGEMENT_CHILD_ROUTES[openRoute] : constants.FEATURE_MANAGEMENT_PATH, params: { id: id, layer: layerName }});
    }
  }
}
