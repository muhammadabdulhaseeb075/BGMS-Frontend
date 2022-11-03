<template>
  <div id = "graveLinkComponent">
    <div v-show="!addNewLink && !copyPersons && !copyBurials && !copyTranscribedBurials && !deletedGraveplotID && !copyTranscribedBurialsNoGrave">
      <div v-if="showLabel" style="width: 100%; padding-left: 0px;" class="management-tool-form">
        <label class="col-xs-12 control-label">Graves linked to this memorial:</label>
      </div>
      <div id="noneOption" v-if="selectFlag && graveplots.length > 0">
        <input type="radio" id="selectNone" name="select" :value="[]" v-model="selectedGrave">
        <label for="selectNone">None</label>
      </div>
      <table v-show="!loading" class="table grave-link-table management-tool-form">
        <thead v-if="graveplots.length !== 0">
          <tr>
            <th/>
            <th v-if="selectFlag">Select</th>
            <th>Grave No.</th>
            <th v-if="includeSection">Section</th>
            <th v-if="includeSubsection">Sub</th>
            <!--<th v-if="includeFeatureID">Feature ID</th>-->
            <th v-if="!selectFlag"></th>
            <th v-if="linkToGrave && !selectFlag"></th>
          </tr>
        </thead>
        <tbody id="linked-graves-list">
          <tr v-if="graveplots.length === 0">
            <td colspan="6">No graves have been linked to this memorial.</td>
          </tr>
          <template v-else-if="graveplots.length > 0" v-for="(grave) in graveplots">
            <tr :key="grave.id">
              
              <td v-if="selectFlag"><input type="radio" name="select" :value="grave.id" v-model="selectedGrave"/></td>
              <td class="table-row-bottom">{{ grave.grave_number ? grave.grave_number : 'Unknown' }}</td>
              <td v-if="includeSection" class="table-row-bottom">{{ grave.section }}</td>
              <td v-if="includeSubsection" class="table-row-bottom">{{ grave.subsection }}</td>
              <!--<td v-if="includeFeatureID" class="table-row-bottom">{{ grave.feature_id }}</td>-->
              <td v-if="siteAdminOrSiteWarden && !selectFlag"><a @click.stop="deleteLink(grave)" title="Delete link"><i class="fa fa-trash"></i></a></td>
              <td v-if="linkToGrave && !selectFlag"><a href="" @click="goToGraveManagementTool(grave.id)" title="Go to Grave Management"><i class="fa fa-arrow-circle-right"></i></a></td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <div v-if="!selectFlag">
      <button id="add-new-grave-link-btn" class="bgms-button btn" @click="addNewLink = true" v-show="!addNewLink && !copyPersons && !copyBurials && !copyTranscribedBurials && !deletedGraveplotID" v-if="siteAdminOrSiteWarden">Add New Link</button>
      <form class="form-horizontal form-box-inside" @submit.prevent="onSubmit" v-show="addNewLink && !copyTranscribedBurialsNoGrave">
        <div>
          <input id="grave-ref-option" type="radio" :value="linkTypeEnum.graveID" v-model="linkBy">
          <label for="grave-ref-option">Link by grave reference</label>
        </div>
        <div v-show="linkBy === linkTypeEnum.graveID">
          <div class="mc-spinner" v-show="loadingSections || loadingSubsections">
            <i class="fa fa-spinner fa-spin"></i>
            <p>Loading grave sections</p>
          </div>
          <div class="row input-row" v-if="allSections && allSections.length > 0">
            <label class="col-xs-5" for="section">Section:</label>
            <div id="section" class="col-xs-7 model-list-select-element" @keyup.delete="selectedSection=''">
              <model-list-select :list="allSections"
                v-model="selectedSection"
                option-value="id"
                option-text="section_name"
                placeholder="Not selected">
              </model-list-select>
            </div>
          </div>
          <div class="row input-row" v-if="allSubsections && allSubsections.length > 0">
            <label class="col-xs-5" for="subsection">Subsection:</label>
            <div id="subsection" class="col-xs-7 model-list-select-element" @keyup.delete="selectedSubsection=''">
              <model-list-select :list="allSubsectionsFiltered"
                v-model="selectedSubsection"
                option-value="id"
                option-text="subsection_name"
                placeholder="Not selected"
                :isDisabled="allSubsectionsFiltered.length === 0">
              </model-list-select>
            </div>
          </div>
          <div class="row input-row">
            <label class="col-xs-5" for="grave-number">Grave number:</label>
            <div id="grave-number" class="col-xs-7">
              <input type="text" class="form-control form-field" placeholder="Grave number" v-model="enteredGraveNumber" @keyup.enter="findGrave">
            </div>
          </div>
          <div class="row input-row find-grave">
            <button class="bgms-button btn" type="button" @click="findGrave" :disabled="!enteredGraveNumber">Find</button>
          </div>
          <div class="grave-info">
            <div>{{ selectedGraveInfo }}</div>
            <template v-for="grave in multipleGravesInfo">
              <tr :key="grave">
                <td>{{ grave }}</td>
              </tr>
            </template>
            <template v-for="person in selectedGravePersons">
              <tr :key="person.id">
                <td>{{ person.first_names }} {{ person.last_name }}</td>
              </tr>
            </template>
            <button class="bgms-button btn" type="button" 
              v-if="selectedGraveInfo && !validGraveSelected && !(multipleGravesInfo && multipleGravesInfo.length)"
              @click="findTranscribedBurials">
              Look For Transcribed Burials
            </button>
          </div>
        </div>

        <div v-if="allFeatureIDs">
          <input id="feature-id-option" type="radio" :value="linkTypeEnum.featureID" v-model="linkBy">
          <label for="feature-id-option">Link by feature ID</label>
        </div>
        <div v-show="linkBy === linkTypeEnum.featureID" v-if="allFeatureIDs && allFeatureIDs.length > 0">
          <div class="row input-row">
            <label class="col-xs-5" for="feautre-id">Feature ID:</label>
            <div id="feautre-id" class="col-xs-7 model-list-select-element">
              <model-list-select :list="allFeatureIDs"
                v-model="selectedFeatureID"
                option-value="id"
                option-text="feature_id"
                placeholder="Not selected">
              </model-list-select>
            </div>
          </div>
        </div>

        <div>
          <input id="map-option" type="radio" :value="linkTypeEnum.map" v-model="linkBy">
          <label for="map-option">Link by map</label>
        </div>
        <div v-show="linkBy === linkTypeEnum.map">
          <div class="row input-row">
            Select a grave on the map by clicking on it.
          </div>
          <div v-if="validGraveSelected" class="row input-row">
            <i class="fa fa-check-circle"/> Grave selected
          </div>
        </div>

        <div class="form_buttons">
          <button type="submit" class="bgms-button btn" :disabled="((linkBy === linkTypeEnum.graveID || linkBy === linkTypeEnum.map) && !validGraveSelected) || (linkBy === linkTypeEnum.featureID && !selectedFeatureID)">Link & Save</button>
          <button class="bgms-button btn" type="button" @click="formCancel">Cancel</button>
        </div>
      </form>
      
      <LinkBurialsToGraveOrMemorial 
        v-if="copyPersons"
        message="Would you like to link the selected persons to the grave?"
        :distinctPersonsOrBurials="distinctPersonsToCopy"
        :linkToGrave="true"
        :memorialUUID="this.memorialID"
        :graveplotUUID="this.validGraveSelected"
        @linksMadeSuccessfully="refreshPersons()"
        @closeComponent="copyBurials || copyTranscribedBurials ? copyPersons=null : formCancel()">
      </LinkBurialsToGraveOrMemorial>
      <LinkBurialsToGraveOrMemorial
        v-if="copyBurials"
        message="Would you like to link the selected persons to the memorial?"
        :distinctPersonsOrBurials="distinctBurialsToCopy"
        :linkToMemorial="true"
        :memorialUUID="this.memorialID"
        :graveplotUUID="this.validGraveSelected"
        @linksMadeSuccessfully="refreshPersons()"
        @closeComponent="copyPersons || copyTranscribedBurials ? copyBurials=null : formCancel()">
      </LinkBurialsToGraveOrMemorial>
      <LinkBurialsToGraveOrMemorial
        v-if="copyTranscribedBurials"
        message="The following transcribed and unlinked persons have been assigned the same grave number as this grave. Would you like to link them to this grave and memorial?"
        :distinctPersonsOrBurials="distinctTranscribedBurialsToCopy"
        :linkToMemorial="true"
        :linkToGrave="true"
        :memorialUUID="this.memorialID"
        :graveplotUUID="this.validGraveSelected"
        @linksMadeSuccessfully="refreshPersons()"
        @closeComponent="copyPersons || copyBurials ? copyTranscribedBurials=null : formCancel()">
      </LinkBurialsToGraveOrMemorial>

      <LinkBurialsToGraveOrMemorial
        v-if="copyTranscribedBurialsNoGrave"
        :message="`The following transcribed and unlinked persons have been assigned the same grave number (${enteredGraveNumber}). Would you like to link them to this memorial?`"
        :distinctPersonsOrBurials="distinctTranscribedBurialsNoGraveToCopy"
        :linkToMemorial="true"
        :linkToGrave="false"
        :memorialUUID="this.memorialID"
        :graveplotUUID="null"
        :graveNumber="enteredGraveNumber"
        @closeComponent="copyTranscribedBurialsNoGrave=null;"
        v-on:linksMadeSuccessfully="refreshPersonsAndGravePlotsToShowLinks($event)"
      >
      </LinkBurialsToGraveOrMemorial>
      
      <form class="form-horizontal form-box-inside" @submit.prevent="unlinkPersons" v-if="deletedGraveplotID">
        <div style="width: 100%; padding-left: 0px;" class="management-tool-form">
          <label class="col-xs-12 control-label">The following persons currently belong to both grave and memorial. Choose which features you would like them to remain linked to.</label>
        </div>
        <table class="table table-condensed">
          <thead>
            <tr>
              <th>Memorial<br><input type="checkbox" @change="memorialCheck" checked="true"/></th>
              <th>Grave<br><input type="checkbox" @change="graveCheck" checked="true"/></th>
              <th>Name</th>
            </tr>
          </thead>
          <tbody id="linked-memorials-list">
            <tr v-for="burial in sharedBurials" :key="burial.burial_id">
              <td><input type="checkbox" :value="burial.includeInMemorial" v-model="burial.includeInMemorial"/></td>
              <td><input type="checkbox" :value="burial.includeInGrave" v-model="burial.includeInGrave"/></td>
              <td>{{ burial.display_name }}</td>
            </tr>
          </tbody>
        </table>
        <div class="form_buttons">
          <button type="submit" class="bgms-button btn">Save</button>
          <button class="bgms-button btn" type="button" @click="sharedBurials=[]; deletedGraveplotID=null;">Cancel</button>
        </div>
      </form>
    </div>

    <div v-show="loading" class="sidebar-message page-loading-message loading-placeholder">
      <div class="sidebar-message-contents loading-placeholder-contents">
        <i class="fa fa-spinner fa-spin"/>
        <p>Loading...</p>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import VueRouter from 'vue-router';
