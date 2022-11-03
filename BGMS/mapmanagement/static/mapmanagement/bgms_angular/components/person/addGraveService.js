angular.module('bgmsApp.map').service('addGraveService', ['$rootScope', '$http', 'eventService', 'featureOverlayService', 'markerService', 'interactionService', 'geometryHelperService', 'featureHelperService', 'notificationHelper', 'floatingPlotToolbarService', function($rootScope, $http, eventService, featureOverlayService, markerService, interactionService, geometryHelperService, featureHelperService, notificationHelper,floatingPlotToolbarService){

	var view_model = this;

    view_model.addedGraveplotLayer = 'add-plots';
    view_model.availablePlotLayer = 'available_plot';
    view_model.burialPlotLayer = 'plot';

    view_model.current_feature = null;

    view_model.mouseMoveMarker = null;
    view_model.floatingToolbarMarker = null;
    view_model.addedFeature = undefined;

    view_model.highlightHoveredPlots = function(evt, features, layernames){
    	if(!view_model.hoverFeatureOverlay)
    		view_model.hoverFeatureOverlay = featureOverlayService.addFeatureOverlay({
        		name: 'highlight-grave',
        		group: 'add_grave',
        		style: window.MapLayers.layerStyles.selectedStyleFunction
        	});
    	if(features[0]){
    		view_model.hoverFeatureOverlay.addFeature({
				name: features[0].getId()+'highlight-grave',
				feature: features[0],
				layer: layernames[0],
				isLayerGroup:false
			});
    	} else{
    		view_model.hoverFeatureOverlay.removeAllFeatures();
    	}
    };

    view_model.getMouseMoveMarker = function(){
    	if(!view_model.mouseMoveMarker){
    		view_model.mouseMoveMarker = markerService.pushMarker({
				group: 'burialTools',
				name: 'burialMessage',
				class: 'tooltip',
				positioning: ['top-center', 'top-center'],
            	offset: {
            		"top-center": [0, 30]
            	}
			});
		}
    	return view_model.mouseMoveMarker;
    };


	view_model.addBurialMoveHandler = function(evt){
		var marker = view_model.getMouseMoveMarker();
		marker.position = evt.coordinate;
		marker.message = "Click plot or memorial to add new burial details";
	};

	view_model.editPlotMoveHandler = function(evt){
		var marker = view_model.getMouseMoveMarker();
		marker.position = evt.coordinate;
		marker.message = "Click plot to edit";
	};

  view_model.editReservedPlotMoveHandler = function(evt){
		var marker = view_model.getMouseMoveMarker();
		marker.position = evt.coordinate;
		marker.message = "Click reserved plot to edit";
	};

	view_model.addPlotMoveHandler = function(evt){
		var marker = view_model.getMouseMoveMarker();
		marker.position = evt.coordinate;
		marker.message = "Click map to add plot";
	};

    view_model.getFloatingToolbarMarker = function(offset){
    	if(!view_model.floatingToolbarMarker){
    		view_model.floatingToolbarMarker = markerService.pushMarker({
                group: 'add_grave',
                name: 'floating-toolbar',
                positioning: ['top-left', 'top-left'],
                offset: {
                  "bottom-left": offset,
                  "top-left": offset
                },
                template: {
                  component: 'AddGraveToolbarMarker',
                  scope: floatingPlotToolbarService
                }
              });
    	}

      eventService.pushEvent({
        group: 'add_grave',
        name: 'floating-toolbar',
        type: 'moveend',
        handler: angular.bind(view_model,markerService.handleRelocationFloatingToolbar, view_model.addedFeature),
      });

      //TODO: create service to add events to features in Angular2.
      view_model.addedFeature.on("change", function (e) {
          markerService.handleRelocationFloatingToolbar(e.target);
      });
    	return view_model.floatingToolbarMarker;
    };

    view_model.createPlotFeature = function(coordinate, distanceX, distanceY) {
        var point0 = coordinate;
        var point1 = [coordinate[0]+distanceX, coordinate[1]];
        var point2 = [coordinate[0]+distanceX, coordinate[1]+distanceY];
        var point3 = [coordinate[0], coordinate[1]+distanceY]
        var plotMultiPolygon = new ol.geom.MultiPolygon([[[point0, point1, point2, point3, point0]]]);
        return new ol.Feature(plotMultiPolygon);
    };

    view_model.plotMoveHandler = function(feature, evt) {
      var coordinate = evt.coordinate;
      var geometry = feature.getGeometry();
      var originalLocation = geometry.getFirstCoordinate();
      geometry.translate(coordinate[0] - originalLocation[0], coordinate[1] - originalLocation[1]);
      view_model.addedFeature = feature;
    };

    view_model.placeToolbarAtFeature = function(evt) {
        var feature = evt.target;
        var geometry = feature.getGeometry();
        var layerName = feature.get('marker_type');
        var position = null;
        view_model.addedFeature = feature;
        if (geometry.getType() === 'MultiPolygon') {
          position = geometry.getInteriorPoints().getFirstCoordinate();
          var yPosition = 71;
          var offset = markerService.getFloatingToolbarOffset(position, window.OLMap);
          var marker = view_model.getFloatingToolbarMarker(offset);
          marker.position = position;
        }
      };

    view_model.removeToolbarFromFeature = function(feature){
    	featureHelperService.removeGeometryListener(feature, view_model.placeToolbarAtFeature);
    };

    view_model.stopBurialTools = function(feature){
      eventService.removeEventsByGroup('add_grave');
      featureOverlayService.removeAllFeaturesInGroup('add_grave');
      markerService.removeMarkersByGroup('add_grave');
      view_model.floatingToolbarMarker = null;
      interactionService.removeInteractionsByGroup('add_grave');
      eventService.removeEventsByGroup("burialTools");
      markerService.removeMarkersByGroup("burialTools");
      view_model.mouseMoveMarker = null;
      featureHelperService.removeAllFeaturesFromLayer(view_model.addedGraveplotLayer);
      floatingPlotToolbarService.cleanup_internal();
      if(feature)
      	featureHelperService.removeGeometryListener(feature, view_model.placeToolbarAtFeature);
    };

}]);
