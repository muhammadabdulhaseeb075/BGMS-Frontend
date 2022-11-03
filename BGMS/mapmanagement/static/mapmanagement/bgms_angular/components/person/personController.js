angular.module('bgmsApp.map').controller('personController', ['$scope', '$http', '$modal', '$sce', '$filter', '$q', 'personInteractionService', 'layerService', 'featureOverlayService', 'eventService', 'personService', 'markerService', 'memorialService', 'notificationHelper', 'featureHelperService', 'modalHelperService', 'exportMapService','MapService',
  function($scope, $http, $modal, $sce, $filter, $q, personInteractionService, layerService, featureOverlayService, eventService, personService, markerService, memorialService, notificationHelper, featureHelperService, modalHelperService, exportMapService, MapService){

	/*
	The person controller adds/removes the following feature-overlays:
		hovered-features
		clicked-features

	It adds/removes the following overlays:
		person-hover-overlay
		person-click-overlay

	It adds/removes the following events:
		hoverMemorialDetails : pointermove
		clickMemorialDetails : click
	*/

	var view_model = this;
	view_model.memorialsLayerGroup = 'memorials';
	view_model.initialised = $q.defer();

	view_model.init = function(){
		console.log('init called');

		personInteractionService.featureOverlays['hovered-memorials'] = featureOverlayService.addFeatureOverlay('hovered-memorials');
		personInteractionService.featureOverlays['clicked-memorials'] = featureOverlayService.addFeatureOverlay('clicked-memorials');
		personInteractionService.featureOverlays['searched-memorials'] = featureOverlayService.addFeatureOverlay('searched-memorials');

		eventService.pushEvent({
			group: 'person',
			name: 'clickMemorialDetails',
			layerGroup: ['memorials'],
			type: 'click',
			handler: view_model.showMemorialOnClick
		});

		eventService.pushEvent({
			group: 'person',
			name: 'clickGraveInformation',
			layerNames: ['available_plot', 'pet_grave', 'plot', 'reserved_plot'],
			type: 'click',
			handler: view_model.showGraveOnClick
		});

		personInteractionService.highlightOnHoverEvent(true);

		personInteractionService.detailsOnHoverEvent(true);

		view_model.initialised.resolve(true);

	};

	view_model.memorialsLoaded = false;

	$scope.$on('memorialsLoaded', function(event, args) {
		// enables the feature sidebar which requires the memorials to be loaded
		view_model.memorialsLoaded = true;

		view_model.init();
	});

	showFeatureOnClick = function(feature, layerName) {
		if (feature) {
			jQuery(document).trigger('featureSelected', {
				featureID: feature.getId(),
				layerName: layerName
			});
		}
	}

	view_model.showMemorialOnClick = function(evt, features, layerNames) {

    showFeatureOnClick(features[0], layerNames[0]);
	}

	view_model.showGraveOnClick = function(evt, features, layerNames) {
		showFeatureOnClick(features[0], layerNames[0]);
	}

	/**
	 * @function
	 * @description
	 * Function which is called from outside angular to remove
	 * hovered markers.
	 * @returns {undefined}
	 */
	view_model.hideHoverDetails = function(){
		markerService.removeMarkersByGroup('person-hover');
		if(!$scope.$$phase){
	    	$scope.$apply();
	    }
	};

	/**
	 * @function
	 * @description
	 * Function which is called from outside angular to remove
	 * all markers and highlights.
	 * @returns {undefined}
	 */
	view_model.hideClickDetails = function(){
		personInteractionService.hideClickDetails();
		if(!$scope.$$phase){
	    	$scope.$apply();
	    }
	};

	view_model.createSinglePersonHoverTemplate = function(person){
		if(person){
			var message = '';

			if (person.first_names)
				message = person.first_names
			
			if (person.last_name) {
				message += message ? ' ' : '';
				message += person.last_name;
			}

			var template = {
				component: 'HoverDetailsMarker',
				scope: {message: message}
			};
			return template;
		}
	};

	/**
	 * @function
	 * @description
	 * Function which is called from outside angular to simulate a hover
	 * on a person's memorial from the search results.
	 * @returns {undefined}
	 */
	view_model.showSearchHover = function(personId){
		personService.getPersonById(personId)
		.then(function(person) {
			var memorials = null;
			if(person)
				memorials = person.getMemorials();
			if(memorials && memorials.length>0){
				var template = view_model.createSinglePersonHoverTemplate(person);
				for (let i=0;i<memorials.length;i++) {
					personInteractionService.toggleDetailsMarker(personInteractionService.hoverMarkerName + i, memorials[i].getCentreCoordinate(), template);
				}
				if(!$scope.$$phase){
          $scope.$apply();
        }
			}
		});
  };

  /**
	 * @function
	 * @description
	 * Function which is called from outside angular to simulate a hover
	 * on a person's memorial from the search results.
	 * @returns {undefined}
	 */
	view_model.showSearchHover = function(person, featureCentreCoordinates){
    markerService.removeMarkersByGroup('person-hover');

    if(featureCentreCoordinates && featureCentreCoordinates.length>0){
      var template = view_model.createSinglePersonHoverTemplate(person);
      for (let i=0;i<featureCentreCoordinates.length;i++) {
        personInteractionService.toggleDetailsMarker(personInteractionService.hoverMarkerName + i, featureCentreCoordinates[i], template);
      }
    }
    
    if(!$scope.$$phase){
      $scope.$apply();
    }
  };
}]);
