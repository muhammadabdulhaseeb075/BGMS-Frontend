angular.module('bgmsApp.map').service('offlineService', ['$q', '$rootScope', '$http',
  function($q, $rootScope, $http){

    var view_model = this;

    // Public Variables
    view_model.bgmsQueueLength = 0;

		// Come from settings table
    view_model.autoImageUpload = true;
    view_model.queuedMemorialPhotosPrimaryKeys = {};
    view_model.queuedInspectionPhotosPrimaryKeys = {};

    // Public Functions
    view_model.getQueuedItems = getQueuedItems;
    view_model.countQueuedItems = countQueuedItems;
    view_model.getItems = getItems;
		view_model.getItemsByPrimaryKey = getItemsByPrimaryKey;
    view_model.addToQueue = addToQueue;
    view_model.deleteFromQueue = deleteFromQueue;
    view_model.getFirst = getFirst;
    view_model.deleteFirst = deleteFirst;
    view_model.getSetting = getSetting;
    view_model.setSetting = setSetting;

		// get list of primary keys for Memorial Photos stored in queue
		view_model.getSetting('queuedMemorialPhotosPrimaryKeys')
      .then(function(queuedMemorialPhotosPrimaryKeys) {
        if(queuedMemorialPhotosPrimaryKeys) view_model.queuedMemorialPhotosPrimaryKeys = queuedMemorialPhotosPrimaryKeys.value;

				// get list of primary keys for inspection Photos stored in queue
				view_model.getSetting('queuedInspectionPhotosPrimaryKeys')
					.then(function(queuedInspectionPhotosPrimaryKeys) {
						if(queuedInspectionPhotosPrimaryKeys) view_model.queuedInspectionPhotosPrimaryKeys = queuedInspectionPhotosPrimaryKeys.value;

						// get total number of records in queue
						_getQueueStore()
			        .then(function(queueStore) {
								var countRequest = queueStore.count();
								countRequest.onsuccess = function() {
								  var queueCount = countRequest.result;
									var memorialPhotosCount = 0;
									var inspectionPhotosCount = 0;

									if (view_model.queuedMemorialPhotosPrimaryKeys) {
										$.each(view_model.queuedMemorialPhotosPrimaryKeys, function(i, value) {
									    memorialPhotosCount = memorialPhotosCount + view_model.queuedMemorialPhotosPrimaryKeys[i].length
										});
									}

									if (view_model.queuedInspectionPhotosPrimaryKeys){
										$.each(view_model.queuedInspectionPhotosPrimaryKeys, function(i, value) {
									    inspectionPhotosCount = inspectionPhotosCount + view_model.queuedInspectionPhotosPrimaryKeys[i].length
										});
									}

									// if number of records in queue does not match, redo the count
									if (memorialPhotosCount + inspectionPhotosCount != queueCount) {
										view_model.countQueuedItems();
									}
									else {
										view_model.bgmsQueueLength = queueCount;
									}
								}
							});
					})
					.catch(function(error) {
						console.error('[offlineService] Error getting the setting from the database', error);
					});

      })
      .catch(function(error) {
        console.error('[offlineService] Error getting the setting from the database', error);
      });

    // Get the current autoImageUpload setting from the database, if present
    view_model.getSetting('autoImageUpload')
      .then(function(setting) {
        if(setting) view_model.autoImageUpload = setting.value;
      })
      .catch(function(error) {
        console.error('[offlineService] Error getting the setting from the database', error);
      });

    /**
     * Gets (and creates) the database
     * @return {IDBDatabase} the database
     */
    function _getDatabase() {

      var deferred = $q.defer();

      var request = window.indexedDB.open("BGMS-offline-service", 2);

      // Runs when the database is created, or when the version number is
      // higher than the previously installed version
      request.onupgradeneeded = function(event) {
        var db = event.target.result;

        var queueStore = db.createObjectStore("queue", { autoIncrement: true});
        queueStore.createIndex("uuid", "uuid", { unique: false });

        var settingsStore = db.createObjectStore("settings", { keyPath: 'setting'});
      }

      request.onerror = function(event) { deferred.reject(request.errorCode); };
      request.onsuccess = function(event) { deferred.resolve(request.result); };

      return deferred.promise;

    }

    /**
     * Returns the queue store
     * @return {IDBObjectStore} the queue store, if found
     */
    function _getQueueStore() {
      return _getDatabase()
        .then(function(db) {

          var tx = db.transaction(["queue"], "readwrite");
          tx.onerror = function(event) {
            console.error('[offlineService] Unable to perform transaction on Queue Store', event);
          };
          return tx.objectStore("queue");

        })
        .catch(function(errorCode) {
          console.error('[offlineService] Unable to get database:', errorCode);
          return null;
        });
    }

    /**
     * Returns the settings store
     * @return {IDBObjectStore} the settings store, if found
     */
    function _getSettingsStore() {
      return _getDatabase()
        .then(function(db) {

          var tx = db.transaction(["settings"], "readwrite");
          tx.onerror = function(event) {
            console.error('[offlineService] Unable to perform transaction on Setting Store', event);
          };
          return tx.objectStore("settings");

        })
        .catch(function(errorCode) {
          console.error('[offlineService] Unable to get database:', errorCode);
          return null;
        });
    }

    /**
     * Gets all the queued items from the database
     * @return {Promise} A promise which resolves to an array of queued items
     */
    function getQueuedItems() {
      var deferred = $q.defer();
      var queuedItems = [];

      _getQueueStore()
        .then(function(queueStore) {

          var queueCursor = queueStore.openCursor();

          queueCursor.onsuccess = function(event) {

            var cursor = event.target.result;

            if (cursor) {

              var queuedItem = cursor.value;
              queuedItem._key = cursor.primaryKey;

              queuedItems.push(queuedItem);

              cursor.continue();
            }
						else {
              view_model.bgmsQueueLength = queuedItems.length;
              $rootScope.$apply();
              deferred.resolve(queuedItems);
            }
          };

          queueCursor.onerror = function(event) {
            deferred.reject();
          };
        })
        .catch(function() {
          deferred.reject();
        });

      return deferred.promise;
    }

    /**
     * Counts all the queued items from the database and sorts primary keys into arrays linked to memorial uuids
     */
    function countQueuedItems() {
      var deferred = $q.defer();
			view_model.bgmsQueueLength = 0;
	    view_model.queuedMemorialPhotosPrimaryKeys = {};
	    view_model.queuedInspectionPhotosPrimaryKeys = {};

      _getQueueStore()
        .then(function(queueStore) {

          var queueCursor = queueStore.openCursor();

          queueCursor.onsuccess = function(event) {

            var cursor = event.target.result;

            if (cursor) {

              var queuedItem = cursor.value;
              queuedItem._key = cursor.primaryKey;

							// Store the number of queued photos for each memorial
		          if (queuedItem.url === '/mapmanagement/takePhoto/') {

								if (!view_model.queuedMemorialPhotosPrimaryKeys[queuedItem.uuid])
									view_model.queuedMemorialPhotosPrimaryKeys[queuedItem.uuid] = [];

		            view_model.queuedMemorialPhotosPrimaryKeys[queuedItem.uuid].push(queuedItem._key);
		          } else if (queuedItem.url === '/mapmanagement/memorialInspection/') {

								if (!view_model.queuedInspectionPhotosPrimaryKeys[queuedItem.uuid])
									view_model.queuedInspectionPhotosPrimaryKeys[queuedItem.uuid] = [];

		            view_model.queuedInspectionPhotosPrimaryKeys[queuedItem.uuid].push(queuedItem._key);
		          }

							view_model.bgmsQueueLength++;

              cursor.continue();
            }
						else {
							view_model.setSetting('queuedMemorialPhotosPrimaryKeys', view_model.queuedMemorialPhotosPrimaryKeys);
							view_model.setSetting('queuedInspectionPhotosPrimaryKeys', view_model.queuedInspectionPhotosPrimaryKeys);

              $rootScope.$apply();
              deferred.resolve();
            }
          };

          queueCursor.onerror = function(event) {
            deferred.reject();
          };
        })
        .catch(function() {
          deferred.reject();
        });

      return deferred.promise;
    }

    /**
     * Returns all items in the queue that match a criteria
		 * @param url
		 * @param key - name of key to match with value (not primary key)
		 * @param value - value of key to match
     * @return {Promise} A promise which resolves to an array of queued items
     */
    function getItems(url, key, value) {
      var deferred = $q.defer();
      var queuedItems = [];

      _getQueueStore()
        .then(function(queueStore) {

          var queueCursor = queueStore.openCursor();

          queueCursor.onsuccess = function(event) {

            var cursor = event.target.result;

            if (cursor) {
							var queuedItem = cursor.value;

							if ((queuedItem.url.includes(url))
							&& (queuedItem.data.hasOwnProperty(key))
							&& (queuedItem.data[key] === value)) {
								queuedItem.data.queueKey = cursor.key;
								queuedItems.push(queuedItem.data);
							}
							cursor.continue();
						}
						else
							deferred.resolve(queuedItems);
          };

          queueCursor.onerror = function(event) {
            deferred.reject();
          };

        })
        .catch(function() {
          deferred.reject();
        });

      return deferred.promise;
    }

    /**
     * Returns all items in the queue that match a criteria
     * @return {Promise} A promise which resolves to an array of queued items
     */
    function getItemsByPrimaryKey(primaryKey) {
      var deferred = $q.defer();
      var queuedItems = [];

      _getQueueStore()
        .then(function(queueStore) {

					var objectStoreRequest  = queueStore.get(primaryKey);

					objectStoreRequest.onsuccess = function(event) {
						var queuedItem = objectStoreRequest.result.data;
						queuedItem.queueKey = primaryKey;
						deferred.resolve(queuedItem);
					}

          objectStoreRequest.onerror = function(event) {
            deferred.reject();
          };
        })
        .catch(function() {
          deferred.reject();
        });

      return deferred.promise;
    }

    /**
     * Gets the first item in the queue
     * @return {Object} the first item in the queue
     */
    function getFirst() {
      var deferred = $q.defer();

      _getQueueStore()
        .then(function(queueStore) {

          var queueCursor = queueStore.openCursor();

          queueCursor.onsuccess = function(event) {
            var cursor = event.target.result;

            if (cursor) {

              var queuedItem = cursor.value;
              queuedItem._key = cursor.primaryKey;

              deferred.resolve(queuedItem);

            } else {
              deferred.resolve();
            }
          };

          queueCursor.onerror = function(event) {
            deferred.reject();
          };

        })
        .catch(function() {
          deferred.reject();
        });

      return deferred.promise;
    }

    /**
     * Deletes the first item in the queue
     */
    function deleteFirst() {
      var deferred = $q.defer();

      _getQueueStore()
        .then(function(queueStore) {

          var queueCursor = queueStore.openCursor();

          queueCursor.onsuccess = function(event) {
            var cursor = event.target.result;

            if (cursor) {

              var item = cursor.value;

              var deleteFromQueue = cursor.delete();
              deleteFromQueue.onsuccess = function() {

			          // Update the number of queued photos for each memorial
			          if (item.url === '/mapmanagement/takePhoto/') {
									view_model.queuedMemorialPhotosPrimaryKeys[item.uuid] = jQuery.grep(view_model.queuedMemorialPhotosPrimaryKeys[item.uuid], function(value) {
  									return value != cursor.primaryKey;
									});
			          } else if (item.url === '/mapmanagement/memorialInspection/') {
									view_model.queuedInspectionPhotosPrimaryKeys[item.uuid] = jQuery.grep(view_model.queuedInspectionPhotosPrimaryKeys[item.uuid], function(value) {
  									return value != cursor.primaryKey;
									});
			          }

								view_model.bgmsQueueLength--;

								deferred.resolve(item);
              }

            } else {
              deferred.resolve();
            }
          };

          queueCursor.onerror = function(event) {
            deferred.reject();
          };

        })
        .catch(function() {
          deferred.reject();
        });

      return deferred.promise;
    }

    /**
     * Adds an item to the queue database
     * @param {Object} item - the item to be added
     * @return {Promise} A promise which resolves if the addition is successful
     */
    function addToQueue(item) {
      var deferred = $q.defer();

      _getQueueStore()
        .then(function(queueStore) {

          var addToQueue = queueStore.add(item);
          addToQueue.onsuccess = function(e) {

						// Update the number of queued photos for each memorial
						if (item.url === '/mapmanagement/takePhoto/') {

							if (!view_model.queuedMemorialPhotosPrimaryKeys[item.uuid])
								view_model.queuedMemorialPhotosPrimaryKeys[item.uuid] = [];

							view_model.queuedMemorialPhotosPrimaryKeys[item.uuid].push(e.target.result);
							view_model.setSetting('queuedMemorialPhotosPrimaryKeys', view_model.queuedMemorialPhotosPrimaryKeys);

						} else if (item.url === '/mapmanagement/memorialInspection/') {

							if (!view_model.queuedInspectionPhotosPrimaryKeys[item.uuid])
								view_model.queuedInspectionPhotosPrimaryKeys[item.uuid] = [];

							view_model.queuedInspectionPhotosPrimaryKeys[item.uuid].push(e.target.result);
							view_model.setSetting('queuedInspectionPhotosPrimaryKeys', view_model.queuedInspectionPhotosPrimaryKeys);
						}

						view_model.bgmsQueueLength++;

            deferred.resolve(e.target.result);
          };
          addToQueue.onerror = function() {
            deferred.reject();
          };

        })
        .catch(function(error) {
          deferred.reject();
        });

      return deferred.promise;
    }

    /**
     * Deletes an item from the queue database
     * @param {any} uuid - UUID of memorial
     * @param {Number} key - The key of the item to be deleted
     * @param {string} url
     * @return {Promise} A promise which resolves if the deletion is successful
     */
    function deleteFromQueue(uuid, key, url) {
      var deferred = $q.defer();

      _getQueueStore()
        .then(function(queueStore) {

          var deleteFromQueue = queueStore.delete(key);
          deleteFromQueue.onsuccess = function() {

						// Update the number of queued photos for each memorial
						if (url === '/mapmanagement/takePhoto/') {
							view_model.queuedMemorialPhotosPrimaryKeys[uuid] = jQuery.grep(view_model.queuedMemorialPhotosPrimaryKeys[uuid], function(value) {
								return value != key;
							});
							view_model.setSetting('queuedMemorialPhotosPrimaryKeys', view_model.queuedMemorialPhotosPrimaryKeys);
						} else if (url === '/mapmanagement/memorialInspection/') {
							view_model.queuedInspectionPhotosPrimaryKeys[uuid] = jQuery.grep(view_model.queuedInspectionPhotosPrimaryKeys[uuid], function(value) {
								return value != key;
							});
							view_model.setSetting('queuedInspectionPhotosPrimaryKeys', view_model.queuedInspectionPhotosPrimaryKeys);
						}

						view_model.bgmsQueueLength--;

						deferred.resolve();
          };
          deleteFromQueue.onerror = function() {
            deferred.reject();
          };

        })
        .catch(function(error) {
          deferred.reject();
        });

      return deferred.promise;
    }

    /**
     * Get a setting value from the database
     * @param {String} name - the name of the setting to retrieve
     */
    function getSetting(name) {
      var deferred = $q.defer();

      _getSettingsStore()
        .then(function(settingsStore) {

          var getSetting = settingsStore.get(name);
          getSetting.onsuccess = function(event) {
            deferred.resolve(event.target.result);
          };
          getSetting.onerror = function(event) {
            deferred.reject(event);
          };

        })
        .catch(function(error) {
          deferred.reject(error);
        });

      return deferred.promise;
    }

    /**
     * Add or update a setting in the database
     * @param {String} name - the name of the setting to add/update
     * @param {*} value - the value of the setting
     */
    function setSetting(name, value) {
      var deferred = $q.defer();

      _getSettingsStore()
        .then(function(settingsStore) {

          var setting = {
            setting: name,
            value: value,
          };

          var addSetting = settingsStore.put(setting);
          addSetting.onsuccess = function(event) {
            deferred.resolve();
          };
          addSetting.onerror = function(event) {
            deferred.reject();
          };

        })
        .catch(function(error) {
          deferred.reject(error);
        });

      return deferred.promise;
    }

  }
]);
