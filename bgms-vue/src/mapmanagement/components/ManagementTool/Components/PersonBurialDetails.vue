<template>
  <div id="personBurialDetails" class="tab-container">
    <div class="tabs">
      <div class="row" :class="{ 'include-options': siteAdminOrSiteWarden }">
        <div tabindex="0" class="col-xs-6" :class="{ active: selectedTab === personBurialOptionsEnum.person }" @click="appendToOrModifyItemInQuery('tab', personBurialOptionsEnum.person)" @keyup.enter="appendToOrModifyItemInQuery('tab', personBurialOptionsEnum.person)">Person</div>
        <div tabindex="0" class="col-xs-6" :class="{ active: selectedTab === personBurialOptionsEnum.burial }" @click="appendToOrModifyItemInQuery('tab', personBurialOptionsEnum.burial)" @keyup.enter="appendToOrModifyItemInQuery('tab', personBurialOptionsEnum.burial)">Burial</div>
      </div>
      <div v-if="siteAdminOrSiteWarden" class="options">
        <a href="javascript:void(0)" @click.stop="showDropDown=!showDropDown" :class="[{ active: showDropDown }, 'options-button']" title="Options"><i class="fa fa-ellipsis-h management-tool-navigation-icon"></i></a>
        <div ref="dropDownMenu" v-if="showDropDown" class="management-tool-dropdown-menu" :style="{ 'right': contentBarContainerRight }">
          <ul>
            <li><a href="javascript:void(0)" @click.prevent="moveRecord(true)">Move record</a></li>
            <li><a href="javascript:void(0)" @click.prevent="moveRecord(false)">Link record to a memorial</a></li>
            <li><a href="javascript:void(0)" v-if="showRemoveOption" @click.prevent="removeRecord">{{ removeMessage }}</a></li>
            <li><a href="javascript:void(0)"  v-if="siteAdmin" @click.prevent="deleteRecord">Delete record</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="tab-content" :key="person_id + burial_id">
      <DeathPersonDetails v-show="selectedTab === personBurialOptionsEnum.person" :id="person_id" :showComponent="selectedTab === personBurialOptionsEnum.person"/>
      <BurialDetails v-if="renderBurials" v-show="selectedTab === personBurialOptionsEnum.burial" :id="burial_id" :person_id="person_id" :showComponent="selectedTab === personBurialOptionsEnum.burial"/>
    </div>
    <div v-if="moveRecordFlag">
      <MoveRecord @close-tool="closeMoveRecordTool($event)" :data="getMoveData()"/>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import axios from 'axios'
import { Prop, Watch } from 'vue-property-decorator';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin.ts';
import constants, {PERSON_BURIAL_OPTIONS_ENUM} from '@/global-static/constants.ts';
import mapManagementConstants from '@/mapmanagement/static/constants.ts';
import DeathPersonDetails from '@/mapmanagement/components/ManagementTool/Components/DeathPersonDetails.vue';
import BurialDetails from '@/mapmanagement/components/ManagementTool/Components/BurialDetails.vue';
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts';

/**
 * Class representing PersonBurialDetails component
 * @extends ManagementToolsMixin
 */
@Component({
  components: {
    DeathPersonDetails,
    BurialDetails,
    MoveRecord: () => import('@/mapmanagement/components/ManagementTool/Components/MoveRecord.vue')
  }
})
export default class PersonBurialDetails extends mixins(ManagementToolsMixin, FeatureTools) {

  @Prop() burial_id;
  @Prop() person_id;
  
  personBurialOptionsEnum = constants.PERSON_BURIAL_OPTIONS;
  selectedTab: PERSON_BURIAL_OPTIONS_ENUM = null;

  // Don't render burial component until we actually want to see it. This stops a problem with the carousel.
  renderBurials: boolean = false;
  showDropDown: boolean = false;

  moveRecordFlag: boolean = false;
  moveRecordRemoveOriginal: boolean = false;

  toolWidth;

  siteAdmin: boolean = this.$store.state.siteAdmin;

  graveManagementFlag = false;
  memorialManagementFlag = false;
  burialPersonManagementFlag = false;

