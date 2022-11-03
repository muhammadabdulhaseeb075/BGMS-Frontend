import Vue from 'vue'
import Component from 'vue-class-component'

@Component({})
export default class ServiceWorkerTools extends Vue{
  /**
   * Base function for sending a message to the service worker
   * @param {Object} message
   * @param {string} message.type - The type of the message, so the SW knows how to respond
   * @param {*} [message.value] - The contents of the message
   */
  sendMessageToServiceWorker(message) {
    return new Promise(function(resolve, reject) {
      if(navigator.serviceWorker.controller) {
        var messageChannel = new MessageChannel();

        // Waits for a response
        messageChannel.port1.onmessage = function(event) {
          var reply = event.data;

          console.debug('[offline] Reply from SW', reply);

          if (reply.type === "error") {
            reject(reply.value);
          } else {
            resolve(reply.value);
          }
        };

        // Sends the message and a reference to the port that the SW can reply on
        navigator.serviceWorker.controller.postMessage(message, [messageChannel.port2]);
      } else {
        reject('The service worker isn\'t in control of the page!');
      }
    });
  }

  /**
   * Retrieves estimated storage usage and quota
   * https://developers.google.com/web/updates/2017/08/estimating-available-storage-space
   * @returns {Promise} Promise that will resolve storage usage and quota
   */
  storageEstimateWrapper() {
    // mostly just supported by Chrome
    if ('storage' in navigator && 'estimate' in (window as any).navigator.storage) {
      // We've got the real thing! Return its response.
      return (window as any).navigator.storage.estimate();
    }

    if ('webkitTemporaryStorage' in navigator &&
        'queryUsageAndQuota' in (window as any).navigator.webkitTemporaryStorage) {
      // Return a promise-based wrapper that will follow the expected interface.
      return new Promise(function(resolve, reject) {
        (window as any).navigator.webkitTemporaryStorage.queryUsageAndQuota(
          function(usage, quota) {resolve({usage: usage, quota: quota})},
          reject
        );
      });
    }

    // If we can't estimate the values, return a Promise that resolves with NaN.
    return Promise.resolve({usage: NaN, quota: NaN});
  }
}
