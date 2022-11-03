<template>
  <div id="v-VueOtherToolsController">
    <div id="otherToolsAccordion">
      <label class="btn btn-bgms group-burialtools group-othertools" title="Other Tools" data-toggle="collapse" data-parent="#otherAccordion" href="#otherTools">
        <input type="radio" autocomplete="off" checked hidden>
        <span class="fa fa-download"></span>
        <span class="fa fa-download"></span>
      </label>
      <div id="otherTools"  class="btn-group panel-collapse collapse" role="group">

        <!--Export map-->
        <label class="btn btn-bgms" title="Export Map" :class="{ active: exportPDF }">
        <input type="checkbox" name="exportPDF" v-model="exportPDF" autocomplete="off" checked hidden>
        <span class="far fa-file-image"></span>
        </label>

        <!--Site files-->
        <label class="btn btn-bgms hide-opt" title="Site Files" :class="{ active: siteFiles }" v-show="!exportPDF">
          <input type="checkbox" name="siteFiles" v-model="siteFiles" autocomplete="off" checked hidden>
          <span class="far fa-copy"></span>
        </label>
      </div>

      <ExportMap v-if="showExportPDF"/>

    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import axios from 'axios';

Vue.use(Vuex);

/**
 * Class representing OtherTools component
 * @extends Vue
 */
@Component({
  components: {
    ExportMap: () => import('@/mapmanagement/components/MapTools/ExportMap.vue')
  }
})
export default class OtherTools extends Vue{

  toolbarService: any = this.$store.getters.toolbarService;
  modalHelperService: any = this.$store.getters.modalHelperService;
  notificationHelper: any = this.$store.getters.notificationHelper;

  showExportPDF: boolean = false;

  /*** Computed ***/

  get exportPDF() {
    let enabled = this.toolbarService.toggle['exportPDF'];

    if (!enabled)
      this.showExportPDF = false;

    return enabled;
  }
  set exportPDF(value) {
    this.toolbarService.toggle['exportPDF'] = value;
    this.toolbarService.toggle_option('exportPDF').then((is_enabled) => {
      this.showExportPDF = is_enabled;
    });
  }

  get siteFiles() {
    return this.toolbarService.toggle['siteFiles'];
  }
  set siteFiles(value) {
    this.toolbarService.toggle['siteFiles'] = value;
    this.toolbarService.toggle_option('siteFiles').then((is_enabled) => {
      if (is_enabled)
        this.openSiteFilesModal();
    });
  }

  /*** Methods ***/

  /**
   * Open modal to display site files
   */
  openSiteFilesModal() {

    let v= this;

    if (v.modalHelperService.modalOpened) {
      v.modalHelperService.modalOpened = false;

      document.body.style.cursor = 'progress';

      axios.get('/mapmanagement/siteFiles/').
        then((response) => {
          v.modalHelperService.openModal(response.data);
          v.modalHelperService.onCloseModal(() => { v.siteFiles = false });
        }).
        catch((response) => {
          v.modalHelperService.modalOpened = true;
          console.log('could not load data' + response.data);
          v.siteFiles = false;
          document.body.style.cursor = 'default';
        });
    }
  }  
}
</script>
