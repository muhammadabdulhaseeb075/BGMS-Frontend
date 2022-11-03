angular.module('bgmsApp.map').controller('addGraveController', ['$scope', '$http', '$modal', '$sce', 'memorialService', 'interactionService', 'eventService', 'markerService', 'addGraveService', 'featureOverlayService', 'personService', 'toolbarService', 'notificationHelper', 'geometryHelperService', 'featureHelperService', 'floatingPlotToolbarService', 'modalHelperService',
  function($scope, $http, $modal, $sce, memorialService, interactionService, eventService, markerService, addGraveService, featureOverlayService, personService, toolbarService, notificationHelper, geometryHelperService, featureHelperService, floatingPlotToolbarService, modalHelperService) {
    /*

	It adds/removes the following overlays:
		add-grave-message overlay


	It adds/removes the following layers:
		add-grave-layer


	It adds/removes the following interactions:
		add_grave : select (onselect and onunselect), modify, draw (onDrawEnd)

    It adds/removes the following events
        pointermove
	*/

    var view_model = this;

    view_model.plot_feature = null;
    view_model.plot_layer = null;

    view_model.toggle = toolbarService.get_toggle();

    /*
     * @param {String} name of event
     * @return {undefined}
     */
    view_model.burialToolbarHandler = function(eventType, $event) {

      switch (eventType) {
        case 'create_plot':
          toolbarService.toggle_option('create_plot').then(function(is_selected) {
            if (is_selected)
              view_model.createPlotInteraction();
          });
          break;
        case 'edit_plot':
          toolbarService.toggle_option('edit_plot').then(function(is_selected) {
            if (is_selected) {
              view_model.editPlotInteraction(eventType);
            }
          });
          break;
        default:
          view_model.deactivateUI();
          break;
      }
    };

    /**
     * @function
     * @description
     * Creates the events required to generate a plot
     */
    view_model.createPlotInteraction = function() {
      //create a plot and add it to the layer
      var geometry = geometryHelperService.createPolygonGeometry('rectangle', [0, 0], 0.9, 2);
      var plot_feature = featureHelperService.createFeature(geometry, view_model._generateUUID());
      featureHelperService.addFeatureToLayer(plot_feature, addGraveService.addedGraveplotLayer);
      //add events
      eventService.pushEvent({
        group: 'add_grave',
        name: 'move-plot',
        type: 'pointermove',
        handler: angular.bind(view_model, addGraveService.plotMoveHandler, plot_feature)
      });

      //on placing plot, create the floating options handler at plot location
      eventService.pushEvent({
        group: 'add_grave',
        name: 'place-plot',
        type: 'click',
        handler: angular.bind(view_model, view_model.placePlotHandler, plot_feature, addGraveService.addedGraveplotLayer)
      });

      eventService.pushEvent({
        group: 'burialTools',
        name: 'addPlot',
        type: 'pointermove',
        handler: addGraveService.addPlotMoveHandler
      });
    };

    /**
     * @function
     * @description
     * Creates events required to edit plot
     */
    view_model.editPlotInteraction = function(eventType) {
      view_model.selectPlotEvents(view_model.editPlotHandler,eventType);
      eventService.pushEvent({
        group: 'burialTools',
        name: 'editPlot',
        type: 'pointermove',
        handler: addGraveService.editPlotMoveHandler
      });

      eventService.pushEvent({
        group: 'add_grave',
        name: 'highlight-grave',
        layerNames: ['plot', 'available_plot', 'reserved_plot', 'pet_grave'],
        type: 'pointermove',
        handler: addGraveService.highlightHoveredPlots
      });
    };

    /**
     * function
     */
    view_model.selectPlotEvents = function(handlerFunction, eventType) {
      //on placing plot, create the floating options handler at plot location

      var layerNames = ['plot', 'available_plot', 'pet_grave'];
      if (eventType == 'edit_plot'){
        layerNames.push('reserved_plot');
      }

      eventService.pushEvent({
        group: 'add_grave',
        name: 'select-plot',
        layerNames: layerNames,
        layerGroup: ['memorials'],
        type: 'click',
        handler: handlerFunction
      });
    };

    view_model.editPlotHandler = function(evt, features, layerNames) {
      if (features[0]) {
        addGraveService.stopBurialTools();
        floatingPlotToolbarService.initialise(features[0]).then(function(is_closing) {
          if (is_closing) {
            //toggle off when toolbar is removed
            toolbarService.simulated_click('edit_plot');
            featureHelperService.removeGeometryListener(features[0], addGraveService.placeToolbarAtFeature);
          }
        });
        addGraveService.placeToolbarAtFeature({
          target: features[0]
        });
        featureHelperService.addGeometryListener(features[0], addGraveService.placeToolbarAtFeature);
        interactionService.pushInteraction({
          group: 'add_grave',
          type: 'translate',
          parameters: {
            feature: {
              featureId: features[0].getId(),
              layerName: features[0].get('marker_type')
            }
          }
        });
        eventService.removeEventsByGroup("burialTools");
        markerService.removeMarkersByGroup("burialTools");
      }
    };

    view_model._generateUUID = function() {
      var d = new Date().getTime();
      if(performance && typeof performance.now === "function"){
          d += performance.now(); // use high-precision timer if available
      }
      var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
          var r = (d + Math.random()*16)%16 | 0;
          d = Math.floor(d/16);
          return (c=='x' ? r : (r&0x3|0x8)).toString(16);
      });
      return uuid;
    };

    // Unused function AFAICT
    view_model.createBurialPlotEvents = function() {
      //create a plot and add it to the layer
      var geometry = geometryHelperService.createPolygonGeometry('rectangle', [0, 0], 0.9, 2);
      var plot_feature = featureHelperService.createFeature(geometry, view_model._generateUUID());
      featureHelperService.addFeatureToLayer(plot_feature, addGraveService.addedGraveplotLayer);
      //    	add events
      console.log('createAddBurialPlotInteraction');
      eventService.pushEvent({
        group: 'add_grave',
        name: 'move-plot',
        type: 'pointermove',
        handler: angular.bind(view_model, view_model.plotMoveHandler, plot_feature)
      });

      //on placing plot, create the floating options handler at plot location
      eventService.pushEvent({
        group: 'add_grave',
        name: 'place-plot',
        type: 'click',
        handler: angular.bind(view_model, view_model.placePlotHandler, plot_feature, addGraveService.addedGraveplotLayer)
      });

      eventService.pushEvent({
        group: 'burialTools',
        name: 'addPlot',
        type: 'pointermove',
        handler: addGraveService.addPlotMoveHandler
      });
    };

    view_model.plotMoveHandler = function(feature, evt) {
      var coordinate = evt.coordinate;
      var geometry = feature.getGeometry();
      var originalLocation = geometry.getFirstCoordinate();
      geometry.translate(coordinate[0] - originalLocation[0], coordinate[1] - originalLocation[1]);
    };

    view_model.placePlotHandler = function(feature, layerName, evt) {
      //    	floatingPlotToolbarService.cleanup();
      floatingPlotToolbarService.initialise(feature).then(function(is_closing) {
        if (is_closing) {
          //toggle off when toolbar is removed
          toolbarService.simulated_click('create_plot');
          featureHelperService.removeGeometryListener(feature, addGraveService.placeToolbarAtFeature);
        }
      });
      console.log('view_model.placeRectangle');
      addGraveService.placeToolbarAtFeature({
        target: feature
      });
      featureHelperService.addGeometryListener(feature, addGraveService.placeToolbarAtFeature);
      eventService.removeEventsByGroup('add_grave');
    };
  }
]);