import axios from 'axios';
import Component, { mixins } from 'vue-class-component';
import { Watch, Prop } from 'vue-property-decorator';
import GraveLocation from '@/mixins/graveLocation';
import FeatureTools from '@/mapmanagement/mixins/featureTools';
import { messages } from '@/global-static/messages.js';
import constants from '@/global-static/constants.ts';
import LinkBurialsToGraveOrMemorial from '@/mapmanagement/components/ManagementTool/Components/LinkBurialsToGraveOrMemorial.vue';

Vue.use(VueRouter);

enum linkType { graveID, featureID, map }

/**
 * Class representing GraveLinkSidebar component
 * @extends Sidebar mixin
 * @extends GraveLocation mixin
 */
@Component({
  components: {
    LinkBurialsToGraveOrMemorial
  }
})
export default class GraveLinkComponent extends mixins(GraveLocation, FeatureTools){

  @Prop() id;
  @Prop() linkToGraveProp;
  @Prop() selectFlagProp;
  @Prop() showLabelProp;

  linkTypeEnum = linkType;
  linkBy = this.linkTypeEnum.graveID;

  memorialID = null;
  linkToGrave: boolean = false;
  selectFlag: boolean = false;
  selectedGrave = [];

  loading: boolean = false;
  addNewLink: boolean = false;
  copyPersons: boolean = false;
  copyBurials: boolean = false;
  copyTranscribedBurials: boolean = false;
  copyTranscribedBurialsNoGrave: boolean = false;
  distinctPersonsToCopy = []
  distinctBurialsToCopy = []
  distinctTranscribedBurialsToCopy = []
  distinctTranscribedBurialsNoGraveToCopy = []
  graveplots = [];

