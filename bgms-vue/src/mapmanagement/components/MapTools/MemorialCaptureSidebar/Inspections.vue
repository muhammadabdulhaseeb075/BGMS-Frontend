<template>
  <div>
    <button class="btn sidebar-normal-button bgms-button" @click="addNewInspection = true" v-show="!addNewInspection" v-if="siteAdminOrSiteWarden">Add New Inspection</button>
    <form class="form-horizontal form-box-inside" action="" @submit="onSubmit" v-if="addNewInspection">
      <div class="form-group">
        <label class="control-label col-xs-4" for="condition-field">Structure Condition:</label>
        <div id="condition-field" class="col-xs-8">
          <select v-model="condition">
            <option value="1">Good</option>
            <option value="2">Reasonable</option>
            <option value="3">Poor</option>
          </select>
        </div>
      </div>
       <div class="form-group">
        <label class="control-label col-xs-4" for="inscription-field">Inscription Condition:</label>
        <div id="inscription-field" class="col-xs-8">
          <select v-model="inscription">
            <option value="1">Good</option>
            <option value="2">Reasonable</option>
            <option value="3">Poor</option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label class="control-label col-xs-4" for="remarks-field">Remarks:</label>
        <div id="remarks-field" class="col-xs-8">
          <textarea rows="2" class="form-control form-field" placeholder="Remarks" maxlength="200" v-model="remarks"></textarea>
        </div>
      </div>
      <div class="form-group">
        <label class="control-label col-xs-4" for="action-required">Action required:</label>
        <div id="action-required" class="col-xs-8">
          <input type="checkbox" class="form-control" v-model="actionRequired">
        </div>
      </div>
      <div v-show="photoProcessing" class="mc-spinner"><i class="fa fa-spinner fa-spin"></i></div>
      <div class="photo-buttons" v-show="!photoProcessing && !photo && !storageTooSmallForImageUpload">
        <label for="fileUploaderInputInspections" style="margin-bottom:10px;" class="bgms-button btn">Add a Photo</label>
        <input ref="fileUploaderInput" id="fileUploaderInputInspections" type="file" accept="image/jpg,image/jpeg" @change="processPhoto">
        <label for="cameraUploaderInputInspections" style="margin-bottom:10px;" class="bgms-button btn" v-if="takingPhotoSupported"><span class="glyphicon glyphicon-camera"></span>  Take a Photo</label>
        <input ref="cameraUploaderInput" id="cameraUploaderInputInspections" type="file" accept="image/*" capture @change="processPhoto">
      </div>
      <div v-if="storageTooSmallForImageUpload" class="sidebar-notice">
        <i class="fa fa-exclamation-triangle" aria-hidden="true"></i> You are running out of storage space on your device! Uploading images is no longer available. Please synchronise or clear up space on your device.
      </div>
      <div v-if="photo">
        <img :src="photo" />
        <button class="sidebar-normal-button bgms-button" id="remove-button" type="button" @click="removePhoto">Remove image</button>
      </div>
      <button class="btn sidebar-normal-button bgms-button" type="submit" :disabled="photoProcessing">Save</button>
      <button class="btn sidebar-normal-button bgms-button" type="button" @click="formCancel">Cancel</button>
    </form>

    <div v-show="loadingInspections" class="mc-spinner">
      <i class="fa fa-spinner fa-spin"/>
      <p>Loading inspections</p>
    </div>
    <table v-show="!loadingInspections" class="table inspection-table">
      <thead>
        <tr>
          <th title="Condition">Structure Cond.</th>
          <th title="Condition">Inscription Cond.</th>
          <th title="Action Required?">Action Req.?</th>
          <th>Remarks</th>
          <th>Image</th>
        </tr>
      </thead>
      <tbody id="inspection-list" v-if="inspectionsOffline">
        <tr>
          <td colspan="4" class="sidebar-notice">
            <i class="fa fa-exclamation-triangle" aria-hidden="true"></i> Inspections are not available to view while offline.
          </td>
        </tr>
      </tbody>
      <tbody id="inspection-list" v-else-if="totalSWAndBGMSQueueLength > 0">
        <tr>
          <td colspan="4" class="sidebar-notice">
            <i class="fa fa-exclamation-triangle" aria-hidden="true"></i> Unsynchronised inspections are not yet viewable.
          </td>
        </tr>
      </tbody>
      <tbody id="inspection-list" v-else-if="inspections.length === 0">
        <tr>
          <td colspan="4">No inspections recorded.</td>
        </tr>
      </tbody>
      <tbody id="inspection-list" v-else-if="inspections.length > 0">
        <template style="width: 100%;" v-for="inspection in inspections">
          <tr class="table-date-heading" :key="inspection.id">
            <td colspan="4">{{ inspection.date }}</td>
          </tr>
          <tr :key="inspection.id">
            <td class="table-row-bottom">{{ interpretCondition(inspection.condition) }}</td>
            <td class="table-row-bottom">{{ interpretInscription(inspection.inscription) }}</td>
            <td class="table-row-bottom">{{ interpretActionRequired(inspection.action_required) }}</td>
            <td class="table-row-bottom">{{ inspection.remarks }}</td>
            <td class="table-row-bottom">
              <div v-if="inspection.image && inspection.image.image_url" v-viewer="{navbar: 0, title: 0, toolbar: { zoomIn:4,zoomOut:4,oneToOne:4,reset:4 }, url: (image) => {return image.getAttribute('data-image-url')}}">
                <a style="position: relative" href="javascript:void(0)">
                  <div class="mc-spinner image-loading-spinner">
                    <i class="fa fa-spinner fa-spin"/>
                  </div>
                  <img class="image-thumbnail" :data-image-url="inspection.image.image_url" :src="inspection.image.thumbnail_url" :alt="'Inspection: ' + inspection.date"/>
                </a>
              </div>
              <div v-else-if="inspection.image">
                <img class="image-thumbnail" :src="inspection.image"/>
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex';
import Component, { mixins } from 'vue-class-component'
import { Watch, Prop } from 'vue-property-decorator'
import axios from 'axios'
import 'viewerjs/dist/viewer.css';
import Viewer from 'v-viewer';
import { messages } from '@/global-static/messages.js';
import PhotoProcessing from './../../../mixins/photoProcessing'

