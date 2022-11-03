<template>
  <div style="width: 100%">
    <div class="photo-buttons" v-if="memorialPhotographyAccess && !storageTooSmallForImageUpload">
      <label for="fileUploaderInput" class="bgms-button btn">Add a Photo</label>
      <input ref="fileUploaderInput" id="fileUploaderInput" type="file"  accept="image/jpg,image/jpeg" multiple @change="processPhoto">
      <label for="cameraUploaderInput" class="bgms-button btn" v-if="takingPhotoSupported"><span class="glyphicon glyphicon-camera"></span>  Take a Photo</label>
      <input ref="cameraUploaderInput" id="cameraUploaderInput" type="file"  accept="image/*" capture @change="processPhoto">
    </div>
    <div v-if="memorialPhotographyAccess && storageTooSmallForImageUpload" class="sidebar-notice">
      <i class="fa fa-exclamation-triangle" aria-hidden="true"></i> You are running out of storage space on your device! Uploading images is no longer available. Please synchronise or clear up space on your device.
    </div>
    <div v-show="photoProcessing" class="mc-spinner"><i class="fa fa-spinner fa-spin"></i></div>
    <!-- Display the photos -->
    <div v-if="loadingSavedPhotos" class="loading-placeholder">
      <div class="mc-spinner loading-placeholder-contents">
        <i class="fa fa-spinner fa-spin"/>
        <p>Loading photos</p>
      </div>
    </div>
    <div v-if="photos && photos.length > 0" id="photoThumbnails" v-viewer="{title: 0, toolbar: { zoomIn:4,zoomOut:4,oneToOne:4,reset:4,prev:4,next:4,rotateLeft:4,rotateRight:4 }, url: (image) => {return image.getAttribute('data-image-url')}}">
      <span v-for="(photo, i) in photos" class="savedImage" :key="i">
        <span v-if="memorialPhotographyAccess" @click="deletePhoto(photo, i)" class="fa fa-times-circle closethumb"></span>
        <a style="position: relative" href="javascript:void(0)">
          <div class="mc-spinner image-loading-spinner">
            <i class="fa fa-spinner fa-spin"/>
          </div>
          <img v-if="photo.thumbnail_url" class="image-thumbnail" :data-image-url="photo.image_url" :src="photo.thumbnail_url"  :alt="'Memorial Image ' + (i + 1)"/>
          <img v-else class="image-thumbnail" :data-image-url="photo.image_url" :src="photo.image_url"  :alt="'Memorial Image ' + (i + 1)"/>
        </a>
      </span>
    </div>
    <div v-else-if="!photoProcessing && !loadingSavedPhotos" class="blank-form-placeholder">
      No photos recorded.
    </div>
    <!-- Warn user when offline -->
    <div v-if="!online && totalImageCount > 0" class="sidebar-notice">
      <i class="fa fa-exclamation-triangle" aria-hidden="true"></i> This memorial has <b>{{ totalImageCount }}</b> image<i v-if="totalImageCount > 1">s</i>, however you may not be able to view images as you are offline.
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Vuex from 'vuex'
import Component, { mixins } from 'vue-class-component'
import { Watch, Prop } from 'vue-property-decorator'
import axios from 'axios'
import 'viewerjs/dist/viewer.css';
import Viewer from 'v-viewer';
import { messages } from '@/global-static/messages.js';
import PhotoProcessing from '@/mapmanagement/mixins/photoProcessing'
import { VISUALISATIONENUM, showMemorialIndicatorForSingleMemorial } from '@/mapmanagement/components/Map/models/Memorial';

Vue.use(Vuex);
Vue.use(Viewer)

/**
 * Class representing Photos component
 * @extends PhotoProcessing mixin
 */
@Component
export default class Photos extends mixins(PhotoProcessing) {
  photoProcessing: boolean = false;
  loadingSavedPhotos = false;

  notificationHelper: any = this.$store.getters.notificationHelper;
  offlineService: any = this.$store.getters.offlineService;
  memorialPhotographyAccess: boolean = this.$store.state.memorialPhotographyAccess;

  offlineServiceImageCount: number = 0;

  @Prop() takingPhotoSupported: boolean;
  @Prop() updateMemorialIndicators: boolean;

  /**
   * Vue mounted lifecycle hook
   * - Set offlineServiceImageCount
   * - Listens for bootstrap events fired when section is collapsed/opened
   */
  mounted() {
    this.updateOfflineServiceImageCount(this.memorial);
  }

  /*** Watchers ***/

