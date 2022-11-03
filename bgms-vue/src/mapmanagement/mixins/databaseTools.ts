import idb from 'idb';
import axios from 'axios';
import Component, { mixins } from 'vue-class-component'
import SecurityMixin from '@/mixins/securityMixin'
import ServiceWorkerTools from './../mixins/serviceWorkerTools'

@Component({})
export default class DatabaseTools extends mixins(SecurityMixin, ServiceWorkerTools){

  cancelDownloadFilesForOffline: boolean = false;
  downloadingFilesForOffline: boolean = false;

  dataForOfflineSaved: boolean = null;

  // note: this must match the version number in sw
  // TODO avoid hardcoding this twice
  databaseVersion: number = 5;

  /**
   * Download features and store in indexeddb
   */
  saveFeaturesForOffline() {
    const dbPromise = idb.open('BGMS-db', this.databaseVersion);
    let responseData;

    return axios.get('/mapmanagement/getAllFeatures/')
    .then(response => {
      responseData = response.data;
      // clear table
      return dbPromise
      .then(db => {
        const deleteTx = db.transaction('features', 'readwrite');
        deleteTx.objectStore('features').clear();
        return deleteTx.complete;
      });
    })
    .then(() => {
      // add new data
      return dbPromise.then(db => {
        let addTx = db.transaction('features', 'readwrite');

        if (!this.cancelDownloadFilesForOffline) {
          for(const group of responseData) {
            for(const layer of group.layers) {
              let featureJson = layer.layer;

              // Add all the new data
              for(let feature of featureJson.features) {
                feature._layer_type = layer.layer_type;
                addTx.objectStore('features').put(feature);
              
                if (this.cancelDownloadFilesForOffline)
                  break;
              }
              
              if (this.cancelDownloadFilesForOffline)
                break;
            }
            
            if (this.cancelDownloadFilesForOffline)
              break;
          }
        }

        if (this.cancelDownloadFilesForOffline) {
          // rollback transaction
          addTx.abort();
        }

        return addTx.complete;
      });
    })
  }

  /**
   * Download persons and store in indexeddb
   */
  savePersonsForOffline() {
    const dbPromise = idb.open('BGMS-db', this.databaseVersion);
    let responseData;

    return axios.get('/mapmanagement/getPersons/')
    .then(response => {
      responseData = response.data;

      // clear table
      return dbPromise.then(db => {
        const deleteTx = db.transaction('persons', 'readwrite');
        deleteTx.objectStore('persons').clear();
        return deleteTx.complete;
      });
    })
    .then(() => {

      // no persons returned if more than 10,000
      if (!responseData.persons)
        return;

      // add new data
      return dbPromise.then(db => {
        let addTx = db.transaction('persons', 'readwrite');
        if (!this.cancelDownloadFilesForOffline) {
          for(let person of responseData.persons) {
            addTx.objectStore('persons').add(person);
              
            if (this.cancelDownloadFilesForOffline)
              break;
          }
        }

        if (this.cancelDownloadFilesForOffline) {
          // rollback transaction
          addTx.abort();
        }

        this.sendMessageToServiceWorker({
          type: "personsAvailableOffline",
          value: true
        });
        
        return addTx.complete;
      })
    })
  }

  /**
   * Download persons and store in indexeddb
   */
  saveMemorialInscriptionsForOffline() {
    const dbPromise = idb.open('BGMS-db', this.databaseVersion);
    let responseData;

    return axios.get('/mapmanagement/getAllMemorialInscriptions/')
    .then(response => {
      responseData = response.data;
      // clear table
      return dbPromise
      .then(db => {
        const deleteTx = db.transaction('memorialInscriptions', 'readwrite');
        deleteTx.objectStore('memorialInscriptions').clear();
        return deleteTx.complete;
      });
    })
    .then(() => {
      // add new data
      return dbPromise.then(db => {
        let addTx = db.transaction('memorialInscriptions', 'readwrite');
        if (!this.cancelDownloadFilesForOffline) {
          for(let memorialInscription of responseData) {
            addTx.objectStore('memorialInscriptions').add(memorialInscription);
              
            if (this.cancelDownloadFilesForOffline)
              break;
          }
        }

        if (this.cancelDownloadFilesForOffline) {
          // rollback transaction
          addTx.abort();
        }
        
        return addTx.complete;
      })
    })
  }

  /**
   * Download feature attribute materials and store in indexeddb
   */
  saveFeatureAttributeMaterialsForOffline() {
    const dbPromise = idb.open('BGMS-db', this.databaseVersion);
    let responseData;

    return axios.get('/geometries/featureAttributeMaterials/')
    .then(response => {
      responseData = response.data.materials;
      // clear table
      return dbPromise
      .then(db => {
        const deleteTx = db.transaction('materials', 'readwrite');
        deleteTx.objectStore('materials').clear();
        return deleteTx.complete;
      });
    })
    .then(() => {
      // add new data
      return dbPromise.then(db => {
        let addTx = db.transaction('materials', 'readwrite');
        if (!this.cancelDownloadFilesForOffline) {
          for(let material of responseData) {
            addTx.objectStore('materials').add(material);
              
            if (this.cancelDownloadFilesForOffline)
              break;
          }
        }

        if (this.cancelDownloadFilesForOffline) {
          // rollback transaction
          addTx.abort();
        }
        
        return addTx.complete;
      })
    })
  }

  /**
   * Download user's groups and store in indexeddb
   */
  saveUserGroupsForOffline() {
    this.getGroups()
    .then(result => {
      this.sendMessageToServiceWorker({
        type: "group_required",
        value: result
      });
    })
  }

  /**
   * Remove data from indexeddb
   */
  removeDataForOffline() {
    const dbPromise = idb.open('BGMS-db', this.databaseVersion);

    // clear tables
    return dbPromise.then(db => {
      let deleteTx = db.transaction('features', 'readwrite');
      deleteTx.objectStore('features').clear();

      deleteTx = db.transaction('persons', 'readwrite');
      deleteTx.objectStore('persons').clear();

      deleteTx = db.transaction('memorialInscriptions', 'readwrite');
      deleteTx.objectStore('memorialInscriptions').clear();

      return deleteTx.complete;
    })
    .catch(err => {
      //probably because db has not been created
    });
  }
}
