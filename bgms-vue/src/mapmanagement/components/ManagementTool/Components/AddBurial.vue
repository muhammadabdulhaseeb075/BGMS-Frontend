<template>
  <div id="addBurial" class="add-container">
    <div class="wizard-navigation">
      <div v-if="!savingFlag">
        <a class="col-xs-3" @click="close()">Cancel</a>
        <div v-if="selectedPage === addBurialPagesEnum.burial">
          <div class="col-xs-6"></div>
          <a class="col-xs-3" @click="selectedPage=addBurialPagesEnum.person">Next <i class='fa fa-arrow-right'/></a>
        </div>
        <div v-else-if="selectedPage === addBurialPagesEnum.person">
          <div class="col-xs-3"></div>
          <a class="col-xs-3" @click="leavePersonDetails(addBurialPagesEnum.burial)"><i class='fa fa-arrow-left'/> Back</a>
          <a class="col-xs-3" @click="leavePersonDetails(addBurialPagesEnum.features)">Next <i class='fa fa-arrow-right'/></a>
        </div>
        <div v-else-if="selectedPage === addBurialPagesEnum.features">
          <div class="col-xs-3"></div>
          <a class="col-xs-3" @click="selectedPage=addBurialPagesEnum.person"><i class='fa fa-arrow-left'/> Back</a>
          <a class="col-xs-3" @click="saveNewBurial">Save</a>
        </div>
      </div>
      <div v-else>  
          <div class="col-xs-11"></div>
          <div class="col-xs-1"><i class="fa fa-spinner fa-spin"></i></div>
      </div>
    </div>
    <div class="wizard-content">
      <div v-show="selectedPage === addBurialPagesEnum.burial" class="wizard-page">
        <h1>Burial Details</h1>
        <BurialDetails :id="''" :createMode="true"/>
      </div>
      <div v-show="selectedPage === addBurialPagesEnum.person" class="wizard-page">
        <h1>Person Details</h1>
        <DeathPersonDetails ref="personDetails" :id="''" :showComponent="selectedPage === addBurialPagesEnum.person"/>
      </div>
      <div v-if="memorialLinkFlag" v-show="selectedPage === addBurialPagesEnum.features" class="wizard-page">
        <h1>Link to Selected Memorial/s</h1>
        <h3>The following memorial/s are linked to this grave. Select any that you would like to link to this new burial.</h3>
        <LinkedMemorials class="component-container" :id="id" :linkedType:="'grave'" :selectFlagProp="true"/>
      </div>
      <div v-else-if="!memorialLinkFlag" v-show="selectedPage === addBurialPagesEnum.features" class="wizard-page">
        <h1>Link to Selected Grave</h1>
        <h3>The following graves are linked to this memorial. Select up to one that you would like to link to this new person.</h3>
        <GraveLinkComponent class="component-container" :id="id" :selectFlagProp="true"/>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator';
import axios from 'axios'
import constants from '@/global-static/constants.ts';
import DeathPersonDetails from '@/mapmanagement/components/ManagementTool/Components/DeathPersonDetails.vue';
import BurialDetails from '@/mapmanagement/components/ManagementTool/Components/BurialDetails.vue';
import LinkedMemorials from '@/mapmanagement/components/ManagementTool/Components/LinkedMemorials.vue';
import GraveLinkComponent from '@/mapmanagement/components/MapTools/GraveLinkComponent.vue';
import FeatureTools from '@/mapmanagement/mixins/featureTools.ts';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin.ts';
import { makeUndefinedNumbersNull } from '@/global-static/dataFormattingAndValidation.ts';

enum ADD_BURIAL_PAGES { burial, person, features }

/**
 * Class representing AddBurial component
 */
@Component({
  components: {
    DeathPersonDetails,
    BurialDetails,
    LinkedMemorials,
    GraveLinkComponent
  }
})
export default class AddBurial extends mixins(FeatureTools, ManagementToolsMixin) {

  @Prop()  id;
  @Prop() memorialLinkFlagProp;
  
  addBurialPagesEnum = ADD_BURIAL_PAGES;
  selectedPage: ADD_BURIAL_PAGES = this.addBurialPagesEnum.burial;

  notificationHelper = this.$store.getters.notificationHelper;

  savingFlag: boolean = false;
  memorialLinkFlag: boolean = false;

  selectedMemorials = [];

  mounted() {
    if (this.memorialLinkFlagProp && this.memorialLinkFlagProp != 'false')
      this.memorialLinkFlag = true;
  }

  /**
   * Save new burial and person data
   */
  saveNewBurial() {
    this.savingFlag = true;

    let layer = this.$route.params.layer;

    // get data
    let data = {
      burial_details: makeUndefinedNumbersNull(this.$store.state.ManagementTool.currentInformation.burial_details),
      person_details: makeUndefinedNumbersNull(this.$store.state.ManagementTool.currentInformation.death_person_details) };

    if (this.memorialLinkFlag) {
      data['graveplot_id'] = this.id;
      data['selected_memorials'] = this.$store.state.ManagementTool.currentInformation.linked_memorials.selectedMemorials;
    }
    else {
      if (this.$store.state.ManagementTool.currentInformation.linked_graves)
        data['graveplot_id'] = this.$store.state.ManagementTool.currentInformation.linked_graves.selectedGrave;
      data['selected_memorials'] = [this.id];
    }

    data['layer'] = layer;

    axios.post('/mapmanagement/createNewBurial/', data)
    .then(response => {
      this.savingFlag = false;
      this.notificationHelper.createSuccessNotification('New burial saved successfully');

      if (layer==='available_plot' || layer==='reserved_plot') {
        let featureID = layer==='available_plot' ? this.$route.params.addburialavailablePlotID : this.$route.params.id;
        // If burial has been added successfully then this is no longer an available plot. Hence update feature.
        this.changeFeatureLayer(layer, 'plot', featureID, this.$route.params.id)
        .then(() => {
          // remove all vuex data as it is no longer needed
          this.$store.commit('resetFeatureData');
          // close new burial page and refresh data to show new burial
          this.close(response.data.person_id, response.data.burial_id, 'plot');
        })
        .catch(error => {
          let temp = error;
        });
      }
      else {
        // remove all vuex data as it is no longer needed
        this.$store.commit('resetFeatureData');
        // close new burial page and refresh data to show new burial
        this.close(response.data.person_id, response.data.burial_id);
      }
    })
    .catch(function(response) {
      this.savingFlag = false;
      console.warn('Couldn\'t save new burial:', response.response.data);
      this.notificationHelper.createErrorNotification("Couldn't save new burial");
    });
  }

  leavePersonDetails(nextPage) {
    // only move forward if validation in child component passes
    if ((this.$refs.personDetails as any).validateData())
      this.selectedPage=nextPage;
  }

  /**
   * Closes this page. If person_id and burial_id are included, this person/burial will be displayed.
   */
  close(person_id, burial_id, layer=null) {
    let parentName = this.memorialLinkFlag ? constants.GRAVE_MANAGEMENT_PATH : constants.MEMORIAL_MANAGEMENT_PATH;

    // refresh tool and show newly created burial/person
    if (person_id || burial_id) {
      Vue.nextTick(() => {
        const name = parentName === constants.GRAVE_MANAGEMENT_PATH ? constants.GRAVE_MANAGEMENT_CHILD_ROUTES.burials : constants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.persons;
        let params = { burial_id: burial_id, person_id: person_id };

        if (layer)
          params['layer'] = layer;

        this.$router.push({ name: name, params: params, query: { refresh: 'true' }});
      });
    }
    else
      this.$router.push({ name: parentName });
  }
}
</script>