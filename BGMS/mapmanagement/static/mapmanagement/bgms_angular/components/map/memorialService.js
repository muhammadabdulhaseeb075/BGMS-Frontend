angular.module('bgmsApp.map').service('memorialService', ['$http', '$q', '$rootScope', 'styleService', 'featureHelperService', 'eventService', 'layerService', 'layerGroupService', 'offlineService',
function($http, $q, $rootScope, styleService, featureHelperService, eventService, layerService, layerGroupService, offlineService){
	/**
	Json object of the type:
	{
		memorial_id: {
			id: memorial_id,
			//TODO: consider multiple plots
			'features': {layername:{layername:'name of layer', centrepoint:'centre coordinate of feature'}},
			'headpoint': ol-coordinate of point,
			'headstone': ol-coordinate of interior point
		},
		:
		:
		:
	}

	**/

	function Feature(centrepoint, layername){
		this.centrepoint = centrepoint;
		this.layername = layername;
	}

	/**
	 * Defining the memorial constructor to use as the model
	 */
	function Memorial(id, centrepoint, layername){
		this.id = id;
		//key-layername, value-feature_object
		this.centrepoint = centrepoint;
		this.layername = layername;

		this.updateOrCreate = function(centrepoint, layername){
			this.layername = layername;
			this.centrepoint = centrepoint;
		};

		this.updateFromGeoJSONFeature = function(geoJsonFeature){
			var memorialDetails = geoJsonFeature.properties;
			if(geoJsonFeature['id'] != null){
				this.id = id;
				var geometry = geoJsonFeature.geometry;
				if(geometry){
					var coordinate;
					if(geometry['type'] === 'Point'){
						coordinate = geometry['coordinates'];
					} else if(geometry['type'] === 'MultiPolygon'){
						coordinate = new ol.geom.MultiPolygon(geometry['coordinates']).getInteriorPoints().getFirstCoordinate();
					}
					this.updateOrCreate(coordinate, memorialDetails['marker_type']);
				}
			}
		};

		this.getCentreCoordinate = function(){
			return this.centrepoint;
	    };
	}

	var view_model = this;

	view_model.memorials = {};

	view_model.getMemorials = function(){
		return view_model.memorials;
	};

	view_model.addMemorial = function(memorial){
		if(!view_model.memorials[memorial.id]);
			view_model.memorials[memorial.id] = memorial;
	};

	view_model.getBackendMemorialById = function(memorialId) {
		return $http.get(`/mapmanagement/memorialDetails/?memorial_uuid=${memorialId}`);
	}

	view_model.getMemorialById = function(memorialId){
			return view_model.memorials[memorialId];
	};

	view_model.removeMemorial = function(memorial){
		if(view_model.memorials[memorial.id])
			view_model.memorials[memorial.id] = null;
	};
	//TODO: duplicated method, why not return undefined? Avoid accessing twice to the dictionary
	view_model.getMemorialById = function(memorialId){
		if(view_model.memorials[memorialId])
			return view_model.memorials[memorialId];
		return null;
	};

	view_model.createMemorialFromGeoJSONFeature = function(geoJsonFeature){
		if(geoJsonFeature['id'] != null){
			var memorial = view_model.getMemorialById(geoJsonFeature['id']);
			if(!memorial){
				memorial = new Memorial(geoJsonFeature['id'])
			}
			memorial.updateFromGeoJSONFeature(geoJsonFeature);
			view_model.addMemorial(memorial);
		}
	};

	view_model.loadMemorialsFromJSON = function(url){
		$http.get(url).
				success(function(data, status, headers, config) {
					var memorials = data.memorials;
					for(var i=0;i<memorials.length;i++){
						var memorial = memorials[i];
						if(memorial['id'] != null){
							view_model.addMemorial(new Memorial(memorial['id'], memorial['centrepoint'],
									memorial['marker_type']));
						}
					}

					console.log('memorialsLoaded!!!!!!!');
					//message used to inform all other controllers that memorials are now loaded
					// and they can proceed to add interactions, etc.
					$rootScope.$broadcast('memorialsLoaded', {'to':'personController'});
				}).
				error(function(data, status, headers, config) {
						console.log('could not load data from ' + config.url);
				});
	}

	/**
	 * Moves a Memorial between layers
	 */
	view_model.moveMemorialToLayer = function(memorial_uuid, layer_name) {

		var movePromise = $q.defer();

    // features in multiple groups including memorials
		if(layer_name === "bench" || layer_name === "lych_gate" || layer_name === "mausoleum") {
			layer_name = "memorials_" + layer_name;
		}

		// If layer doesn't exist, create it
		if (!layerService.getLayerByName(layer_name)) {

			// Creates the layer and adds it to the memorials group
			layer = layerService.createLayer({
				name: layer_name,
				display_name: layer_name.replace('_', ' ').replace( /\b./g, function(a){ return a.toUpperCase(); } ),
				show_in_toolbar: true,
				switch_on_off: true,
				group: 'memorials',
				visibility: true,
				source: {
					type: 'EmptyVector'
				},
				index: layerGroupService.getLayerGroupByName('memorials').hierarchy,
				defer: $q.defer(),
				style: window.MapLayers.layerStyles[layer_name]
			});
      jQuery(document).trigger('addLayer', layer);
			layerGroupService.getLayerGroupByName('memorials').addLayer(layer);

			// When the layer is created
			layer.defer.promise.then(function () {

				// Add the event listeners to it
				var personEvents = eventService.getEventsByGroup('person');
				var memorialEvents = eventService.getEventsByGroup('add_memorial');
				for (var index in personEvents) {
					personEvents[index].addLayerNames(layer_name);
				}
				for (var index in memorialEvents) {
					memorialEvents[index].addLayerNames(layer_name);
				}

				// Get the memorial and move it
				var memorial = view_model.getMemorialById(memorial_uuid);

				var from_layer_name = memorial.layername;

				// features in multiple groups including memorials
				if(from_layer_name === "bench" || from_layer_name === "lych_gate" || from_layer_name === "mausoleum") {
					featureHelperService.removeFeatureFromLayer(memorial_uuid, from_layer_name);
					from_layer_name = "memorials_" + from_layer_name;
				}

				featureHelperService.moveFeatureBetweenLayers(memorial_uuid, from_layer_name, layer_name).then(function() {
					memorial.layername = layer_name;
					movePromise.resolve();
				});

			});

		} else {

			// Get the memorial and move it
			var memorial = view_model.getMemorialById(memorial_uuid);

			var from_layer_name = memorial.layername;

    	// features in multiple groups including memorials
			if(from_layer_name === "bench" || from_layer_name === "lych_gate" || from_layer_name === "mausoleum") {
				featureHelperService.removeFeatureFromLayer(memorial_uuid, from_layer_name);
				from_layer_name = "memorials_" + from_layer_name;
			}

			featureHelperService.moveFeatureBetweenLayers(memorial_uuid, from_layer_name, layer_name).then(function() {
				memorial.layername = layer_name;
				movePromise.resolve();
			});

		}

		return movePromise.promise;
	}
}]);
