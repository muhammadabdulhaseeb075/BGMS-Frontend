import Vue from 'vue'
import Component from 'vue-class-component'

@Component
export default class PersonMixin extends Vue {

  personInteractionService = this.$store.getters.personInteractionService;
  click_dict = {}

  /**
   * Displays marker at feature
   * @param coordinate 
   * @param featureId 
   * @param template 
   * @param closeHandler 
   */
  showClickDetails(coordinate, featureId, template, closeHandler){

    // I originally wrote this as a class variable. 
    // But it caused a 'Maximum call stack size exceeded' in deployment (not development).
    let markerService = this.$store.getters.markerService;
    // let layer_name = 'person-basic-details';  
    if(!this.$store.state.ExportMap.severalPopUps && !this.$store.state.ExportMap.severalSurnames){
      this.closeClickDetails();
    }
    let layer_name = featureId;

    if (this.click_dict[featureId]==null){
      this.click_dict[featureId]=1;
    }
    else{
      if(this.click_dict[featureId]<4){
        this.click_dict[featureId]++;
        if(this.click_dict[featureId] != 1) {
          this.personInteractionService.featureOverlays['clicked-memorials'].removeFeatureByName(featureId); //remove selected overlays
          this.$store.getters.markerService.removeMarkerByName(featureId)
        }
      }
      else{
        this.click_dict[featureId] = 0
        this.personInteractionService.featureOverlays['clicked-memorials'].removeFeatureByName(featureId); //remove selected overlays
        this.$store.getters.markerService.removeMarkerByName(featureId)
      }
    }
    let bottom_left = this.click_dict[featureId] == 1? "ol-popup-bottom" :
        this.click_dict[featureId] == 2? "ol-popup-right" :
        this.click_dict[featureId] == 3? "ol-popup-top" : "ol-popup-left"
    let bottom_offset = this.click_dict[featureId] == 1? "[0, -25]" :
        this.click_dict[featureId] == 2? "[25, 0]":
        this.click_dict[featureId] == 3? "[0, 25]" : "[-25, 0]";

    let offset_title = this.click_dict[featureId] == 1? "bottom-center" :
        this.click_dict[featureId] == 2? "center-left":
        this.click_dict[featureId] == 3? "top-center" : "center-right";
    let top_left = "ol-popup-top"
    let tooltip_json = JSON.parse('{"' + offset_title + '": "' + bottom_left+ '" ,"top-left": "'+ top_left+ '"}')
    let offset_json = JSON.parse('{"' + offset_title + '": '  + bottom_offset+ ',"top-left": [-47, 21] }')
    markerService.removeMarkersByGroup('person-hover'); //remove hoovered pop up

    let myMarker = {
      group: 'person',
      name: layer_name,
      positioning: [offset_title,'top-left'],
      tooltip: tooltip_json,
      offset: offset_json,
      position: coordinate,
      //autoPan: true,
      template: template,
      closeHandler: closeHandler,
      featureId: featureId
    }
    if(this.click_dict[featureId] != 0) {
      markerService.pushMarker(myMarker);
    }
    if(!this.$store.state.ExportMap.severalPopUps && !this.$store.state.ExportMap.severalSurnames){
      this.personInteractionService.detailsOnHoverEvent(false);
    }
  }

  /**
   * Remove marker at feature
   */
  closeClickDetails() {
    this.personInteractionService.featureOverlays['clicked-memorials'].removeAllFeatures(); //remove selected overlays
    this.$store.getters.markerService.removeMarkersByGroup('person');
    this.click_dict = {}
  }
}
