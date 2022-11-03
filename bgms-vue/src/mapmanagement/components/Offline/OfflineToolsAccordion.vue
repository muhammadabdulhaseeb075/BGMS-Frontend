<template>
  <div id="v-VueOfflineController" data-html2canvas-ignore="true" v-if="!isBacasEnabled">
    <div id="offlineToolsAccordion" class="offline-left-button">
      <button v-if="swSupported || indexedDBSupported" class="btn sidebar-normal-button btn-bgms btn-right-toolbar" aria-label="Left Align" title="Offline Tools" data-toggle="collapse" data-parent="#offlineToolsAccoridion" href="#offlineIndicators">
        <span class="icon-Globe" :class="[ online ? 'online' : 'offline', downloadingFilesForOffline ? 'fa fa-spin' : '' ]"></span>
        <!--<span class="icon-Globe" :class="[ online ? 'online' : 'offline' ]"></span>-->
      </button>

      <div id="queueCount" v-if="swQueueLength || bgmsQueueLength" data-toggle="collapse" data-parent="#offlineToolsAccoridion" href="#offlineIndicators">
        {{ swQueueLength + bgmsQueueLength }}
      </div>

      <div id="offlineIndicators" class="panel-collapse collapse">

        <div class="panel panel-default">
          <div class="panel-heading">
            Offline Mode:  {{ offlineReady ? 'ACTIVE' : swSupported && swInControl ? 'AVAILABLE' : 'UNAVAILABLE' }}
          </div>
          <div class="panel-body">
            <span v-if="!swSupported">
              You may need to upgrade your browser if you wish to use BGMS while disconnected from the internet!
            </span>

            <div v-if="swSupported && swInControl && online && !swQueueLength">
              <span>You are <span class="online">online</span>!<span v-if="offlineReady"> Offline mode is ready if you disconnect from the internet.</span></span>
            </div>

            <span v-if="offlineReady && (!online || swQueueLength)">
              You are <span :class="[ online ? 'online' : 'offline' ]">{{ online ? 'online' : 'offline' }}</span>! Any changes you make will be saved on your device, and can be synchronised when connected to the internet.
            </span>

            <span v-if="swSupported && swInControl && !offlineReady && !online">
              You are <span class="offline">offline</span>! Offline mode has not been activated, so functionality will be limited.
            </span>

            <span v-if="swSupported && quotaTooSmall">
              Offline mode is not possible as you do not have enough storage available on your device.
            </span>

            <div v-if="swSupported && swInControl" class="download-data">
              <div class="download-data-left">Download data to activate offline mode: </div>
              <div class="slideThree download-data-right" v-show="online && (!swQueueLength || swQueueLength === 0)">
                <input id="downloadData" type="checkbox" v-model="saveDataForOffline" hidden>
                <label for="downloadData"></label>
              </div>
              <div class="download-data-right" v-show="!online || swQueueLength > 0">
                <span>{{saveDataForOffline ? "ON" : "OFF"}}</span>
              </div>
            </div>

            <div class="loading-spinner" v-if="swSupported && (!swInControl || downloadingFilesForOffline) && !quotaTooSmall">
              <i class="fa fa-spinner fa-spin"/>
              <p v-if="!swInControl">Downloading the files required to make offline mode available, please wait!</p>
              <p v-if="downloadingFilesForOffline">Downloading the files required to work while offline, please wait!</p>
            </div>

          </div>
        </div>

        <div class="panel panel-default" v-if="indexedDBSupported">
          <div class="panel-heading">
            Delay Image Uploads
            <div class="slideThree" @click="toggleDelayImageUploads" v-show="isNaN(estimateQuotaAvailableMB) || (estimateQuotaAvailableMB>=queuesMinimumMB)">
              <input ng-attr-id="delayImageUpload" type="checkbox" v-model="delayImageUpload" hidden>
              <label ng-attr-for="delayImageUpload"></label>
            </div>
          </div>
          <div class="panel-body">

            <span v-if="isNaN(estimateQuotaAvailableMB) || (estimateQuotaAvailableMB>=queuesMinimumMB)">
              <span v-if="!delayImageUpload">
                On slow or mobile connections, you may want to turn this on.
              </span> Images will be stored on your device until you choose to upload them.
            </span>
            <span v-else>
              This feature is not currently available as you do not have enough storage available on your device.
            </span>

          </div>
        </div>

        <Sync v-if="bgmsQueueLength > 0 || swQueueLength > 0"/>

      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Component, { mixins } from 'vue-class-component'