Vue.use(Vuex);
Vue.use(Viewer);

/**
 * Class representing Inspections component
 * @extends PhotoProcessing mixin
 */
@Component
export default class Inspections extends mixins(PhotoProcessing) {
  photoProcessing: boolean = false;
  addNewInspection: boolean = false;
  loadingInspections: boolean = false
  inspectionsOffline: boolean = false;

  notificationHelper: any = this.$store.getters.notificationHelper;
  offlineService: any = this.$store.getters.offlineService;
  siteAdminOrSiteWarden: boolean = this.$store.state.siteAdminOrSiteWarden;

  condition: number = 1;
  inscription: number = 1;
  remarks: string = "";
  actionRequired: boolean = false;

  photo: string = null;

  @Prop()
  takingPhotoSupported: boolean;

  /*** Watchers ***/

  /**
   * Watcher: When the selected memorial is changed, this loads existing inspections
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('memorial', { immediate: true})
  onMemorialChanged(val: any, oldVal: any) {
    if (val === oldVal || !val){
      return;
    }

    let v = this;
    v.loadingInspections = true;

    if(v.online) {
      // Get the existing inspections for the memorial
      axios.get('/mapmanagement/memorialInspection/?memorial_uuid=' + val.getId())
        .then(function(response) {
          for (let inspection of response.data) {
            v.$store.commit('addInspection', inspection);
          }
          v.loadingInspections = false;
        })
        .catch(function(response) {

          // Service worker responds with {offline: true}
          if (response.data && response.data.offline) {
            // This is just a precaution. This state should be automatically changed if network status changes.
            v.$store.commit('updateOnline', false);
            return;
          }

          v.loadingInspections = false;
          console.warn('[MemorialCaptureSidebar/Inspections] Couldn\'t get memorial inspections:', response);
        });
    }
    else {
      v.inspectionsOffline = true;
      v.loadingInspections = false;
    }
  }

  /**
   * Watcher: when new data is entered or unsaved data is saved
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('addNewInspection', { immediate: true})
  onInspectionChanged(val: any, oldVal: any) {
    this.$store.commit('toggleUnsavedInspection', val);
  }

  /**
   * Watcher: When the online status changes, this loads photos for memorial if they haven't previously been loaded
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('online', { immediate: false})
  onOnlineChanged(val: any, oldVal: any) {
    // reload photos if we have just come online
    if (val && this.inspections.length === 0)
      this.onMemorialChanged(this.$store.state.MemorialSidebar.memorial,null);
      this.inspectionsOffline = false;
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
   * Computed property: Get existing inspections
   * @returns {any} Existing inspections
   */

  get inspections() {
    return this.$store.state.MemorialCaptureSidebar.inspections;
  }

  /**
   * Used by mixin to retrieve vue instance
   */
  get vueInstance() {
    return this;
  }

