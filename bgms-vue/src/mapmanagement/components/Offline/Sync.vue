<template>
  <div class="panel panel-default">
    <div class="panel-heading">
      Synchronise
    </div>
    <div class="panel-body">

      <span v-if="swQueueLength || bgmsQueueLength">
        You have made {{ totalQueuesCount }} unsynchronised change{{ totalQueuesCount > 1 ? "s" : "" }}.
      </span>
      <span v-if="online">
         Remember to synchronise!
      </span>
      <span v-else>
         Remember to synchronise when online!
      </span>
      <br>
      <br>
      <span v-if="estimateQuotaAvailableMB">
         (Estimated {{ estimateQuotaAvailableMB >= 1024 ? (estimateQuotaAvailableMB / 1024).toFixed(1) + " GB" : estimateQuotaAvailableMB + " MB"}} of storage remaining.)
      </span>

      <button id="syncButton" class="sync sidebar-normal-button ladda-button" data-style="slide-right" v-show="online && !syncInProgress" @click="sync">
        <span class="ladda-label">Sync Now</span>
      </button>

      <button class="blocked sidebar-normal-button ladda-button" data-style="slide-right" v-if="swQueueBlocked" @click="unblockSwQueue">
        <span class="ladda-label">Delete first item in queue</span>
      </button>

      <button class="blocked sidebar-normal-button ladda-button" data-style="slide-right" v-if="bgmsQueueBlocked" @click="unblockBGMSQueue">
        <span class="ladda-label">Delete first item in queue</span>
      </button>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import axios from 'axios'
import NoSleep from 'nosleep.js'

import ServiceWorkerTools from './../../mixins/serviceWorkerTools'

/**
 * Class representing Sync component
 * @extends Vue
 */
@Component
export default class Sync extends mixins(ServiceWorkerTools){

  offlineService: any = this.$store.getters.offlineService;
  notificationHelper: any = this.$store.getters.notificationHelper;
  reportingService: any = this.$store.getters.reportingService;

  swQueueBlocked: boolean = false;
  bgmsQueueBlocked: boolean = false;

  // used for progress bar
  progress: number = 0;
  percent: number = 0;
  syncNotice;
  progressBar;
  totalItemsInQueues = 0;

  noSleep = new NoSleep();

   /**
    * Vue mounted lifecycle hook
    */
  mounted() {
    (document.getElementById("syncButton") as any).addEventListener('click', this.enableNoSleep, false);
  }

  /*** Computed ***/