import { Watch } from 'vue-property-decorator'

import Sync from './Sync.vue'
import ServiceWorkerTools from './../../mixins/serviceWorkerTools'
import DatabaseTools from './../../mixins/databaseTools'

/**
 * Class representing Offline component
 * @extends Vue
 */
@Component({
 components: {
   Sync
 }
})
export default class Offline extends mixins(ServiceWorkerTools, DatabaseTools){

  offlineService: any = this.$store.getters.offlineService;
  notificationHelper: any = this.$store.getters.notificationHelper;

  swInstalled: boolean = false;
  swSynchronising: boolean = false;

  quotaMB: number = 0;
  quotaTooSmall = false;

  swInstallMiniumumMB: number = this.$store.state.Offline.swInstallMiniumumMB;
  queuesMinimumMB: number = this.$store.state.Offline.queuesMinimumMB;

  saveDataForOffline: boolean = null;

  aerialLayerWhileOffline = null;
  baseLayerWhileOffline = null;

   /**
    * Vue mounted lifecycle hook
    */
  mounted() {
    let v = this;

    v.setOnlineStatus();
    // If the user goes online/offline this will update vuex state
    window.addEventListener('online', v.setOnlineStatus);
    window.addEventListener('offline', v.setOnlineStatus);

    // Detect if Service Workers and indexeddb are supported
    if ('serviceWorker' in navigator && 'indexedDB' in window && 'caches' in window) {
      console.log("Offline requirements met.");    
      v.swSupported = true;
      v.indexedDBSupported = true;
    } else if ('indexedDB' in window) {
      console.log("No serviceWorker/Cache but Db available.");
      v.indexedDBSupported = true;
    }

    if (v.swSupported) {
      // only register sw if quota is greater than 100mb
      this.storageEstimateWrapper()
      .then(function(estimate) {
        //updates the estimate of how much storage is available
        v.$store.commit('updateEstimateQuotaAvailableMB', estimate);
        v.quotaMB = v.estimateQuotaAvailableMB;

        // only install service worker if there is adequate storage available or if it is already registered
        if (isNaN(v.quotaMB) || v.quotaMB >= v.swInstallMiniumumMB || navigator.serviceWorker.controller)
        {
          // Only register the service worker when the window has finished loading
          if(document.readyState === "complete") {
            v.initiateServiceWorker();
          } else {
            window.addEventListener("load", function(e) {
              v.initiateServiceWorker();
            });
          }
        }
        else
          v.quotaTooSmall = true;
      });
    }

    // Get the current autoImageUpload setting from the database, if present
    // Notice: this is the opposite of delayImageUpload!
    v.offlineService.getSetting('autoImageUpload')
      .then(function(setting) {
        if(setting) {
          v.delayImageUpload = !setting.value;
        }
      })
      .catch(function(error) {
        console.error('[offlineController] Error getting the setting from the database', error);
      });

    // Get the current downloadFilesForOffline setting from the database, if present, otherwise false
    v.offlineService.getSetting('downloadFilesForOffline')
      .then(function(setting) {
        if(setting)
          v.saveDataForOffline = setting.value;
        else
          // Default is false.
          v.saveDataForOffline = false;
      })
      .catch(function(error) {
        console.error('[offlineController] Error getting the setting from the database', error);
      });
  }

  /*** Computed ***/

  //Return true if site is using BACAS API integration
  get isBacasEnabled(): boolean {
    return this.$store.state.isBacasEnabled;
  } 

