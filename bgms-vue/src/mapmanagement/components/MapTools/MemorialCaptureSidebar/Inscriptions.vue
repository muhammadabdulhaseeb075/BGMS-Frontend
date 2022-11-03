<template>
  <div id="inscriptionsComponent" class="panel">
    <div class="panel-header">
      <button v-bind:class="{collapsed: collapsed}" class="sidebar-subheading" type="button" data-toggle="collapse" data-target="#inscriptionCollapse" aria-expanded="!collapsed" aria-controls="inscriptionCollapse">
      Inscriptions
      </button>
    </div>
    <div v-bind:class="{in: !collapsed}" class="collapse collapseSection" id="inscriptionCollapse" ref="inscriptionCollapse">
      <div class="panel-body">
        <button class="btn sidebar-normal-button bgms-button" @click="addNewInscription = true" v-show="!addNewInscription" v-if="siteAdminOrSiteWarden">Add New Inscription</button>
        <form class="form-horizontal form-box-inside" action="" @submit="onSubmit" v-if="addNewInscription">
          <div class="form-group">
            <label class="control-label col-xs-4" for="first-names">First name(s):</label>
            <div id="first-names" class="col-xs-8">
              <input type="text" class="form-control form-field" placeholder="First name(s)" maxlength="200" v-model="firstNames" autofocus>
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-xs-4" for="last-name">Last name:</label>
            <div id="last-name" class="col-xs-8">
              <input type="text" class="form-control form-field" placeholder="Last name" maxlength="35" v-model="lastName">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-xs-4" for="age-field">Age:</label>
            <div id="age-field" class="col-xs-4">
              <input type="number" class="form-control form-field" placeholder="Age" min="0" max="150" v-model.number="age">
            </div>
          </div>
          <button type="submit" class="btn bgms-button sidebar-normal-button">Save</button>
          <button class="btn sidebar-normal-button bgms-button" type="button" @click="formCancel">Cancel</button>
        </form>

        <div v-show="loadingInscriptions" class="mc-spinner">
          <i class="fa fa-spinner fa-spin"/>
          <p>Loading inscriptions</p>
        </div>
        <table v-show="!loadingInscriptions" class="table inscription-table">
          <thead>
            <tr>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Age</th>
              <th v-if="siteAdminOrSiteWarden"></th>
            </tr>
          </thead>
          <tbody id="person-list" v-if="inscriptions.length > 0">
            <tr v-for="inscription in inscriptions" :key="inscription.id">
              <td>{{ inscription.first_names }}</td>
              <td>{{ inscription.last_name }}</td>
              <td>{{ inscription.age }}</td>
              <td id="remove-icon" class="col-xs-1" v-if="siteAdminOrSiteWarden">
                <a class="glyphicon glyphicon-remove" @click="deleteMemorialInscription(inscription)"></a>
              </td>
            </tr>
          </tbody>
          <tbody id="person-list" v-else>
            <tr>
              <td colspan="4">No inscriptions recorded.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import Component from 'vue-class-component'
import { Watch } from 'vue-property-decorator'
import axios from 'axios'

import { messages } from '@/global-static/messages.js';

Vue.use(Vuex);

/**
 * Class representing Inscriptions component
 * @extends Vue
 */
@Component
export default class Inscriptions extends Vue{

  addNewInscription: boolean = false;
  loadingInscriptions: boolean = false

  notificationHelper: any = this.$store.getters.notificationHelper;
  siteAdminOrSiteWarden: boolean = this.$store.state.siteAdminOrSiteWarden;

  firstNames: string = "";
  lastName: string = "";
  age: number = null;

  /**
   * Vue mounted lifecycle hook
   * - Listens for bootstrap events fired when section is collapsed/opened
   */
  mounted() {
    let v = this;

    (window as any).jQuery(this.$refs.inscriptionCollapse).on('hidden.bs.collapse', function () {
      v.$store.commit('setInscriptionCollapsed', true);
    });

    (window as any).jQuery(this.$refs.inscriptionCollapse).on('shown.bs.collapse', function () {
      v.$store.commit('setInscriptionCollapsed', false);
    });
  }