  /**
   * Watcher: When the selected memorial is changed, this loads photo
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('memorial', { immediate: true})
  onMemorialChanged(val: any, oldVal: any) {
    if (val === oldVal || !val){
      return;
    }

    this.$store.commit('resetPhotos');

    this.loadingSavedPhotos = true;
    this.updateOfflineServiceImageCount(val);
    // Get the existing photos for the memorial
    axios.get('/mapmanagement/getMemorialImages/?id=' + val.getId())
      .then(response => {
        // this stops photos being added to the wrong memorial if the memorial is changed again
        if (val != this.memorial)
          return;

        this.addPhotosToStore(response.data);
        this.loadingSavedPhotos = false;
      })
      .catch(response => {
        if (response.response) {
          let data = response.response.data;
          // Service worker responds with {offline: true}
          if (data && ((data.length > 0 && data[0].offline) || data.offline)) {
            // This is just a precaution. This state should be automatically changed if network status changes.
            this.$store.commit('updateOnline', false);
          }

          // if response contains data from indexeddb queue_id
          if (data && data.length > 1)
          {
            // this stops photos being added to the wrong memorial if the memorial is changed again
            if (val != this.memorial)
              return;

            this.addPhotosToStore(data.slice(1));
          }
            else
              console.warn('[MemorialCaptureSidebar/Photos] Couldn\'t get memorial images:', response);
        }
        this.loadingSavedPhotos = false;
      });

      // if photos in the offline service queue, these need loaded seperately
      if (this.offlineServiceImageCount && this.offlineServiceImageCount > 0) {
        for(let i = 0; i < this.offlineServiceImageCount; i++) {
          //queuedMemorialPhotosPrimaryKeys contains array of primary keys
          this.offlineService.getItemsByPrimaryKey(this.offlineService.queuedMemorialPhotosPrimaryKeys[this.memorial.getId()][i])
          .then(item => {
            item.image_url = "data:image/jpeg;base64," + item.image;
            delete item.image;
            item.offline_service = true;

            // this stops photos being added to the wrong memorial if the memorial is changed again
            if (val != this.memorial)
              return;

            this.addPhotosToStore([item]);
          });
        }
      }
  }

  /**
   * Watcher: When the online status changes, this loads photos for memorial if they haven't previously been loaded
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('online', { immediate: false})
  onOnlineChanged(val: any, oldVal: any) {
    // reload photos if we have just come online
    if (val && this.photos.length !== this.totalImageCount) {
      this.$store.commit('resetPhotos');
      this.onMemorialChanged(this.$store.state.MemorialSidebar.memorial,null);
    }
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
   * Computed property: Get the memorial's photos
   * @returns {any} photos
   */
  get photos() {
    return this.$store.state.MemorialCaptureSidebar.photos;
  }

  /**
   * Computed property: Get online status
   * @returns {boolean} True if online
   */
  get online(): boolean {
    return this.$store.state.Offline.online;
  }

  /**
   * Computed property: Used by mixin to retrieve vue instance
   */
  get vueInstance() {
    return this;
  }

  /**
   * Computed property: Get total number of images including those in the offline service queue
   * (which are not included in 'images_count' for some reason)
   * @returns {number}
   */
  get totalImageCount(): number {
    return this.$store.getters.imageCount + (this.offlineServiceImageCount);
  }

  /**
   * Computed property: true if further image uploads must be disallowed because storage is too small
   * @returns {boolean}
   */
  get storageTooSmallForImageUpload(): boolean {
    return this.$store.getters.storageTooSmallForImageUpload;
  }

  /*** Methods ***/

  stopSidebarClose(stop: boolean) {
    this.$store.commit('toggleStopSidebarClose', stop);
  }