  /**
   * Get serviceWorkerSupported
   * @returns {boolean}
   */
  get swSupported(): boolean {
    return this.$store.state.Offline.serviceWorkerSupported;
  }
  /**
   * Set serviceWorkerSupported
   * @param {boolean} value True if service workers supported
   */
  set swSupported(value: boolean) {
    this.$store.commit('updateServiceWorkerSupported', value);
  }

  /**
   * Get swInControl
   * @returns {boolean}
   */
  get swInControl(): boolean {
    return this.$store.state.Offline.swInControl;
  }
  /**
   * Set swInControl
   * @param {boolean} value True if service worker in control
   */
  set swInControl(value: boolean) {
    this.$store.commit('updateSwInControl', value);
  }

  /**
   * Get indexedDBSupported
   * @returns {boolean}
   */
  get indexedDBSupported(): boolean {
    return this.$store.state.Offline.indexedDBSupported;
  }
  /**
   * Set indexedDBSupported
   * @param {boolean} value True if indexeddb supported
   */
  set indexedDBSupported(value: boolean) {
    this.$store.commit('updateIndexedDBSupported', value);
  }

  /**
   * @returns {boolean} True if offline functionality is ready to be used
   */
  get offlineReady(): boolean {
    const returnValue: boolean = this.swSupported && this.swInControl && this.dataForOfflineSaved;

    if (returnValue)
      this.notificationHelper.createSuccessNotification("Ready to work offline!");

    return returnValue;
  }

  /**
   * Computed property: Get online status
   * @returns {boolean} True if online
   */
  get online(): boolean {
    return this.$store.state.Offline.online;
  }
  /**
   * Set online status
   * @param {boolean} value True if online
   */
  set online(value: boolean) {
    if (!value) {
      this.turnAerialOff();
      this.turnBaseOff();
    }
    else {
      if (this.aerialLayerWhileOffline)
        this.turnAerialOn();
      if (this.baseLayerWhileOffline)
        this.turnBaseOn();
    }
    this.$store.commit('updateOnline', value);
  }

  /**
   * @returns {number} - number of items in SW queue
   */
  get swQueueLength(): number {
    return this.$store.state.Offline.swQueueLength;
  }
  /**
   * Set swQueueLength
   * @param {number}
   */
  set swQueueLength(value: number) {
    this.$store.commit('updateSWQueueLength', value);
  }

  /**
   * @returns {number} - number of items in BGMS queue
   */
  get bgmsQueueLength(): number {
    return this.offlineService.bgmsQueueLength;
  }

  /**
   * @returns {boolean} - true if enabled
   */
  get delayImageUpload(): boolean {
    return !this.offlineService.autoImageUpload;
  }
  /**
   * @param {boolean} value - true if enabled
   */
  set delayImageUpload(value: boolean) {
    this.offlineService.autoImageUpload = !value;
  }

  /**
   * @returns {boolean}
   */
  get syncInProgress(): boolean {
    return this.$store.state.Offline.swQueueLength;
  }

  /**
   * @returns {number} - estimated storage available
   */
  get estimateQuotaAvailableMB(): number {
    let returnValue: number = this.$store.state.Offline.estimateQuotaAvailableMB;

    if (!this.syncInProgress) {
      // if we need to disable turning delayImageUpload off
      if (!this.delayImageUpload && returnValue && !isNaN(returnValue) && returnValue<=this.queuesMinimumMB)
      {
        this.delayImageUpload = true;
        this.notificationHelper.createInfoNotification("Delay Image Uploads", "Delay Image Uploads has been disabled as you do not have enough storage space available to store images on your device. Please synchronise or clear up space on your device.");
      }

      // if we need to disable uploading images with SW
      if (this.swInControl && this.swQueueLength > 0 && !isNaN(returnValue) && returnValue<=this.queuesMinimumMB)
      {
        this.notificationHelper.createInfoNotification("Offline Mode", "You are running out of storage space on your device! Uploading images is no longer available. Please synchronise or clear up space on your device.");
      }
    }

    return returnValue;
  }

  /*** Watchers ***/