  /*** Watchers ***/

  /**
   * Watcher: When the selected memorial is changed, this loads memorial inscriptions
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('memorial', { immediate: true})
  onMemorialChanged(val: any, oldVal: any) {
    if (val === oldVal || !val){
      return;
    }

    let v = this;
    v.loadingInscriptions = true;

    // Get the existing inscriptions for the memorial
    axios.get('/api/memorialInscriptions/?memorial_uuid=' + val.getId())
      .then(function(response) {
        for (let inspection of response.data) {
          v.$store.commit('addInscription', inspection);
        }
        v.loadingInscriptions = false;
      })
      .catch(function(response) {

        // Service worker responds with {offline: true}
        if (response.data && response.data.offline) {
          // This is just a precaution. This state should be automatically changed if network status changes.
          v.$store.commit('updateOnline', false);
          return;
        }

        v.loadingInscriptions = false;
        console.warn('[MemorialCaptureSidebar/Inscriptions] Couldn\'t get memorial inscriptions:', response);
      });
  }

  /**
   * Watcher: when new data is entered or unsaved data is saved
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('addNewInscription', { immediate: true})
  onInscriptionChanged(val: any, oldVal: any) {
    this.$store.commit('toggleUnsavedInscription', val);
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
   * Computed property: Get online status
   * @returns {boolean} True if online
   */
  get online(): boolean {
    return this.$store.state.Offline.online;
  }

  /**
   * Computed property: Get existing inscriptions
   * @returns {any} Existing inscriptions
   */

  get inscriptions() {
    return this.$store.state.MemorialCaptureSidebar.inscriptions;
  }

  /**
   * Computed property: Get inscriptionCollapsed
   * @returns {boolean} True if this section should be collapsed
   */
  get collapsed(): boolean {
    return this.$store.state.MemorialCaptureSidebar.inscriptionCollapsed;
  }

  /*** Methods ***/

  /**
   * Cancel new inscriptions
   */
  formCancel() {
    this.resetForm();
    this.addNewInscription = false
  }

  /**
   * If online: saves change to server.
   * If offline: adds change to service worker queue.
   */
  onSubmit(e) {
    e.preventDefault();

    let v = this;

    let postData = {
      "memorial": this.memorial.getId(),
      "first_names": this.firstNames,
      "last_name": this.lastName,
      "age": this.age,
      "date": this.getTodaysDate()
    }

    axios.post('/api/memorialInscriptions/', postData)
      .then(function (response) {
        console.log(response);
        v.notificationHelper.createSuccessNotification(messages.memorialInscriptions.save.success.title);

        //show new record
        v.$store.commit('addInscription', response.data);

        //close form
        v.formCancel();
      })
      .catch(function (error) {
        console.log(error);
        v.notificationHelper.createErrorNotification(messages.memorialInscriptions.save.fail.title);
      });
  }

  /**
   * Reset the form
   */
  resetForm()
  {
    this.firstNames = "";
    this.lastName = "";
    this.age = null;
  }

  /**
   * Deletes an inscription.
   */
  deleteMemorialInscription(inscription) {

    let v = this;

    let postData = {
      "id": inscription.id,
      "queue_id": inscription.queue_id
    }

    axios.delete('/api/memorialInscriptions/', { params: postData })
      .then(function (response) {
        console.log(response);
        v.notificationHelper.createSuccessNotification(messages.memorialInscriptions.delete.success.title);

        //remove record
        v.$store.commit('removeInscription', inscription);
      })
      .catch(function (error) {
        console.log(error);
        v.notificationHelper.createErrorNotification(messages.memorialInscriptions.delete.fail.title);
      });
  }

  /**
   * @returns {any} Today's date
   */
  getTodaysDate() {
    let today = new Date();
    let dd: number = today.getDate();
    let mm: number = today.getMonth()+1; //January is 0!
    let yyyy: number = today.getFullYear();

    if(dd<10) {
        dd = 0+dd
    }

    if(mm<10) {
        mm = 0+mm
    }

    return dd + '/' + mm + '/' + yyyy;
  }
}
</script>