  deletedGraveplotID = null;
  sharedBurials = [];

  validGraveSelected: string = null;
  selectedGraveInfo: string = "";
  multipleGravesInfo = [];
  selectedGravePersons = [];

  subsectionFilter: string = "";

  siteAdminOrSiteWarden: boolean = this.$store.state.siteAdminOrSiteWarden;

  personService = this.$store.getters.personService;
  eventService = this.$store.getters.eventService;
  toolbarService = this.$store.getters.toolbarService;
  notificationHelper: any = this.$store.getters.notificationHelper;

  showLabel: boolean = false;

  plotLayerNames = ['plot', 'available_plot', 'reserved_plot'];
  featureOverlay = null;

  /**
   * Vue mounted lifecycle hook
   * - gets list of grave feature_ids
   */
  mounted() {
    let v= this;

    v.memorialID = v.id;
    v.linkToGrave = v.linkToGraveProp === true;
    v.selectFlag = v.selectFlagProp === true;
    v.showLabel = v.showLabelProp === true;

    if (!this.allFeatureIDs) {
      // Get all feature ids
      axios.get('/mapmanagement/getFeatureIDs/')
        .then(function(response) {
          if (response.data && response.data.length > 0)
            v.$store.commit('populateFeatureIDs', response.data);
        })
        .catch(function(response) {
          console.warn('Couldn\'t get feature ids:', response);
        });
    }
  }

