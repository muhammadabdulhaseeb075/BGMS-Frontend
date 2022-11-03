angular.module('bgmsApp.map').service('addMemorialService', ['$rootScope', '$http', 'eventService', 'featureOverlayService', 'markerService', 'interactionService', 'geometryHelperService', 'featureHelperService', 'notificationHelper', 'floatingMemorialToolbarService',
                                                             function($rootScope, $http, eventService, featureOverlayService, markerService, interactionService, geometryHelperService, featureHelperService, notificationHelper,floatingMemorialToolbarService){

	var view_model = this;

    view_model.addedMemorialsLayer = 'add-memorials';
    view_model.availablePlotLayer = 'available_memorials';
    view_model.defaultMemorialLayer = 'gravestone';
    view_model.memorialLayerGroup = 'memorials';
    view_model.hoverFeatureOverlay = null;
    view_model.floatingToolbarMarker = null;
    view_model.addedFeature = undefined;

    view_model.memorialMoveHandler = function(feature, evt) {
      var coordinate = evt.coordinate;
      var geometry = feature.getGeometry();
      var originalLocation = geometry.getFirstCoordinate();
      geometry.translate(coordinate[0] - originalLocation[0], coordinate[1] - originalLocation[1]);
      view_model.addedFeature = feature;
      //TODO: view_model.feature = feature
    };

    view_model.getFloatingToolbarMarker = function(offset, feature, name){
    	if(!view_model.floatingToolbarMarker){

        view_model.floatingToolbarMarker = markerService.pushMarker({
          group: 'add_memorial',
          name: name,
          positioning: ['top-left', 'top-left'],
          offset: {
            // "bottom-left": [-47, 51],
            // "top-left": [-47, 51]
            "bottom-left": offset,
            "top-left": offset
          },
          template: {
            component: 'AddMemorialToolbarMarker',
            scope: { feature: feature }
          },
        });

        eventService.pushEvent({
          group: 'add_memorial',
          name: 'floating-toolbar',
          type: 'moveend',
          handler: angular.bind(view_model,markerService.handleRelocationFloatingToolbar, feature),
        });

        //TODO: create service to add events to features in Angular2.
        // var inttras = interactionService.getInteractionByType('translate');
        feature.on("change", function (e) {
            // console.log(e);
            markerService.handleRelocationFloatingToolbar(e.target);
        });

    	}
    	return view_model.floatingToolbarMarker;
    };

    view_model.placeToolbarAtFeature = function(evt) {
      var feature = evt.target;
      var geometry = feature.getGeometry();  
      if (geometry.getType() === 'MultiPolygon') {
        position = geometry.getInteriorPoints().getFirstCoordinate();
        var yPosition = 51;
        var offset = markerService.getFloatingToolbarOffset(position, window.OLMap);
        var marker = view_model.getFloatingToolbarMarker(offset, feature, 'memorial-toolbar');
        marker.position = position;

      }
    };

    view_model.highlightHoveredMemorials = function(evt, features, layernames){
    	if(!view_model.hoverFeatureOverlay)
    		view_model.hoverFeatureOverlay = featureOverlayService.addFeatureOverlay({
        		name: 'highlight-memorial',
        		group: 'add_memorial',
        		style: window.MapLayers.layerStyles.selectedStyleFunction
        	});
    	if(features[0]){
        evt.map.getTarget().style.cursor = 'pointer';
    		view_model.hoverFeatureOverlay.addFeature({
				name: features[0].getId()+'highlight-memorial', //todo: change hardcoded to include case multiple plots same location like lych_gate and bench
				feature: features[0], //todo: change hardcoded to include case multiple plots same location like lych_gate and bench
				layer: layernames[0], //todo: change hardcoded to include case multiple plots same location like lych_gate and bench
				isLayerGroup:false
			});
    	} else{
        evt.map.getTarget().style.cursor = '';
    		view_model.hoverFeatureOverlay.removeAllFeatures();
    	}
    };

    view_model.removeToolbarFromFeature = function(feature){
    	featureHelperService.removeGeometryListener(feature, view_model.placeToolbarAtFeature);
    };

    view_model.stopBurialTools = function(feature){
      eventService.removeEventsByGroup('add_memorial');
      featureOverlayService.removeAllFeaturesInGroup('add_memorial');
      markerService.removeMarkersByGroup('add_memorial');
      view_model.floatingToolbarMarker = null;
      interactionService.removeInteractionsByGroup('add_memorial');
      eventService.removeEventsByGroup("burialTools");
      markerService.removeMarkersByGroup("memorialTools");
      floatingMemorialToolbarService.mouseMoveMarker = null;
      featureHelperService.removeAllFeaturesFromLayer(view_model.addedMemorialsLayer);
      floatingMemorialToolbarService.cleanup_internal();
      if(feature)
      	featureHelperService.removeGeometryListener(feature, view_model.placeToolbarAtFeature);
    };


    /**
     * Returns the feature underneath for features memorials after the event cliked is executed
     * @param  {event} evt
     */
    view_model.getFeatureUnderneath = function(evt){
      var mapz = evt.map;
      var fu, fut, ful;
			var features_clicked = mapz.getFeaturesAtPixel(evt.pixel);

      if(features_clicked.length <= 1){
        return fu;
      }

      for(var i=0; i<features_clicked.length; i++){
        fut = features_clicked[i];
        fus = fut.get('marker_type').split('memorials_');

        if (fus.length > 1){
          ful = fus[1];
          for(var j=0; j<features_clicked.length; j++){
            if(features_clicked[j].get('marker_type') == ful){
              return features_clicked[j];
            }
          }
        }
      }
      return fu;
    };

}]);