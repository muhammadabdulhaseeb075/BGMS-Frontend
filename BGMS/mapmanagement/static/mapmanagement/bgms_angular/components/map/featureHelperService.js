angular.module('bgmsApp.map').service('featureHelperService', ['$q', function($q){
	/*
		FeatureOverlays represented by object of type:
	*/

	var view_model = this;

	/**
	 * @function
	 * @description
	 * Separates the layer name(marker_type) from the canonical id and returns
	 * the canonical id.
	 * @param {ol.Feature} feature - the feature from which to extract the canonical id
	 */
	view_model.getFeatureId = function(feature){
		if(!feature || !feature.getId())
			return null;
		var feature_id = feature.getId();
		if(typeof feature_id === 'string' && feature_id.indexOf(';')!=-1){
			feature_id = feature_id.substring(feature_id.indexOf(';')+1);
		}
		return feature_id;
	};

	/**
	 * @function
	 * @description
	 * Sets the feature id to 'marker_type;feature_id' (if marker_type exists),
	 * where marker_type is a property of the feature.
	 * @param {string|number} feature_id_opt - New Id for the feature. If it is 
	 * not passed, it gets the current id from the feature.
	 */
	view_model.setFeatureId = function(feature, feature_id_opt){
		if(!feature)
			return null;
		if(!feature_id_opt)
			feature_id_opt = feature.getId();
		var layer_name_opt = feature.get('marker_type');
		if(typeof feature_id_opt === 'string' && feature_id_opt.indexOf(';')!=-1){
			feature_id_opt = feature_id_opt.substring(feature_id_opt.lastIndexOf(';')+1);
		}
		if(feature_id_opt)
			feature.setId(feature_id_opt);
	};

	/**
	 * @function
	 * @description
	 * Sets the specified geometry as the geometry for the feature with the
	 * specified id
	 * @param {ol.Geometry} geometry - geometry to set for the feature
	 * @param {ol.Feature} feature - feature modified in place
	 * @returns {ol.Feature}  modified feature
	 */
	view_model.setFeatureGeometry = function(feature, geometry){
		if(feature && geometry)
			feature.setGeometry(geometry);
		return feature;
	};

	/**
	 * @function
	 * @description
	 * Creates a feature with the specified geometry and id
	 * @param {ol.Geometry} geometry - geometry to set for the feature
	 * @param {string|number} id_opt - (optional) id to set for the feature
	 * @returns {ol.Feature}  the created feature
	 */
    view_model.createFeature = function(geometry, id){
    	if(!geometry || !id)
    		return null;
    	var feature = new ol.Feature(geometry);
    	if(id){
    		feature.setId(id);
				feature.setProperties({
					id: id
				});
    	}
    	return feature;
    };

    /**
     * @function
     * @description
     * Adds a feature to the specified layer name
     * @param {ol.Feature} feature - the feature to be moved
     * @param {string} layer_name - name of the layer it needs to be moved to
     */
    view_model.addFeatureToLayer = function(feature, layer_name){
    	var added_feature = $q.defer();
    	if(!feature && !layer_name)
    		added_feature.reject('missing parameters');
			window.OLMap.getLayers().forEach(function(layer){
				if(layer.get('name') === layer_name){
					layer.getSource().addFeature(feature);
						feature.set('marker_type', layer_name);
						view_model.setFeatureId(feature);
						added_feature.resolve(feature);
				}
			})
    	return added_feature.promise
    };

    /**
     * @function
     * @description
     * Gets a feature from the specified layer
     * @param {string|number} feature_id - the id of the feature to be obtained
     * @param {string} layer_name - name of the layer it needs to be obtained from
     * @returns the promise of the feature
     */
    view_model.getFeatureFromLayer = function(feature_id, layer_name){
    	var feature = $q.defer();
    	if((typeof feature_id === 'string') && feature_id.indexOf(';')!=-1)
    		feature_id = feature_id.substring(feature_id.indexOf(';')+1);
    	console.log(feature_id);
			window.OLMap.getLayers().forEach(function(layer){
				if(layer.get('name') === layer_name)
					feature.resolve(layer.getSource().getFeatureById(feature_id));
			});
    	return feature.promise;
    };

    /**
     * @function
     * @description
     * Removes the feature from the layer specified by layer_name
     * @param {ol.Feature|string|number} feature_or_id - the feature or the id of the feature
     * @param {string} layer_name - name of the layer where the feature is located
     * @returns promise of the removed feature
     */
    view_model.removeFeatureFromLayer = function(feature_or_id, layer_name){
    	var feature = $q.defer();
    	if(!feature_or_id || !layer_name)
    		feature.reject('invalid input');
    	else{
				window.OLMap.getLayers().forEach(function(layer){
					var temp_feature = null;
					if(layer.get('name') === layer_name){
								if((typeof feature_or_id === 'object') && (feature_or_id.constructor === ol.Feature))
									temp_feature = feature_or_id;
								else
									temp_feature = layer.getSource().getFeatureById(feature_or_id);
								if(temp_feature){
									layer.getSource().removeFeature(temp_feature);
									feature.resolve(temp_feature);
								}
					}
				});
    	}
    	return feature.promise;
    };

    /**
     * @function
     * @description
     * Removes all the features from the specified layer
     * @param {string} layerName - the name of the layer to be cleared
     */
    view_model.removeAllFeaturesFromLayer = function(layerName){
			window.OLMap.getLayers().forEach(function(layer){
				if(layer.get('name') === layerName){
					layer.getSource().clear(true);
				}
			});
    };

    /**
     * @function
     * @description
     * Removes the specified feature from the from_layer specified and
     * adds it to the new layer specified.
     * @param {ol.Feature|string} feature_or_id - the feature or id of the feature to be moved
     * @param {string} from_layer_name - the name of layer from which to remove feature
     * @param {string} to_layer_name - the name of the layer to which the feature must be added
     */
    view_model.moveFeatureBetweenLayers = function(feature_or_id, from_layer_name, to_layer_name){
    	var moved_feature = $q.defer();
    	if(!feature_or_id && !from_layer_name && !to_layer_name)
    		moved_feature.reject('missing parameters');
    	view_model.removeFeatureFromLayer(feature_or_id, from_layer_name).then(function(feature){
			if(feature){
    			view_model.addFeatureToLayer(feature, to_layer_name).then(function(added_feature){
    				moved_feature.resolve(added_feature);
    			});
    		}
    	});
    	return moved_feature.promise;
    };


    /**
     * @function
     * @description
     * Adds the listener_function as a geometry change listener function to the feature
     * @param {ol.Feature} feature - the feature to which the change listener is to be added
     * @param {function} listener_function - function to be the change listener
     * @param {string} to_layer_name - the name of the layer to which the feature must be added
     * @returns unique listener key to be used to detach the listenergoog.events.Key
     */
    view_model.addGeometryListener = function(feature, listener_function){
    	if(!feature)
    		return null;
    	return feature.on('change:geometry', listener_function);
    };


    /**
     * @function
     * @description
     * Adds the listener_function as a geometry change listener function to the feature
     * @param {ol.Feature} feature - the feature to which the change listener is to be added
     * @param {function} listener_function - function to be the change listener
     * @param {string} to_layer_name - the name of the layer to which the feature must be added
     * @returns unique listener key to be used to detach the listenergoog.events.Key
     */
    view_model.removeGeometryListener = function(feature, listener_function_or_key){
    	if(!feature || !listener_function_or_key)
    		return null;
    	if(typeof listener_function_or_key === 'function')
    		feature.un('change:geometry', listener_function_or_key);
    	else
    		ol.Observable.unByKey(listener_function_or_key);
    };

}]);