  /**
   * Watcher: When the service worker is in control, download mandatory data
   * @param {boolean} val
   * @param {boolean} oldVal
   */
  @Watch('swInControl')
  onSWInControl(val: boolean, oldVal: boolean) {
    let v = this;

    if (v.online && v.swQueueLength === 0 && v.saveDataForOffline && !v.dataForOfflineSaved && !v.downloadingFilesForOffline) {
      v.downloadFilesForOffline();
    }
  }

  /**
   * Watcher: Download/remove optional files when toggle is changed
   * @param {boolean} val
   * @param {boolean} oldVal
   */
  @Watch('saveDataForOffline')
  onDownloadFiles(val: boolean, oldVal: boolean) {
    let v = this;

    // reasons not to update data, i.e. sw not yet activated
    if (val === null || ((!v.online || v.swQueueLength !== 0) && !val) || !v.swInControl)
      return;
    else if ((!v.online || v.swQueueLength !== 0) && val) {
      // If offline or a queue, then val will have been changed from settings.
      // Hence can assume data is already in indexed.
      v.dataForOfflineSaved = true;
    }
    else if (val) {
      v.downloadFilesForOffline();
      v.offlineService.setSetting('downloadFilesForOffline', true);
    }
    else {
      if (v.downloadingFilesForOffline) {
        // cancel downloading files
        v.cancelDownloadFilesForOffline = true;
      }
      v.removeDataForOffline()
      .then(() => {
        v.dataForOfflineSaved = false;
        v.offlineService.setSetting('downloadFilesForOffline', false);
      });
    }
  }

  @Watch('offlineReady', { immediate: true })
  onOfflineReady(val: boolean, oldVal: boolean) {
    this.$store.commit('updateOfflineReady', val);
  }

  /**
   * Tell service worker that persons are saved in Indexeddb
   */
  @Watch('dataForOfflineSaved')
  onDataForOfflineSaved(val: boolean, oldVal: boolean) {
    this.sendMessageToServiceWorker({
      type: "dataSavedInIndexedDB",
      value: val
    });
  }

  /*** Methods ***/

  initiateServiceWorker() {
    let v = this;

    console.debug('[offlineController] Checking SW are supported');
    if(v.swSupported) {

      // Registers the service worker and then gets the status and queue length
      // NOTE: 'register' is a no-op if the service worker already exists but it still triggers the .then()
      console.debug('[offlineController] Registering SW');
      navigator.serviceWorker.register("/sw.js").then(function(reg) {
        console.debug('[offlineController] SW registered');

        // Detects if the SW is in control of the page
        if (!navigator.serviceWorker.controller) {
          console.warn('[offlineController] SW not in control of page. It may be in the process of installing or waiting to activate.');
          v.swInControl = false;
        } else {
          console.debug('[offlineController] A SW is in control of this page. Getting the online/offline status from it.');
          v.swInControl = true;
          v.setSWQueueLength();
        }

        let serviceWorker;
        if (reg.installing) {
          serviceWorker = reg.installing;
          v.swInstalled = false;
        } else if (reg.waiting) {
          serviceWorker = reg.waiting;
          v.swInstalled = true;
        } else if (reg.active) {
          serviceWorker = reg.active;
          v.swInstalled = true;
        }

        if (serviceWorker) {
          serviceWorker.addEventListener('statechange', function(e) {

            if(e.target.state === "installed") {
              v.swInstalled = true;
            }

            if(navigator.serviceWorker.controller) {
              v.swInControl = true;
            } else {
              v.swInControl = false;
            }
          });
        }

      }).catch(function(error){
        console.error('[offlineController] SW failed to register', error);
      });

      // Listens for messages sent explicitly by the service worker. This
      // doesn't recieve messages that are replies to a client message
      console.debug('[offlineController] Adding event listener for messages from SW');
      navigator.serviceWorker.addEventListener('message', function(event) {

        var message = event.data;

        switch (message.type) {
          case "offlineReady": {
            v.swInstalled = true;
            v.swInControl = true;
            break;
          }
          case "queueLength": {
            v.swQueueLength = message.value;
            break;
          }
          case "needToken": {
            const token = (document.getElementsByName("csrfmiddlewaretoken")[0] as HTMLInputElement).value;
            if(token) {
              event.ports[0].postMessage({
                type: "csrftoken",
                value: token,
              });
            } else {
              event.ports[0].postMessage({
                type: "error",
              });
            }
            break;
          }
          case "synchronising": {
            v.swSynchronising = true;
            break;
          }
          case "synchronised": {
            v.swSynchronising = false;
            if (message.value.count > 0 && message.value.finished) {
              //v.notificationHelper.createSuccessNotification('Queue Synchronised! Refresh the page to download any changes made while you were offline.');
            } else if (message.value.count > 0 && !message.value.finished){
              v.notificationHelper.createErrorNotification('Your queued changes have partially been sent to the server, but the process was interrupted.');
            }
            break;
          }
          case "error": {
            v.notificationHelper.createErrorNotification(message.value);
            break;
          }
          case "itemSynced": {
            // this event is handled elsewhere
            break;
          }
          default: {
            console.warn('[offlineController] The Service Worker sent a message type that isn\'t supported!', message);
          }
        }

      });
    } else {
      console.warn('[offlineController] Service Workers are not supported in this browser, offline mode is unavailable.');
    }
  }

