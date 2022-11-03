<template>
<div>
  <label v-if="canShowOptions()" class="btn btn-bgms" aria-label="Rotate Headstone" title="Rotate Headstone">
    <input type="radio" name="rotate" autocomplete="off" checked hidden @click="floatingMemorialToolbarService.floatingOptionsHandler('rotatePlot')">
    <span class="glyphicon glyphicon-repeat"></span>
  </label>
 
  <div  v-if="canShowOptions()" class="btn-group dropdown" @click="layerSelectionService.showDropup($refs.id_shps_floating_toolbar)">
    <label type="button" class="btn btn-bgms dropdown-toggle" aria-label="Change Shape" title="Change Shape" data-toggle="dropdown" data-placeholder="false">
      <span class="glyphicon glyphicon-object-align-left"></span>
    </label>
    <ul id="id_shps_floating_toolbar" ref="id_shps_floating_toolbar" class="dropdown-menu toolbar noclose" role="menu">
      <li><input @click="floatingMemorialToolbarService.floatingOptionsHandler('selectShape', 'gravestone')" type="radio" id="id_shp_mem_0" name="name" value="value"><label for="id_shp_mem_0">Rectangle (0.65m x 0.18m)</label></li>
      <li><input @click="floatingMemorialToolbarService.floatingOptionsHandler('selectShape', 'plaque')" type="radio" id="id_shp_mem_1" name="name" value="value"><label for="id_shp_mem_1">Rectangle (1.15m x 0.12m)</label></li>
      <li><input @click="floatingMemorialToolbarService.floatingOptionsHandler('selectShape', 'window')" type="radio" id="id_shp_mem_2" name="name" value="value"><label for="id_shp_mem_2">Rectangle (2m x 0.22m)</label></li>
      <li><input @click="floatingMemorialToolbarService.floatingOptionsHandler('selectShape', 'table_tomb')" type="radio" id="id_shp_mem_3" name="name" value="value"><label for="id_shp_mem_3">Rectangle (2m x 0.9m)</label></li>
      <li><input @click="floatingMemorialToolbarService.floatingOptionsHandler('selectShape', 'rectangle1')" type="radio" id="id_shp_mem_4" name="name" value="value"><label for="id_shp_mem_4">Rectangle (0.2m x 0.3m)</label></li>
      <li><input @click="floatingMemorialToolbarService.floatingOptionsHandler('selectShape', 'square_plaque')" type="radio" id="id_shp_mem_5" name="name" value="value" ><label for="id_shp_mem_5">Square (0.3m x 0.3m)</label></li>
      <li><input @click="floatingMemorialToolbarService.floatingOptionsHandler('selectShape', 'square')" type="radio" id="id_shp_mem_6" name="name" value="value" ><label for="id_shp_mem_6">Square (0.6m x 0.6m)</label></li>
      <li><input @click="floatingMemorialToolbarService.floatingOptionsHandler('selectShape', 'war_memorial')" type="radio" id="id_shp_mem_7" name="name" value="value"><label for="id_shp_mem_7">Square (0.9m x 0.9m)</label></li>
      <li><input @click="floatingMemorialToolbarService.floatingOptionsHandler('selectShape', 'large_square')" type="radio" id="id_shp_mem_8" name="name" value="value" ><label for="id_shp_mem_8">Square (2m x 2m)</label></li>
      <li><input @click="floatingMemorialToolbarService.floatingOptionsHandler('selectShape', 'circle')" type="radio" id="id_shp_mem_9" name="name" value="value"><label for="id_shp_mem_9">Circle (diameter 1.3m)</label></li>
    </ul>
  </div>
  <!-- Hide memorial edit toolbar for now, getting incorrect list of memorial types.
  <div class="btn-group dropdown" @click="layerSelectionService.showDropup($refs.id_lyrs_floating_toolbar)">
    <label type="button" class="btn btn-bgms dropdown-toggle"  aria-label="+Change Memorial Layer" title="Change Memorial Layer" data-toggle="dropdown" data-placeholder="false">
      <span class="icon-Map-Layers-Filled"></span>
    </label>
    <ul id="id_lyrs_floating_toolbar" ref="id_lyrs_floating_toolbar" class="dropdown-menu toolbar noclose" role="menu" style="overflow-y: auto; height: 300px;">      
      <li v-for="(lyr, index) in layerSelectionService.getLayerGroups().memorials" inside-dropdown :key="index">
        <input @click="floatingMemorialToolbarService.floatingOptionsHandler('selectLayer', lyr.feature_codes__feature_type)" type="radio" :id="'id_lyr_mem_' + index" name="name" value="vale" :checked="lyr.checked">        
        <label :for="'id_lyr_mem_' + index">{{lyr.feature_codes__display_name}}</label>        
      </li>
    </ul>
  </div>
  -->
  <label class="btn btn-bgms" :disabled="floatingMemorialToolbarService.isSaving" aria-label="Save Memorial" title="Save Memorial" >
    <input type="radio" name="save" autocomplete="off" checked hidden @click="floatingMemorialToolbarService.floatingOptionsHandler('saveMemorial')">
    <span class="glyphicon glyphicon-floppy-save" aria-hidden="true"></span>
  </label>
  <label class="btn btn-bgms" aria-label="Link" title="Link Plot" v-show="!isGraveAddMarker()">
    <input type="radio" name="delete" autocomplete="off" checked hidden @click="floatingMemorialToolbarService.floatingOptionsHandler('linkPlot')" >
    <span class="glyphicon glyphicon-link" aria-hidden="true"></span>
  </label>
  <label v-if="canShowOptions()" class="btn btn-bgms" :disabled="floatingMemorialToolbarService.isDeleting" aria-label="Delete" v-show="!isGraveAddMarker() && !floatingMemorialToolbarService.isSaving" title="Delete Memorial">
    <input type="radio" name="delete" autocomplete="off" checked hidden @click="floatingMemorialToolbarService.floatingOptionsHandler('deleteMemorial')" >
    <span class="icon-Delete-Filled" aria-hidden="true"></span>
  </label>
  <label class="btn btn-bgms" aria-label="Cancel" title="Cancel">
    <input type="radio" name="cancle" autocomplete="off" checked hidden @click="floatingMemorialToolbarService.floatingOptionsHandler('cancel')" >
    <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
  </label>