  /**
   * If online: uploads photo to server.
   * If offline: adds photo to service worker queue.
   * Apologies for the complexity of this process. With more time it could be much improved!
   * @param {any} photoToUpload: the processed photo ready for uploading
   * @param {any} thumbnail: thumbnail read for display on page
   * @param {any} memorial: memorial this photo is to be added to
   * @param {any} lastPhoto: true if this is the last photo in this upload
   */
  processPhotoPart2(photoToUpload, memorial, lastPhoto) {
    this.photoProcessing = true;

    let memorialID = memorial.getId();
    let url = '/mapmanagement/takePhoto/';
    let postData = {
      memorial_id: memorialID,
      image: photoToUpload.replace("data:image/jpeg;base64,", "")
    };

    // If auto image uploading is turned on, send to server, else, store in DB
    if(this.offlineService.autoImageUpload) {
      axios.post(url, postData)
      .then(response => {
        this.notificationHelper.createSuccessNotification(messages.memorialImages.upload.success.title);
        this.modifyImageCount(memorial, 1);

        // if this is still the selected memorial
        if (memorialID === this.memorial.getId()) {
          // Add photo to list
          this.photos.push({
            'id': response.data.uuid,
            'image_url': photoToUpload,
            'queueKey': response.data.queueKey
          });
        }
        else if (this.updateMemorialIndicators)
          showMemorialIndicatorForSingleMemorial(VISUALISATIONENUM.image, memorial, memorial.get('marker_type'));

        // Clean up
        photoToUpload = null;

        if (lastPhoto)
          this.cleanupUpload();
      })
      .catch(response => {
        this.notificationHelper.createErrorNotification(messages.memorialImages.upload.fail.title);
        this.modifyImageCount(memorial, -1);

        if (lastPhoto)
          this.cleanupUpload();
      });
    } else {
      const image = {
        uuid: memorialID,
        url: url,
        data: postData,
      };
      this.offlineService.addToQueue(image)
      .then(key => {
        this.notificationHelper.createSuccessNotification(messages.memorialImages.upload.success.title);
        this.updateOfflineServiceImageCount(memorial);

        // if this is still the selected memorial
        if (memorialID === this.memorial.getId()) {
          this.photos.push({
            'id': null,
            'image_url': photoToUpload,
            'offline_service': true,
            'queueKey': key
          });
        }
        else if (this.updateMemorialIndicators)
          showMemorialIndicatorForSingleMemorial(VISUALISATIONENUM.image, memorial, memorial.get('marker_type'));

        // Clean up
        photoToUpload = null;

        if (lastPhoto)
          this.cleanupUpload();
      })
      .catch(() => {
        this.notificationHelper.createErrorNotification(messages.memorialImages.upload.fail.title);
        this.modifyImageCount(memorial, -1);

        if (lastPhoto)
          this.cleanupUpload();
      });
    }
  }

  cleanupUpload() {
    this.photoProcessing = false;
    this.stopSidebarClose(false);
  }

  /**
   * Deletes a photo
   * @param {any} photo - photo to be deleted
   * @param {number} posInArray - photo's position in the photos array
   */
  deletePhoto(photo, posInArray: number){
    let v = this;
    v.notificationHelper.createConfirmation(messages.memorialImages.delete.confirmation.title, messages.memorialImages.delete.confirmation.text, function() {
      let postData = {
        memorial_uuid: v.memorial.getId()
      };
      if (photo.id)
        postData['image_uuid'] = photo.id;
      else if (photo.queueKey)
        postData['queue_id'] = photo.queueKey;

      // if photo is from server or sw queue
      if (!photo.offline_service) {
      axios.post('/mapmanagement/deleteMemorialImage/', postData)
        .then(function(response) {
          v.modifyImageCount(v.memorial, -1);
          v.photoDeletedSuccessfully(posInArray, v.memorial);
        })
        .catch(function(response) {
          v.notificationHelper.createErrorNotification(messages.memorialImages.delete.fail.title);
          console.error('[Photos] Unable to delete image:', response);
        })
      }
      //if photo is from offline service queue
      else {
        v.offlineService.deleteFromQueue(v.memorial.getId(), photo.queueKey, '/mapmanagement/takePhoto/')
        .then(function(response) {
          v.updateOfflineServiceImageCount(v.memorial);
          v.photoDeletedSuccessfully(posInArray, v.memorial);
        })
        .catch(function(response) {
          v.notificationHelper.createErrorNotification(messages.memorialImages.delete.fail.title);
          console.error('[Photos] Unable to delete image:', response);
        });
      }
    });
  }

  /**
   * Called after a photo has been deleted
   * @param {number} posInArray - photo's position in the photos array
   */
  photoDeletedSuccessfully(posInArray: number, memorial) {
    this.notificationHelper.createSuccessNotification(messages.memorialImages.delete.success.title);

    // Remove photo from list
    this.$store.commit('removePhoto', posInArray);

    if (this.updateMemorialIndicators)
      showMemorialIndicatorForSingleMemorial(VISUALISATIONENUM.image, memorial, memorial.get('marker_type'));
  }

  /**
   * Modify memorial's image count
   * @param {any} memorial
   * @param {number} i - what to add on to the existing image count
   */
  modifyImageCount(memorial, i:number) {
    let image_count = memorial.get("images_count");

    if (image_count)
      memorial.set("images_count", image_count + i);
    else // undefined
      memorial.set("images_count", i);
  }

  /**
   * Update memorial's offline service queue image count
   * @param {any} memorial
   */
  updateOfflineServiceImageCount(memorial) {
    if (this.memorial) {
      let queuedMemorialPhotos = this.offlineService.queuedMemorialPhotosPrimaryKeys[this.memorial.getId()];
      if (memorial === this.memorial && queuedMemorialPhotos)
        this.offlineServiceImageCount = queuedMemorialPhotos.length;
    }
  }

  /**
   * Add photos to store
   * @param {any} photos - array of json objects containing photo data
   */
  addPhotosToStore(photos) {
    for(let i = 0; i < photos.length; i++) {
      this.$store.commit('addPhoto', photos[i]);
    }
  }
}
</script>