  /**
   * Vue mounted lifecycle hook
   */
  mounted() {
    if (this.isRouteActive(constants.GRAVE_MANAGEMENT_PATH))
      this.graveManagementFlag = true;
    else if (this.isRouteActive(constants.MEMORIAL_MANAGEMENT_PATH))
      this.memorialManagementFlag = true;
    else if (this.isRouteActive(constants.BURIAL_PERSON_MANAGEMENT_PATH))
      this.burialPersonManagementFlag = true;

    if (this.$route.query.tab) {
      this.selectedTab = parseInt(this.$route.query.tab as string) as PERSON_BURIAL_OPTIONS_ENUM;

      if (this.selectedTab === this.personBurialOptionsEnum.burial) {
        this.renderBurials = true;
      }
    }
    else
      this.appendToOrModifyItemInQuery('tab', 0);
      
    // Reset flag. This needs reset if someone moves from edit mode straight to another person/burial.
    this.$store.commit('commitRestoreSavedDataFlag', null);
  }

  destroyed() {
    this.showDropDown = false;

    // clean event listener
    window.removeEventListener('click', this.documentClick);
  }

  /*** Computed ***/

  /**
   * @return True if remove option should be shown
   */
  get showRemoveOption() {
    return !this.burialPersonManagementFlag;
  }
  
  get removeMessage() {
    return "Remove record from " + (this.graveManagementFlag ? 'grave' : 'memorial');
  }

  /**
   * Getter / setter for the right position of the contentbar container
   */
  get contentBarContainerRight() {
    return parseInt(document.getElementById('management-tool-contentbar-container').style.right) + 10 + 'px';
  }
  set contentBarContainerRight(value) {
    document.getElementById('management-tool-contentbar-container').style.right = value;
  }

  /*** Watchers ***/

  /**
   * Watcher: When select in router query is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.query.tab')
  onTabChanged(val: any, oldVal: any) {
    if (val != null) {
      this.selectedTab = parseInt(val) as PERSON_BURIAL_OPTIONS_ENUM;

      if (this.selectedTab === this.personBurialOptionsEnum.burial) {
        this.renderBurials = true;
      }
    }
    else
      this.selectedTab = this.personBurialOptionsEnum.person;
  }

  @Watch('showDropDown')
  onDropDownChanged(val: boolean, oldVal: boolean) {
    if (val)
      window.addEventListener('click', this.documentClick);
    else if (!val && oldVal)
      window.removeEventListener('click', this.documentClick);
  }
  
  /*** Methods ***/

  // closes the dropdown menu if outsite has been clicked
  documentClick(e) {
    let el = this.$refs.dropDownMenu
    let target = e.target
    if (( el !== target) && !(el as any).contains(target)) {
      this.showDropDown=false;
    }
  }

  getMoveData() {

    let data = {
      removeFromOriginal: this.moveRecordRemoveOriginal,
      burial_id: this.burial_id,
      person_id: this.person_id
    };

    if (this.moveRecordRemoveOriginal) {
      if (this.graveManagementFlag) {
        data["from_graveplot_uuid"] = this.$route.params.id;
      }
      else if (this.memorialManagementFlag) {
        data["from_memorial_uuid"] = this.$route.params.id;
      }
    }

    return data;
  }

  /**
   * Moves burial and person records to another grave or memorial
   * @param removeOriginal True if record is to be removed from original grave or memorial
   */
  moveRecord(removeOriginal: boolean) {
    this.toolWidth = document.getElementById('management-tool-container').clientWidth;

    this.moveRecordRemoveOriginal = removeOriginal;
    this.moveRecordFlag = true;

    this.showDropDown = false;

    //hide managment tool
    document.getElementById('management-tool-container').style.right = -this.toolWidth + "px";
    this.contentBarContainerRight = -mapManagementConstants.TOOL_CONTENT_WIDTH  - this.toolWidth + "px";
    
    let layersAccordion = document.getElementById('layersAccordion');
    if (layersAccordion) layersAccordion.style.right = "5px";
  }

  closeMoveRecordTool(response=null) {
    this.moveRecordFlag = false;

    if (this.moveRecordRemoveOriginal) {
      // refresh tool as data will now be different
      if (response && response.layer && response.topopolygon_id)
        this.closeRecordAndRefresh(response.layer, response.topopolygon_id);
      else if (response !== null)
        this.closeRecordAndRefresh();
    }

    //show managment tool
    document.getElementById('management-tool-container').style.right = "5px";
    this.contentBarContainerRight = this.toolWidth - mapManagementConstants.TOOL_BORDER_WIDTH + "px";
    
    let layersAccordion = document.getElementById('layersAccordion');
    if (layersAccordion) layersAccordion.style.right = this.toolWidth + mapManagementConstants.TOOL_CONTENT_WIDTH + mapManagementConstants.TOOL_BORDER_WIDTH + 10 + "px";
  }