  destroyed() {
    this.resetForm();
  }

  /*** Watchers ***/

  /**
   * Watcher: When the selected memorial is changed, this loads linked graves data
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('memorialID', { immediate: true})
  onMemorialChanged(val: any, oldVal: any) {
    if (val === oldVal || !val){
      return;
    }

    this.loading = true;

    this.formCancel();

    // Get the existing grave links for the memorial
    axios.get('/mapmanagement/graveLinks/?memorial_uuid=' + val)
      .then(response => {
        this.graveplots = response.data.graveplot_memorials;

        // show form straight away if not current links
        if (this.graveplots.length === 0 && this.siteAdminOrSiteWarden)
          this.addNewLink = true;

        this.loading = false;
      })
      .catch(response => {
        this.loading = false;
        console.warn('[GraveLinkSidebar] Couldn\'t get grave links:', response);
      });
  }

  /**
   * Update store when a grave has been un/selected
   */
  @Watch('selectedGrave')
  onSelectedGraveChanged(val: any, oldVal: any) {
    this.$store.commit('appendToComponentData', { componentName: 'linked_graves', fieldName: 'selectedGrave', value: val });
  }

  @Watch('linkBy')
  onLinkByChanged(val: any, oldVal: any) {
    this.validGraveSelected = null;
    if (val === this.linkTypeEnum.map)
      // enable selecting on map
      this.linkByMap();
    else if (oldVal === this.linkTypeEnum.map) {
      this.resetForm();
    }
  }

  @Watch('addNewLink')
  onAddNewLinkChanged(val: any, oldVal: any) {
    if (val && this.linkBy === this.linkTypeEnum.map)
      // enable selecting on map
      this.linkByMap();
  }

  @Watch('enteredGraveNumber')
  onGraveNumberChanged(val: any, oldVal: any) {
    this.validGraveSelected = null;
    this.selectedGraveInfo = "";
    this.multipleGravesInfo = [];
    this.selectedGravePersons = [];
  }

  /*** Computed ***/

  /**
   * Computed property: Get the selected memorial
   * @returns {any} memorial
   */
  get memorial() {
    return this.$store.state.MemorialSidebar.memorial;
  }

  /**
   * Computed property: Get the available feature ids
   * @returns {any}
   */
  get allFeatureIDs() {
    return this.$store.state.allFeatureIDs;
  }

  get includeSection(): boolean {
    const result = this.graveplots.find(grave => grave.section );
    return result;
  }

