angular.module('openlayers-directive').service('olexHelper', [function(){
	var view_model = this;
	this.olLayers = {};
	this.olLayerGroups = {};
	
	/**
	 * @description
	 * Initialises the olLayers and olLayerGroups objects
	 */
	view_model.initLayers = function(map){
        map.getLayers().forEach(function(layer){
        	var layerName = layer.get('name');
        	var groupName = layer.get('groupName');
            if(layer && layerName){
            	view_model.olLayers[layerName] = layer;
	            if(groupName){
	            	if(!view_model.olLayerGroups[groupName])
	            		view_model.olLayerGroups[groupName] = {};
	            	view_model.olLayerGroups[groupName][layerName] = layer;
	            	
	            }
            }
        });
	};

	/**
	 * @description
	 * Gets the openlayers layer from map and layer/group name.
	 */
	view_model._getLayer = function(map, name, isLayerName){
		var layers = {};
		var selector = 'groupName', baseObject = this.olLayerGroups;
		if(isLayerName){
			selector = 'name';
			baseObject = this.olLayers;
		}
		var layer = baseObject[name];
		if(!layer){
			view_model.initLayers(map);
			layer = baseObject[name];
		}
		if(layer){ 
			if(!isLayerName)
				layers = layer;
			else
				layers[name] = layer;
		}
		return layers;
	};

	/**
	 * @description
	 * Gets the openlayers layer from map and a single/array of layer/group names.
	 */
	view_model.getOlLayers = function(map, names, isLayerName){
		var layers = {};		
		if(typeof names === 'string'){
			layers = view_model._getLayer(map, names, isLayerName);
		} else{
			// it is an array of layer or group names
			for (var index in names){
				var name = names[index];
				angular.extend(layers, view_model._getLayer(map, name, isLayerName));
			}
		}
		return layers;
	};

//	view_model.getOlLayers = function(map, names, isLayerName){
//		if()
//		var olLayers = {}, selector = 'groupName';
//        if(isLayerName){
//            selector = 'name';
//        }
//		
//		if(names.constructor != Array){
//			var name = names;
//	        map.getLayers().forEach(function(layer){
//	            if(layer && (layer.get(selector) === name)){
//	                olLayers[layer.get('name')] = layer;
//	            }
//	        });
//    	} else{
//            map.getLayers().forEach(function(layer){
//            	for ( var i = names.length-1; i>=0; i--) {
//                    if(layer && (layer.get(selector) === names[i])){
//                        olLayers[layer.get('name')] = layer;
//                    }
//				}
//            });
//    	}
//        
//        return olLayers;
//    }

	/**
	 * @description
	 * Gets the openlayers features from map and a single/array of layer/group names.
	 */
    view_model.getOlFeatures = function(features, layers, map){
        var olFeatures = [], olJSON = {};
        angular.forEach(features, function(value, index, collection){
                var layer = layers[value.layer];
                var resolution = map.getView().getResolution();
                if(layer && layer.getMinResolution()<=resolution && resolution<layer.getMaxResolution() && layer.getOpacity()>0){
                    var feature;
                    if(value.coordinate) {
                        feature = layer.getSource().getFeaturesAtCoordinate(value.coordinate)[0];
                        if(!feature)
                        	feature = layer.getSource().getClosestFeatureToCoordinate(value.coordinate);
                        if(feature)
                        	olJSON[feature.getGeometry().getCoordinates()+'']=(feature);
							// console.log(feature.get('features').length);
                    } else if(value.featureId){
						// console.log(layer.getProperties().name);
                        feature = layer.getSource().getFeatureById(value.featureId);
                        if(feature)
                        	olFeatures.push(feature);
                    } else if(value.feature){
                    	olFeatures.push(value.feature);
                    }
                }
        });
        var olFeatureArray = [];
        olFeatureArray = Object.keys(olJSON).map(function(k) { return olJSON[k] });
        olFeatures.push.apply(olFeatures, olFeatureArray);
        return olFeatures;
    };

}]);