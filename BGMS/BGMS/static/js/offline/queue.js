/* jshint esversion:6 */

class RequestQueue {

  constructor(options = {}) {
    this.databaseName = options.name ? options.name + "-queue" : "request-queue";
    this.queueStoreName = "queue-store";
    this.version = 1;
  }

  /**
   * Friendly name for creating the database in the SW activate event
   */
  createDatabase() {
    return this._getDatabase();
  }

  /**
   * Adds a new request to the database
   */
  push(request) {
    return Promise.all([
      this._getDatabase(),
      this._serialize(request)
    ]).then(values => {
      let db = values[0];
      let serialized = values[1];

      const tx = db.transaction(this.queueStoreName, 'readwrite');
      tx.objectStore(this.queueStoreName).add(serialized);

      return tx.complete;
    });
  }

  /**
   * Adds a new request to the database and returns the autogenerated key
   */
  pushAndReturnKey(request) {
    return Promise.all([
      this._getDatabase(),
      this._serialize(request)
    ]).then(values => {
      let db = values[0];
      let serialized = values[1];

      const tx = db.transaction(this.queueStoreName, 'readwrite');
      let objectStore = tx.objectStore(this.queueStoreName);
      let requestAdd = objectStore.add(serialized);
      
      return requestAdd.then((key) => {
        return Promise.resolve(key);
      });
    });
  }

  /**
   * Deletes the first item in the queue
   */
  unshift() {
    return this._getDatabase().then(db => {
      const tx = db.transaction(this.queueStoreName, 'readwrite');
      return tx.objectStore(this.queueStoreName).openCursor().then(cursor => {
        return new Promise((resolve, reject) => {
          var value = cursor.value;
          cursor.delete().then(() => {
            resolve(cursor.value);
          }).catch(() => {
            reject();
          });
        });
      });
    });
  }
	
	deleteItem(queue_id) {
		return this._getDatabase().then(db => {
      let tx = db.transaction(this.queueStoreName, 'readwrite');
      let objectStore = tx.objectStore(this.queueStoreName);
			return new Promise((resolve, reject) => {
				objectStore.delete(queue_id).then(() => {
					resolve();
				})
				.catch(() => {
					reject();
				});
			});
		});
	}

  /**
   * Returns the first item in the queue
   */
  first() {
    return this._getDatabase().then(db => {
      const tx = db.transaction(this.queueStoreName, 'readonly');
      return tx.objectStore(this.queueStoreName).openCursor().then(cursor => {
        if (!cursor) return null;
        return [cursor.key, cursor.value];
      });
    })
  }

  /**
   * Returns all items in the queue that match a criteria
   */
  getItems(method, url, key, value) {
    return this._getDatabase().then(db => {
    	var items = [];
      const tx = db.transaction(this.queueStoreName, 'readonly');
      tx.objectStore(this.queueStoreName).iterateCursor(cursor => {
        if (cursor && cursor.value.body) {
          var body = JSON.parse(cursor.value.body);
          if ((cursor.value.method === method)
            && (cursor.value.url.includes(url))
            && (body.hasOwnProperty(key))
            && (body[key] === value)) {
            body.queueKey = cursor.key;
            items.push(body);
          }
        	cursor.continue();
        };
      });

      return tx.complete.then(() => {
      	return items;
      })
      .catch(() => {
      	return
      });
    }).then(result => {
      if (!result) return null;
      return result;
    });
  }

  /**
   * Returns a Promise that resolves after executing the given function on every queue item.
   * The given function must return a Promise.
   * QUESTION: Should the callback be given a serialized request or a Request?
   */
  map(callback) {
    return this._getDatabase().then(db => {
      const tx = db.transaction(this.queueStoreName, 'readwrite');
      tx.objectStore(this.queueStoreName).iterateCursor(cursor => {
        if (!cursor) return;
        callback(cursor).then(() =>
          cursor.continue()
        );
      });
      return tx.complete;
    });
  }

  /**
   * Returns the length of the queue
   */
  length() {
    return this._getDatabase().then(db => {
      const tx = db.transaction(this.queueStoreName, 'readonly');
      return tx.objectStore(this.queueStoreName).count();
    });
  }

  /**
   * Returns the database, creating the object store if needed
   */
  _getDatabase() {
    const dbPromise = idb.open(this.databaseName, this.version, upgradeDB => {
      switch (upgradeDB.oldVersion) {
        case 0:
          upgradeDB.createObjectStore(this.queueStoreName, { autoIncrement: true });
      }
    });

    // dbPromise resolves with a reference to the db
    return dbPromise;
  }

  /**
   * You can't store a Request object in IndexedDB so you need to convert it into a regular
   * object first. See: https://serviceworke.rs/request-deferrer_service-worker_doc.html
   */
  _serialize(request) {
    var headers = {};

    for(var entry of request.headers.entries()) {
      headers[entry[0]] = entry[1];
    }
    var serialized = {
      url: request.url,
      headers: headers,
      method: request.method,
      mode: request.mode,
      credentials: request.credentials,
      cache: request.cache,
      redirect: request.redirect,
      referrer: request.referrer
    };

    if(request.method !== 'GET' && request.method !== 'HEAD') {
      return request.clone().text().then(function(body) {
        serialized.body = body;
        return Promise.resolve(serialized);
      });
    }
    return Promise.resolve(serialized);
  }
}