  get includeSubsection(): boolean {
    const result = this.graveplots.find(grave => grave.subsection );
    return result;
  }

  get includeFeatureID(): boolean {
    const result = this.graveplots.find(grave => grave.feature_id );
    return result;
  }

  /*** Methods ***/

  /**
   * Cancels new grave link form
   */
  formCancel() {
    this.resetForm();
    this.addNewLink = false;

    this.distinctPersonsToCopy = [];
    this.copyPersons = false;

    this.distinctBurialsToCopy = [];
    this.copyBurials = false;

    this.distinctTranscribedBurialsToCopy = [];
    this.copyTranscribedBurials = false;

    this.distinctTranscribedBurialsNoGraveToCopy = [];
    this.copyTranscribedBurialsNoGrave = false;
  }

  /**
   * Reset the form
   */
  resetForm() {
    this.enteredGraveNumber = "";
    this.selectedSection = "";
    this.selectedSubsection = "";
    this.selectedFeatureID = "";
    this.validGraveSelected = null;
    this.selectedGraveInfo = "";
    this.multipleGravesInfo = [];
    this.selectedGravePersons = [];

    if (this.featureOverlay)
      this.featureOverlay.removeAllFeatures();
      
    this.eventService.removeEventsByGroup("select_record");
    this.toolbarService.restoreEventsSub();
  }
  
  /**
   * Submit grave to be linked to memorial
   */
  onSubmit(e) {
    e.preventDefault();

    let postData;

    // if grave selected using grave number
    if (this.linkBy === this.linkTypeEnum.graveID) {

      if (!this.validGraveSelected) {
        this.notificationHelper.createErrorNotification("You must have found a valid result first.");
        return;
      }
    }
    // if grave selected using feature id
    else if (this.linkBy === this.linkTypeEnum.featureID) {

      if (!this.selectedFeatureID) {
        this.notificationHelper.createErrorNotification("You must include a Feature ID.");
        return;
      }

      this.validGraveSelected = this.selectedFeatureID;
    }

    postData = {
      "memorial_id": this.memorialID,
      "graveplot_id": this.validGraveSelected
    }

    axios.post('/mapmanagement/graveLinks/', postData)
    .then(response => {
      console.log(response);
      this.notificationHelper.createSuccessNotification(messages.graveLinks.save.success.title);

      this.refreshGravePlots(response.data.memorials);

      this.copyPersons = response.data.memorial_persons_distinct_list && response.data.memorial_persons_distinct_list.length > 0;
      this.copyBurials = response.data.graveplot_burial_distinct_list && response.data.graveplot_burial_distinct_list.length > 0;
      this.copyTranscribedBurials = response.data.transcribed_burials_distinct_list && response.data.transcribed_burials_distinct_list.length > 0;

      if (this.copyPersons || this.copyBurials || this.copyTranscribedBurials) {

        this.addNewLink = false;

        if (this.copyPersons)
          this.distinctPersonsToCopy = response.data.memorial_persons_distinct_list;

        if (this.copyBurials)
          this.distinctBurialsToCopy = response.data.graveplot_burial_distinct_list;

        if (this.copyTranscribedBurials)
          this.distinctTranscribedBurialsToCopy = response.data.transcribed_burials_distinct_list;
      }
      else {
        //close form
        this.formCancel();
      }
    })
    .catch(error => {
      console.log(error);
      this.notificationHelper.createErrorNotification(messages.graveLinks.save.fail.title);
    });
  }

  /** 
   * Called when user wants to delete link to grave
   * @param {any} grave - the grave to break link with
   */
  deleteLink(grave) {
    let v = this;
    v.notificationHelper.createConfirmation("Delete link", "Any persons linked to this grave will be removed from this memorial.\n\nAre you sure you want to delete this link?", function() {
      let postData = {
        "memorial_id": v.memorialID,
        "graveplot_id": grave.id
      }

      axios.delete('/mapmanagement/graveLinks/', { params: postData })
      .then(function (response) {
        console.log(response);
        v.notificationHelper.createSuccessNotification(messages.graveLinks.delete.success.title);

        //remove record
        const index = v.graveplots.indexOf(grave);

        if (index !== -1) {
          v.graveplots.splice(index, 1);
        }

        // update count
        v.modifyLinkedGravesCount(-1);

        if (response.data.shared_burials && response.data.shared_burials.length > 0) {
          // open form so user can decide which feature burials should belongs
          v.deletedGraveplotID = grave.id;
          v.sharedBurials = response.data.shared_burials;
        }
        else {
          //close form
          v.formCancel();
        }
      })
      .catch(function (error) {
        console.log(error);
        v.notificationHelper.createErrorNotification(messages.graveLinks.delete.fail.title);
      });
    });
  }

