angular.module('bgmsApp.map').service('personInteractionService', ['$http', '$filter', 'eventService', 'featureOverlayService', 'markerService', 'personService', 'featureHelperService', 'notificationHelper','memorialService', 'reservedPersonService', '$q', '$timeout',
function($http, $filter, eventService, featureOverlayService, markerService, personService, featureHelperService, notificationHelper, memorialService, reservedPersonService, $q, $timeout){
	var view_model = this;

	view_model.groupName = 'person';
	view_model.hoverMarkerName = 'person-hover-details';

	/**
	 * @description
	 * contains the feature overlays used - hovered-memorials, clicked-memorials and searched-memorials
	 */
    view_model.featureOverlays = {};
    
    /**
     * @returns {boolean} True if this is a touch screen device
     */
    view_model.isTouchDevice = function() {
      return (('ontouchstart' in window)
      || (navigator.MaxTouchPoints > 0)
      || (navigator.msMaxTouchPoints > 0));
    }

	/**
	 * @function
	 * @description
	 * Adds/removes the event to show persons on hover of memorial or plot.
     * Don't add event to touch screens.
	 * @param {boolean} true to add, false to remove
	 * @returns {undefined}
	 */
	view_model.detailsOnHoverEvent = function(enable){
    if (!view_model.isTouchDevice()) {
			if(enable){
				eventService.pushEvent({
					group: view_model.groupName,
					name: 'hoverMemorialDetails',
					layerGroup: ['memorials', 'memorial_cluster'],
					layerNames: ['plot', 'reserved_plot'],
					type: 'pointermove',
					handler: view_model.showDetailsOnHover
				});
			} 
			else
				eventService.removeEventByName('hoverMemorialDetails');
    }
	};

	/**
	 * @function
	 * @description
	 * Adds/removes the event to highlight related features on hover of memorial or plot.
     * Don't add event to touch screens.
	 * @param {boolean} true to add, false to remove
	 * @returns {undefined}
	 */
	view_model.highlightOnHoverEvent = function(enable){
		if (!view_model.isTouchDevice()) {
			if(enable){
				eventService.pushEvent({
					group: view_model.groupName,
					name: 'hoverSelectFeatures',
					layerGroup: ['memorials', 'memorial_cluster'],
					layerNames: ['plot', 'reserved_plot', 'available_plot', 'pet_grave'],
					type: 'pointermove',
					handler: view_model.selectIconsOnHover
				});
			} 
			else {
				eventService.removeEventByName('hoverSelectFeatures');
			}
    }
	};

	/**
	 * @function
	 * @description
	 * Shows/hides the marker(specified by name) based on whether there is a coordinate to display at.
	 * @param {String} markerName
	 * @param {ol.Coordinate} coordinate to display at
	 * @param {object} template object containing the scope and url of the relevant partial
	 * @returns {undefined}
	 */
	view_model.toggleDetailsMarker = function(markerName, coordinate, template){
		markerService.removeMarkerByName(markerName);
		if(coordinate){
			window.setTimeout(() => {
				markerService.pushMarker({
					group: 'person-hover',
					name: markerName,
					positioning: ['bottom-left','top-left'],
					tooltip: {
						"bottom-left":"ol-popup-bottom",
						"top-left": "ol-popup-top"
					},
					offset: {
						"bottom-left":[-47, -21],
						"top-left":[-47, 21]
					},
					position: coordinate,
					template: template
				});
			});
		}
	};


  /**
   * Return true if the feature is already selected, otherwise false
   * @param  {ol.feature} feature
   * @return {boolean}
   */
  view_model.isFeatureSelected = function(feature){
  	var allMarkers = markerService.getMarkers();
    for(var i = 0; i < allMarkers.length; i++) {
      if (allMarkers[i].featureId === feature.getId()) {
          return true;
      }
    }
    return false;
  };

	view_model.currentCoordinate;

	view_model.selectIconsOnHover = function(evt, features){
		
		let feature = features[0];

		// show pointed while hovering over a feature
		if (feature)
			view_model.togglePointerOverFeature(evt.map, true);
		else
			view_model.togglePointerOverFeature(evt.map, false);
		
		const overlayExistsForFeature = view_model.featureOverlays['hovered-memorials'] && view_model.featureOverlays['hovered-memorials'].featureExistsInOverlay(featureHelperService.getFeatureId(feature));

		if (!feature || !overlayExistsForFeature) {
			view_model.featureOverlays['hovered-memorials'].removeAllFeatures();

			if(feature)
				view_model.addMemorialsToOverlay(featureHelperService.getFeatureId(feature), evt.coordinate, 'hovered-memorials', 'hover');
			else
				view_model.toggleDetailsMarker(view_model.hoverMarkerName);
		}
	};

	view_model.eventCreated = false;

	view_model.showDetailsOnHover = function(evt, features){

		// Add event to reset coordinates once mouse moves offscreen.
		// Otherwise coordinates freezes at last point on map.
		if (!view_model.eventCreated) {
			view_model.eventCreated = true;
			evt.map.getViewport().addEventListener('mouseout', function(evt){
				view_model.currentCoordinate = null;
      }, false);
		}

		view_model.currentCoordinate = evt.coordinate;

		//considering only 1st feature because only one memorial layer (cluster/geojson) is active at a time
		let feature = features[0];

		// If the mouse has stopped, i.e. hasn't moved during the duration of the timeout
    if (evt.coordinate === view_model.currentCoordinate && feature && !view_model.isFeatureSelected(feature)){
			//hovering on top of memorial
			view_model.getPersonsUnmarkedGravesFromFeature(feature)
			.then(function(personsUnmarkedGraves) {
				var personArray = personsUnmarkedGraves["personArray"];
				var personsReserved = personsUnmarkedGraves["personsReserved"];
				var noOfUnmarkedGraves = personsUnmarkedGraves["noOfUnmarkedGraves"];
				var memorialId = personsUnmarkedGraves["memorialId"];
				// ugly json to array done to prevent duplicate values appearing
				var arr = Object.keys(personArray).map(function(k) { return personArray[k] });

				var arrpr = Object.keys(personsReserved).map(function(k) { return personsReserved[k] });
				var template = view_model.createDetailsTemplate(arr, arrpr, noOfUnmarkedGraves, memorialId);
				var template_2 = view_model.createMarkerTemplate(arr, arrpr, noOfUnmarkedGraves, memorialId);

				if(template)
					{view_model.toggleDetailsMarker(view_model.hoverMarkerName, evt.coordinate, template)}
				else if (template_2)
					{view_model.toggleDetailsMarker(view_model.hoverMarkerName, evt.coordinate, template_2)}
				else 
					{view_model.toggleDetailsMarker(view_model.hoverMarkerName)};
			});
		}
		else
			view_model.toggleDetailsMarker(view_model.hoverMarkerName);
	};

	/**
	 * @function
	 * @description
	 * Creates and returns the template object, by populating its scope
	 * and setting its template.
	 * @param array of persons to be shown
	 * @param no of unknown persons in the cluster
	 */
	view_model.createDetailsTemplate = function(personArray, personsReserved, noOfUnmarkedGraves, memorialId){
		var itemsPerPage = 5;
		personArray = $filter('orderBy')(personArray,
			function(person){
				if(person.burial_date === 'Unknown')
					return 0;
				else
					return person.burial_date;
			},
			true);
		var template = {
			component: 'ClusterDetailsMarker',
			scope: {
				persons: personArray,
				personsReserved: personsReserved,
				noOfUnmarkedGraves: noOfUnmarkedGraves,
				memorialId: memorialId,
				personsPage: personArray.slice(0, itemsPerPage),
				personsReservedPage: personsReserved.slice(0, itemsPerPage),
				totalItems: personArray.length + personsReserved.length,
				currentPage: 1,
				itemsPerPage:itemsPerPage,
				closeHandler: view_model.hideClickDetails,
				maxSize: 5
			}
		}
		return template;
	};
	// create Only Surname Template
	view_model.createMarkerTemplate=function(personArray, personsReserved, noOfUnmarkedGraves, memorialId){
		var itemsPerPage = 5;
		personArray = $filter('orderBy')(personArray,
			function(person){
				if(person.burial_date === 'Unknown')
					return 0;
				else
					return person.burial_date;
			},
			true);
		var template_2 = {
			component: 'DisplayNameMarker',
			scope: {
				persons: personArray,
				personsReserved: personsReserved,
				noOfUnmarkedGraves: noOfUnmarkedGraves,
				memorialId: memorialId,
				personsPage: personArray.slice(0, itemsPerPage),
				personsReservedPage: personsReserved.slice(0, itemsPerPage),
				totalItems: personArray.length + personsReserved.length,
				currentPage: 1,
				itemsPerPage:itemsPerPage,
				closeHandler: view_model.hideClickDetails,
				maxSize: 5
			}
		}
		return template_2;
	}


	view_model.getPersonsUnmarkedGravesFromFeature = function(feature){
		// debugger;
		var personArray = {};
		var personsReservedArr = {};
		var clusterArray = feature.get('features');
		if(!clusterArray){
			// normal geojson feature
			clusterArray = [feature];
		}

		let deferred = $q.defer();

		//if noOfUnmarkedGraves > 1, the template shows "Unknown graves" instead of person's name
		let noOfUnmarkedGraves = clusterArray.length;
		let memorialId;
		let memorialIdsArray = [];

		// get memorial_ids for memorials in cluster
		for (var i = clusterArray.length - 1; i >= 0; i--) {
			memorialId = featureHelperService.getFeatureId(clusterArray[i]);
			memorialIdsArray.push(memorialId);

			//memorialId is graveplot.uuid
			var personsReserved = reservedPersonService.getPersonsReservedByPlotId(memorialId);

			if(personsReserved){
				//Substract in case reservedPersons came from available plot
				angular.extend(personsReservedArr, personsReserved);
				for (var j = 0; j < personsReserved.length; j++) {
					if(reservedPersonService.getOrigin(personsReserved[j]) === 'available_plot'){
						noOfUnmarkedGraves--;
					}
				}
			}
		}

		personService.getPersonsByMemorialIds(memorialIdsArray)
		.then(function(result) {

			persons = result.persons;
			knownMemorials = result.knownMemorials;
			//Substract people from unmarked graves to show Unknown grave in the pop up
			/*if(persons && persons.length > 0){
				angular.extend(personArray, persons);
				noOfUnmarkedGraves--;
			}*/

			if (knownMemorials)
				noOfUnmarkedGraves = noOfUnmarkedGraves - knownMemorials.length

			// note: when we need memorialId there will only be one feature
			deferred.resolve({"personArray": persons, "noOfUnmarkedGraves": noOfUnmarkedGraves, "personsReserved": personsReservedArr, "memorialId": memorialId});
		});

		return deferred.promise;
	};

	view_model.togglePointerOverFeature = function(map, enable){
		map.getTarget().style.cursor = enable ? 'pointer' : '';
	};

	view_model.addMemorialsToOverlay = function(memorialId, memorialCoordinate, overlayName, featureNamePrefix){
		// featureOverlayService.removeAllFeatures(overlayName);
		var memorials = [], features = [];
		if(memorialId){
			var memorial = memorialService.getMemorialById(memorialId);
			if(memorial){
				memorials.push(memorial);
				var layer_name = memorial.layername;
				personService.getPersonsByMemorialIds([memorialId])
				.then(function(result) {
					let persons = result.persons;
					for (var key in persons){
						memorials.push.apply(memorials,persons[key].getMemorials());
					}
					for (var key in memorials){
						features.push({
							name: memorials[key].id+memorials[key].layername+featureNamePrefix,
							feature: memorials[key].id,
							layer: memorials[key].layername,
							isLayerGroup:false
						});
					}
					view_model.featureOverlays[overlayName].addFeatures(features);
				});
			}
		}
		if(memorialCoordinate) {
			view_model.featureOverlays[overlayName].addFeature({
				name: 'cluster-'+featureNamePrefix,
				feature: memorialCoordinate,
				layer: 'cluster',
				isLayerGroup:false
			});
		}
	};

	view_model.hideClickDetails = function(){
		markerService.removeMarkersByGroup('person');
		markerService.removeMarkersByGroup('person-hover');
		if(view_model.featureOverlays['clicked-memorials'])
			view_model.featureOverlays['clicked-memorials'].removeAllFeatures();
		view_model.detailsOnHoverEvent(true);

		featureOverlayService.removeAllFeaturesInGroup('hovered-memorials');
		featureOverlayService.removeAllFeaturesInGroup('clicked-memorials');

	};

}]);