  /**
   * Computed property: Get online status
   * @returns {boolean} True if online
   */
  get online(): boolean {
    return this.$store.state.Offline.online;
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
   * @returns {number} - returns total number of items in SW queue and BGMS queue
   */
  get totalQueuesCount(): number {
    let v = this;

    this.storageEstimateWrapper()
    .then(function(estimate) {
      v.$store.commit('updateEstimateQuotaAvailableMB', estimate);
    });
    return v.bgmsQueueLength + v.swQueueLength;
  }

  /**
   * @returns {number} - estimated storage available
   */
  get estimateQuotaAvailableMB(): number {
    return this.$store.state.Offline.estimateQuotaAvailableMB;
  }

  /**
   * @returns {boolean}
   */
  get syncInProgress(): boolean {
    return this.$store.state.Offline.syncInProgress;
  }
  /**
   * Set syncInProgress
   * @param {boolean}
   */
  set syncInProgress(value: boolean) {
    this.$store.commit('updateSyncInProgress', value);
  }

  /*** Methods ***/

  /**
   * Sync all items in both sw queue and bgms queue
   */
  sync() {
    let v = this;
    v.syncInProgress = true;

    // Initialises progress varaiables
    let percent: number = 0;
    v.totalItemsInQueues = v.totalQueuesCount;

    // Create progress notification
    v.syncNotice = v.notificationHelper.createProgressNotification('Synchronising!', function(notice) {
      v.progressBar = notice.get().find("div.progress-bar");
      v.progressBar.width(0 + "%").attr("aria-valuenow", 0).find("span").html(0 + "%");
    });
    v.progress = 0;

    // sync sw queue first
    if (v.swQueueLength)
      {
        // Start the sync
        v.uploadSWQueuedItems()
        .then(function(length) {
          v.swQueueLength = Number(length);
          if (length > 0) {
            v.swQueueBlocked = true;
            v.notificationHelper.createErrorNotification('Couldn\'t synchronise changes. Are you sure you\'re online?');
            v.syncCompleted();
          } else {
            // once sw queue has successfully synced, sync the bgms queue
            if (v.bgmsQueueLength) {
              v.syncBGMSQueuedItems();
            }
            else {
              v.syncCompletedSuccessfully();
            }
          }

        }).catch(function(error) {
          // Close the progress notice
          v.swQueueBlocked = true;
          v.notificationHelper.createErrorNotification('Couldn\'t synchronise changes. Are you sure you\'re online?');
          v.syncCompleted();

        });
    }
    else
      v.syncBGMSQueuedItems();
  }

  /**
   * Uploads the saved images
   */
  syncBGMSQueuedItems() {
    let v = this;

    v.uploadBGMSQueuedItems()
      .then(function() {
        v.syncCompletedSuccessfully();
      })
      .catch(function(error) {

        if (error === -1) {
          // User is offline
          v.notificationHelper.createErrorNotification('Unable to connect to the server');
        } else if (error === 400) {
          // Server couldn't understand the request
          v.notificationHelper.createErrorNotification('We were unable to process the queued item. Try again later, or remove the item from the queue.');
          v.bgmsQueueBlocked = true;
        } else {
          // A different error occurred
          v.notificationHelper.createErrorNotification('Unable to upload images');
        }

        v.syncCompleted();

      });
  }

  /**
   * Tidy up after sync has been successfully completed
   */
  syncCompletedSuccessfully() {
    this.notificationHelper.createSuccessNotification('All items synced successfully! Refresh the page to download any changes made while you were offline.');

    this.bgmsQueueBlocked = false;
    this.swQueueBlocked = false;

    this.syncCompleted();
  }

  /**
   * Tidy up after sync has been un/successfully completed
   */
  syncCompleted() {
    let v = this;

    // Close the progress notice
    v.syncNotice.remove();
    v.syncInProgress = false;
    v.noSleep.disable();

    // updated estimated quota available
    this.storageEstimateWrapper()
    .then(function(estimate) {
      v.$store.commit('updateEstimateQuotaAvailableMB', estimate);
    });
  }

  /**
   * Recursive function which uploads all items in the sw queue
   * Note: this recursion used to be done in the sw. But in long syncs, the sw would get killed causing the sync to appear to be stuck.
   * @return {Promise} A promise which resolves if all items are successfully uploaded
   */
  uploadSWQueuedItems() {
    let v = this;

    return new Promise(function(resolve, reject) {
      v.sendMessageToServiceWorker({
        type: "synchroniseFirstItemInQueue"
      }).then(function(length) {

          // if nothing was actually synced
          if (v.swQueueLength === length) {
            return reject();
          }

          // item synced successfully so update proress bar
          v.progress++;
          let percent = Number(((v.progress / v.totalItemsInQueues) * 100).toFixed());
          v.progressBar.width(percent + "%").attr("aria-valuenow", percent).find("span").html(percent + "%");
          v.swQueueLength--;

          if (length > 0) {
            // Recursion
            v.uploadSWQueuedItems()
              .then(function(length) {
                resolve(length);
              })
              .catch(function(error) {
                reject(error);
              });
            }
            else
              resolve(length);
        })
        .catch(function(error) {
            reject(error);
        });
      })
  }

  /**
   * Recursive function which uploads all items in the bgms queue
   * @return {Promise} A promise which resolves if all items are successfully uploaded
   */
  uploadBGMSQueuedItems() {
    let v = this;

    return new Promise(function(resolve, reject) {
      v.offlineService.getFirst()
        .then(function(item) {

          if (item) {
            let componentData = item.data;
            let url = item.url;

            let config = {};
            if (item.headers) config['headers'] = item.headers;

            axios.post(url, componentData, config)
              .then(function(response) {
                v.offlineService.deleteFromQueue(item.uuid, item._key, url)
                  .then(function() {

                    // item synced successfully so update proress bar
                    v.progress++;
                    let percent = Number(((v.progress / v.totalItemsInQueues) * 100).toFixed());
                    v.progressBar.width(percent + "%").attr("aria-valuenow", percent).find("span").html(percent + "%");

                    // Recursion
                    v.uploadBGMSQueuedItems()
                      .then(function() {
                        resolve();
                      })
                      .catch(function() {
                        reject();
                      });

                  })
                  .catch(function() {
                    reject();
                  });
              })
              .catch(function(response) {
                reject(response.status);
              });

          } else {
            resolve();
          }

        })
        .catch(function() {
          reject();
        });
      });
  }

  /**
   * Unblocks the Service Worker queue
   */
  unblockSwQueue(e) {
    let v= this;

    v.notificationHelper.createConfirmation('Delete', 'Are you sure you want to delete the first item in the queue? This may result in errors for other items in the queue. An error report will be send to the system administrator.', function() {

      v.sendMessageToServiceWorker({
        type: "unblockQueue"
      }).then(function(item) {

        v.reportingService.sendBugReport(JSON.stringify(item));

        v.notificationHelper.createSuccessNotification('Delete successful');
        v.swQueueBlocked = false;
        v.swQueueLength--;

      }).catch(function(error) {

        v.notificationHelper.createErrorNotification('Couldn\'t delete the first item in the queue');
        console.error('[offlineController] Couldn\'t delete the first item in the queue:', error);

      });

    }, function() {
    });

  }

  /**
   * Unblocks the BGMS queue
   */
  unblockBGMSQueue($event) {
    let v = this;

    v.notificationHelper.createConfirmation('Delete', 'Are you sure you want to delete the first item in the queue? This will send an error report to the system administrator.', function() {

      v.offlineService.deleteFirst()
        .then(function(item) {

          v.reportingService.sendBugReport(JSON.stringify(item));

          v.notificationHelper.createSuccessNotification('Delete successful');
          v.bgmsQueueBlocked = false;
        })
        .catch(function() {
          v.notificationHelper.createErrorNotification('Couldn\'t delete the first item in the queue');
        })
        .finally(function() {
        });

    }, function() {

    });
  }

  // stops device going to sleep
  enableNoSleep() {
    this.noSleep.enable();
  }
}
</script>