  unlinkPersons(e) {
    e.preventDefault();

    let sharedBurialsToUnlink = [];

    this.sharedBurials.forEach((burial) => {
      if ('includeInGrave' in burial || 'includeInMemorial' in burial) {
        let newItem = { 'burial_id': burial.burial_id,
                        'person_id': burial.person_id };

        if (!burial.includeInGrave)
          newItem['add_to_grave'] = false;
        if (!burial.includeInMemorial)
          newItem['add_to_memorial'] = false;

        sharedBurialsToUnlink.push(newItem);
      }
    });

    if (sharedBurialsToUnlink.length > 0) {

      let postData = {
        "memorial_uuid": this.memorialID,
        "graveplot_uuid": this.deletedGraveplotID,
        "burial_list": sharedBurialsToUnlink
      }

      axios.post('/mapmanagement/modifyBurialsLinkedFeatures/', postData)
      .then((response) => {
        this.notificationHelper.createSuccessNotification("Persons successfully unlinked");

        // force list of persons to refresh
        this.refreshPersons();

        this.updateGraveplotLayer(response.data, this.deletedGraveplotID);
      })
      .catch(() => {
        this.notificationHelper.createErrorNotification("Persons unsuccessfully unlinked");
      })
      .finally(() => {
        this.deletedGraveplotID = null;
        this.sharedBurials = [];
      });
    }
    else {
      this.deletedGraveplotID = null;
      this.sharedBurials = [];
    }
  }

  /**
   * Check if graveplot needs layer updated, and change it if it does
   */
  updateGraveplotLayer(data, graveplotId) {
    if (data.original_graveplot_layer && data.new_graveplot_layer && data.original_graveplot_layer !== data.new_graveplot_layer) {
      // need to change graveplot layer

      // if changed to available layer, need to update layer id with topopolygon id
      const newID = data.new_graveplot_layer === 'available_plot' ? data.graveplot_topopolygon_id : data.graveplot_id;
      this.changeFeatureLayer(data.original_graveplot_layer, data.new_graveplot_layer, graveplotId, newID);
    }
  }
  
  /**
   * Modify memorial's linked graves count
   * @param {any} memorial
   * @param {number} i - what to add on to the existing linked graves count
   */
  modifyLinkedGravesCount(i:number) {
    if (this.memorial) {
      let count = this.memorial.get("linked_graves_count");

      if (count)
        this.memorial.set("linked_graves_count", count + i);
      else // undefined
        this.memorial.set("linked_graves_count", i);
    }
  }

  /**
   * Finds grave using given reference
   */
  findGrave() {
    this.selectedGravePersons = [];
    this.selectedGraveInfo = "";
    this.multipleGravesInfo = [];
    this.validGraveSelected = null;

    if (!this.enteredGraveNumber) {
      this.notificationHelper.createErrorNotification("You must include a Grave Number.");
      return;
    }

    let params = {graveNumber: this.enteredGraveNumber};

    if (this.selectedSection)
      params["sectionID"] = this.selectedSection;
    if (this.selectedSubsection)
      params["subsectionID"] = this.selectedSubsection;

    // Find details about inputed grave
    axios.get('/mapmanagement/findGraveplotByGraveNumber/', { params: params })
    .then(response => {
      if (response.data.results === 1) {
        
        this.selectedGraveInfo = this.getGraveInfoMessage(response.data);
        this.selectedGravePersons = response.data.persons;
        this.validGraveSelected = response.data.grave_id;
      }
      else if (response.data.results > 1) {
        this.selectedGraveInfo = "More than one result:";

        for (let i = 0; i<response.data.graves.length; i++) {
          this.multipleGravesInfo.push(i + 1 + ". " + this.getGraveInfoMessage(response.data.graves[i]));
        }
      }
      else {
        this.selectedGraveInfo = "Grave not found.";
      }
    })
    .catch(response => {
      console.warn('[GraveLinkSidebar] Couldn\'t find graveplot:', response);
    });
  }