  /**
   * Gets the queue length from the service worker and stores it
   */
  setSWQueueLength() {
    let v = this;
    v.sendMessageToServiceWorker({
      type: "getQueueLength"
    }).then(function(response) {
      v.swQueueLength = Number(response);
    }).catch(function(error) {
      console.error('[offlineController] Error getting queue length from service worker:', error);
    });
  }

  /**
   * Toggles the delay image upload, storing it in the database
   */
  toggleDelayImageUploads() {
    this.delayImageUpload = !this.delayImageUpload;

    this.offlineService.setSetting('autoImageUpload', !this.delayImageUpload);
  }

  setOnlineStatus() {
    this.online = navigator.onLine;
  }

  /**
   * Download files that are needed for offline functionality
   */
  downloadFilesForOffline() {
    this.downloadingFilesForOffline = true;
    this.dataForOfflineSaved = false;

    // download and save to IndexedDB data needed for offline mode
    Promise.all([
      this.savePersonsForOffline()
      .then(this.saveFeaturesForOffline)
      .then(this.saveMemorialInscriptionsForOffline)
      .then(this.saveFeatureAttributeMaterialsForOffline)
      .then(this.saveUserGroupsForOffline)
    ])
    .then(() => {
      // if everything downloaded and saved without being cancelled
      if (!this.cancelDownloadFilesForOffline)
        this.dataForOfflineSaved = true;
    })
    .catch((response) => {
      console.error(response.message);
      this.dataForOfflineSaved = false;
      this.saveDataForOffline = false;
      this.notificationHelper.createErrorNotification('Download of offline data failed: ' + response.message);
    })
    .finally(() => {
      this.cancelDownloadFilesForOffline = false;
      this.downloadingFilesForOffline = false;
    });
  }

  /**
   * Remove aerial layer while offline
   */
  turnAerialOff() {
    if (this.$store.state.MapLayers.layers['aerial']) {
      this.aerialLayerWhileOffline = this.$store.state.MapLayers.layers['aerial'];
      delete this.$store.state.MapLayers.layers['aerial'];
    }
  }

  /**
   * Restore aerial layer
   */
  turnAerialOn() {
    this.$store.state.MapLayers.layers['aerial'] = this.aerialLayerWhileOffline;
    this.aerialLayerWhileOffline = null;
  }

  /**
   * Remove base layer while offline
   */
  turnBaseOff() {
    if (this.$store.state.MapLayers.layers['base']) {
      this.baseLayerWhileOffline = this.$store.state.MapLayers.layers['base'];
      delete this.$store.state.MapLayers.layers['base'];
    }
  }

  /**
   * Restore base layer
   */
  turnBaseOn() {
    this.$store.state.MapLayers.layers['base'] = this.baseLayerWhileOffline;
    this.baseLayerWhileOffline = null;
  }
}
</script>