  /**
   * Computed property: Get total SW and BGMS queue length
   * @returns {number}
   */
  get totalSWAndBGMSQueueLength(): number {
    return this.offlineService.bgmsQueueLength + this.$store.state.Offline.swQueueLength;
  }

  /**
   * Computed property: Get inspectionCollapsed
   * @returns {boolean} True if this section should be collapsed
   */
  get collapsed(): boolean {
    return this.$store.state.MemorialCaptureSidebar.inspectionCollapsed;
  }

  /**
   * Computed property: true if further image uploads must be disallowed because storage is too small
   * @returns {boolean}
   */
  get storageTooSmallForImageUpload(): boolean {
    return this.$store.getters.storageTooSmallForImageUpload;
  }

  /*** Methods ***/

  /**
   * Display photo and show remove button
   * @param {any} photo: the processed photo ready for uploading
   */
  processPhotoPart2(photo) {
    this.photo = photo;
    this.photoProcessing = false;
  }

  /**
  * Remove the selected photo
  */
  removePhoto() {
    this.photo = null;
  }

  /**
   * Cancel new inspection
   */
  formCancel() {
    this.resetForm();
    this.addNewInspection = false
  }

  /**
   * Reset the form
   */
  resetForm()
  {
    this.condition = 1;
    this.inscription= 1;
    this.remarks = "";
    this.actionRequired = false;
    this.removePhoto();
  }

  /**
   * If online: saves change to server.
   * If offline: adds change to service worker queue.
   * Updates table if successful.
   */
  onSubmit(e) {
    //debugger; // eslint-disable-line no-debugger
    e.preventDefault();

    let v = this;
    let photoToUpload = this.photo;

    if(photoToUpload)
      photoToUpload = photoToUpload.replace("data:image/jpeg;base64,", "")

    debugger; // eslint-disable-line no-debugger
    const [onlyDate] = new Date().toISOString().split('T');
    let postData = {
      "memorial": this.memorial.getId(),
      "condition": this.condition,
      'inscription':this.inscription,
      "remarks": this.remarks,
      "action_required": this.actionRequired,
      "date": onlyDate,
      "imageBase64": photoToUpload
    };

    axios.post('/mapmanagement/memorialInspection/', postData)
      .then(function (response) {
        console.log(response);
        v.notificationHelper.createSuccessNotification(messages.inspection.save.success.title);

        //show new record
        if (response.data) {  // i.e. the data was saved to the server
          v.$store.commit('addInspection', response.data);
        }
        else {  // i.e. data added to sw queue
          delete postData["imageBase64"];
          postData["image"] = v.photo;
          v.$store.commit('addInspection', postData);
        }

        //close form
        v.formCancel();
      })
      .catch(function (error) {
        console.log(error);
        v.notificationHelper.createErrorNotification(messages.inspection.save.fail.title);
      });
  }

  /**
   * Deletes an inspection.
   * @param {any} inspection: inspection to be deleted
   */
  /*deleteMemorialInspection(inspection) {

    let v = this;

    let postData = {
      "id": inspection.id,
      "queue_id": inspection.queue_id
    }

    axios.delete('/mapmanagement/memorialInspection/', { params: postData })
      .then(function (response) {
        console.log(response);
        v.notificationHelper.createSuccessNotification(messages.inspection.delete.success.title);

        //remove record
        v.$store.commit('removeInspection', inspection);
      })
      .catch(function (error) {
        console.log(error);
        v.notificationHelper.createErrorNotification(messages.inspection.delete.fail.title);
      });
  }*/

  /**
   * Maps conditions
   * @param {number} condition: inspection to be deleted
   * @returns {string}
   */
  interpretCondition(condition: number): string {
    if (condition === 1)
      return "Good";
    else if (condition ===2)
      return "Reasonable";
    else
      return "Poor";
  }
   /**
   * Maps inscription
   * @param {number} inscription: inspection to be deleted
   * @returns {string}
   */
  interpretInscription(inscription: number): string {
    if (inscription === 1)
      return "Good";
    else if (inscription === 2)
      return "Reasonable";
    else 
      return "Poor";
  }
  /**
   * Maps action required
   * @param {boolean} actionRequired: inspection to be deleted
   * @returns {string}
   */
  interpretActionRequired(actionRequired: boolean): string {
    if (actionRequired)
      return "Yes";
    else
      return "No";
  }

  /**
   * @returns {string} Today's date
   */
  getTodaysDate(): string {
    let today = new Date();
    let options = { day: 'numeric', month: 'short', year: 'numeric' };

    return today.toLocaleDateString('en-GB', options);
  }
}
</script>