  getGraveInfoMessage(graveData) {
    let message = "Grave number: " + graveData.grave_number;

    if (graveData.section) {
      message += ",\nSection: " + graveData.section;
    }

    if (graveData.subsection) {
      message += ",\nSubsection: " + graveData.subsection;
    }

    return message;
  }

  goToGraveManagementTool(id) {
    this.$router.replace({ name: constants.GRAVE_MANAGEMENT_PATH, params: { id: id, layer: 'unknown' }});
  }


  /**
   * Toggle checkbox for all rows
   */
  memorialCheck(event) {
    this.sharedBurials.forEach((burial) => {
      burial.includeInMemorial = event.target.checked;
    });
  }

  /**
   * Toggle checkbox for all rows
   */
  graveCheck(event) {
    this.sharedBurials.forEach((burial) => {
      burial.includeInGrave = event.target.checked;
    });
  }

  refreshPersons() {
    this.personService.currentMemorialID = null;

    // if being used within the management tool
    if (this.$route && this.$route.name) {
      let query = JSON.parse(JSON.stringify(this.$route.query));
      query['refresh'] = true;
      this.$router.replace({ query: query });
    }
  }
  refreshGravePlots(memorials) {
     //show new record
      this.graveplots = memorials.graveplot_memorials;

      // update count
      this.modifyLinkedGravesCount(1);
  }

  refreshPersonsAndGravePlotsToShowLinks(memorials) {
    this.refreshPersons();
    this.refreshGravePlots(memorials);
    this.formCancel();
  }

  /**
   * Use the map to select a grave to link memorial to
   */
  linkByMap() {
    let v = this;

    let personInteractionService = v.$store.getters.personInteractionService;

    // remove current ol events
    v.toolbarService.removeEventsSub();

    // create event handler for highlighting features on mouseover
    v.eventService.pushEvent({
      group: 'select_record',
      name: 'hover_highlight_record',
      layerNames: v.plotLayerNames,
      type: 'pointermove',
      handler: personInteractionService.selectIconsOnHover
    });

    // create event handler for clicking on feature
    v.eventService.pushEvent({
      group: 'select_record',
      name: 'click_record',
      layerNames: v.plotLayerNames,
      type: 'click',
      handler: (evt, features, layerNames) => {
        if (features[0]) {
          v.featureSelected(features[0]);
        }
      }
    });
  }

  /**
   * When a feature is selected on the map
   */
  featureSelected(feature) {
    this.validGraveSelected = feature.getId();

    if (!this.featureOverlay) {

      let featureOverlayService = this.$store.getters.featureOverlayService;

      // overlay for highlighting the selected grave
      this.featureOverlay = featureOverlayService.addFeatureOverlay({
        name: 'selected-grave',
        group: 'select_record',
        layerGroup: this.plotLayerNames,
        style: this.$store.state.MapLayers.layerStyles.selectedStyleFunction
      });
    }
    else
      this.featureOverlay.removeAllFeatures();
      
    const featureObject = {
      name: this.validGraveSelected + feature.getProperties().marker_type+'-highlighted',
      feature: this.validGraveSelected,
      layer: feature.getProperties().marker_type,
      isLayerGroup:false
    };

    this.featureOverlay.addFeature(featureObject);
  }

  findTranscribedBurials() {
    if (this.enteredGraveNumber) {
      axios.get("/mapmanagement/unlinkedBurialsWithTranscribedGraveNumber/" + this.enteredGraveNumber+ "/")
        .then(response => {
          this.copyTranscribedBurialsNoGrave = response.data.graveplot_burial_distinct_list && response.data.graveplot_burial_distinct_list.length;
          if (this.copyTranscribedBurialsNoGrave) 
            this.distinctTranscribedBurialsNoGraveToCopy = response.data.graveplot_burial_distinct_list;
          else
            this.notificationHelper.createSuccessNotification("No burials found.");
        });
    }
  }
}
</script>
