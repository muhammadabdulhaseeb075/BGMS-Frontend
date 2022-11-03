<template>
<div class="">

  <label class="btn btn-bgms" aria-label="Rotate Plot" title="Rotate Plot">
    <input type="radio" name="rotate" autocomplete="off" checked hidden @click="floatingPlotToolbarService.floatingOptionsHandler('rotatePlot')">
    <span class="glyphicon glyphicon-repeat"></span>
  </label>
 
  <div class="btn-group dropdown" @click="layerSelectionService.showDropup($refs.id_shps_floating_toolbar)">
    <label type="button" class="btn btn-bgms dropdown-toggle" aria-label="Change Shape" title="Plot Shape" data-toggle="dropdown" data-placeholder="false">
      <span class="glyphicon glyphicon-object-align-left"></span>
    </label>
    <ul id="id_shps_floating_toolbar" ref="id_shps_floating_toolbar" class="dropdown-menu toolbar noclose" role="menu">
      <li><input @click="floatingPlotToolbarService.floatingOptionsHandler('selectShape', 'default_plot')" type="radio" id="id_shp_mem_0" name="name" value="value"><label for="id_shp_mem_0">Burial (0.9m x 2m)</label></li>
      <li><input @click="floatingPlotToolbarService.floatingOptionsHandler('selectShape', 'cremation_plot')" type="radio" id="id_shp_mem_1" name="name" value="value"><label for="id_shp_mem_1">Cremation (0.5m x 0.5m)</label></li>
    </ul>
  </div>

  <label class="btn btn-bgms" :disabled="floatingPlotToolbarService.isSaving" aria-label="Save Plot" title="Save Plot" >
    <input type="radio" name="save" autocomplete="off" checked hidden @click="floatingPlotToolbarService.floatingOptionsHandler('savePlot')">
    <span class="glyphicon glyphicon-floppy-save" aria-hidden="true"></span>
  </label>
  <label class="btn btn-bgms" :disabled="floatingPlotToolbarService.isDeleting" aria-label="Delete" v-show="scope.feature.get('marker_type')!=addedGraveplotLayer && !floatingPlotToolbarService.isSaving" title="Delete">
    <input type="radio" name="delete" autocomplete="off" checked hidden @click="floatingPlotToolbarService.floatingOptionsHandler('deletePlot')" >
    <span class="icon-Delete-Filled" aria-hidden="true"></span>
  </label>
  <label class="btn btn-bgms" aria-label="Cancel" title="Cancel">
    <input type="radio" name="cancle" autocomplete="off" checked hidden @click="floatingPlotToolbarService.floatingOptionsHandler('cancel')" >
    <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
  </label>
</div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';

@Component
export default class AddGraveToolbarMarker extends Vue {

  @Prop() scope;

  addedGraveplotLayer = 'add-plots'

  floatingPlotToolbarService: any = this.$store.getters.floatingPlotToolbarService;
  layerSelectionService: any = this.$store.getters.layerSelectionService;
}
</script>