</div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import Feature from "@/mapmanagement/components/Map/models/Feature";
import Memorial from "@/typings/Memorial";

@Component
export default class AddMemorialToolbarMarker extends Vue {

  @Prop() scope;

  readonly DEFAULT_MEMORIAL: Partial<Memorial> = {
    user_generated: false
  }

  get isAgStaffUser(){
      return this.$store.state.agStaff;
  }

  get memorialEdited(): Memorial | Partial<Memorial> {
      return this.$store.state.memorialEdited ? this.$store.state.memorialEdited : this.DEFAULT_MEMORIAL;
  }

  beforeMount() {
    if(!this.isGraveAddMarker() && (!this.memorialEdited || this.isDifferentFromMemorialStored(this.scope.feature))) {
      this.editMemorial(this.scope.feature);
    }
  }

  editMemorial(featureMemorial) {
    this.$store.dispatch('editMemorial', featureMemorial);
  }

  isDifferentFromMemorialStored(feature: Feature) {
    return this.memorialEdited && ( this.memorialEdited.id !== feature.id_);
  }

  isGraveAddMarker(){
    return this.scope.feature.get('marker_type') === this.addedGraveplotLayer
  }

  canShowOptions(){
    return this.isGraveAddMarker() || this.memorialEdited.user_generated || this.isAgStaffUser;
  }

  addedGraveplotLayer = 'add-memorials'

  floatingMemorialToolbarService: any = this.$store.getters.floatingMemorialToolbarService;
  layerSelectionService: any = this.$store.getters.layerSelectionService;

}
</script>