  /**
   * Remove person and burial records from this feature
   */
  removeRecord() {
    let v = this;

    v.notificationHelper.createConfirmation('Remove Record', `Are you sure you want to remove this record from this ${this.graveManagementFlag ? 'grave' : 'memorial'}?`, () => {

      let postData = {};

      // graves have an id and memorials have a feature id
      if (v.graveManagementFlag) {
        postData['burial_id'] = v.burial_id;
      }
      else if (v.memorialManagementFlag) {
        postData['person_id'] = v.person_id;
        postData['memorial_uuid'] = v.$route.params.id;
      }

      axios.post('/mapmanagement/removeBurialPersonRecords/', postData)
      .then(function(response) {
        let returned_data;
        if (response.data != ""){
          returned_data = response.data;
        }
        else if(response.config && response.config.data){
          returned_data = response.config.data;
        }
        else{
          throw "Error: No data returned."
        }

        // change current plot to an available plot if it has no more burials
        if(returned_data.layer && returned_data.layer==='available_plot') {
          v.changeFeatureLayer('plot', 'available_plot', v.$route.params.id, returned_data.topopolygon_id);
          v.closeRecordAndRefresh(returned_data.layer, returned_data.topopolygon_id);
        }
        else if(returned_data.layer && returned_data.layer==='reserved_plot') {
          v.changeFeatureLayer('plot', 'reserved_plot', v.$route.params.id, v.$route.params.id);
          v.closeRecordAndRefresh(returned_data.layer);
        }
        else
          v.closeRecordAndRefresh();

        v.notificationHelper.createSuccessNotification(`Record was successfully removed from this ${v.graveManagementFlag ? 'grave' : 'memorial'}.`);
      })
      .catch(function(response) {
        v.notificationHelper.createErrorNotification(`Record was unsuccessfully removed from this ${v.graveManagementFlag ? 'grave' : 'memorial'}.`);
        console.warn(`Record move failed: ${response}\n${response.response.data}`);
      });
    });
  }

  /**
   * Delete person and burial records from BGMS
   */
  deleteRecord() {
    let v = this;

    let layer = v.$route.params.layer;

    v.notificationHelper.createConfirmation('Delete Record', 'Are you sure you want to delete this record from BGMS? This cannot be undone.', () => {

      let postData = {
        burial_id: v.burial_id,
        person_id: v.person_id
      };

      axios.delete('/mapmanagement/deleteBurialPersonRecords/', { params: postData })
      .then(function(response) {
        v.notificationHelper.createSuccessNotification('Record was successfully deleted');

        if (response.data.layer && response.data.layer!=='plot' && response.data.graveplot_id && response.data.topopolygon_id) {
          if (response.data.layer==='available_plot') {
            // If plot is now an available_plot
            v.changeFeatureLayer('plot', 'available_plot', response.data.graveplot_id, response.data.topopolygon_id)
            .then(() => {
              // refresh tool
              v.closeRecordAndRefresh('available_plot', response.data.topopolygon_id);
            });
          }
          if (response.data.layer==='reserved_plot') {
            // If plot is now an reserved_plot
            v.changeFeatureLayer('plot', 'reserved_plot', response.data.graveplot_id, response.data.graveplot_id)
            .then(() => {// refresh tool
              v.closeRecordAndRefresh('reserved_plot');
            });
          }
        }
        else {
          if (v.burialPersonManagementFlag) {
            // close tool
            v.$store.commit('closeFlag', true);
            v.$router.replace('/');
          }
          else
            // refresh tool
            v.closeRecordAndRefresh();
        }
      })
      .catch(function(response) {
        v.notificationHelper.createErrorNotification('Record was unsuccessfully deleted.');
        console.warn(`Record delete failed: ${response}\n${response.response.data}`);
      });
    });
  }

  /**
   * Close the current record and refresh the tool to show new data
   */
  closeRecordAndRefresh(layer=null, availablePlotID=null) {
    let query = null;

    let params = { layer: (layer ? layer : this.$route.params.layer) };

    if (availablePlotID)
      params['availablePlotID'] = availablePlotID;

    query = { 'refresh': true };
    
    // remove all vuex data as it is no longer needed
    this.$store.commit('resetFeatureData');

    if (this.memorialManagementFlag)
      this.$router.replace({ name: constants.MEMORIAL_MANAGEMENT_PATH, params: params, query: query });
    else if (this.graveManagementFlag)
      this.$router.replace({ name: constants.GRAVE_MANAGEMENT_PATH, params: params, query: query });
    else if (this.burialPersonManagementFlag)
      this.$router.replace({ name: constants.BURIAL_PERSON_MANAGEMENT_PATH, query: query });
  }
}
</script>