angular.module('bgmsApp.map').service('floatingPlotToolbarService', ['$q', '$rootScope', '$http', 'styleService', 'notificationHelper', 'interactionService', 'eventService', 'featureOverlayService', 'geometryHelperService', 'featureHelperService', 'markerService', 'layerSelectionService', 'personInteractionService',
  function($q, $rootScope, $http, styleService, notificationHelper, interactionService, eventService, featureOverlayService, geometryHelperService, featureHelperService, markerService, layerSelectionService, personInteractionService){

    var view_model = this;
    view_model.addedGraveplotLayer = 'add-plots';
    view_model.availablePlotLayer = 'available_plot';
    view_model.reservedPlotLayer = 'reserved_plot';
    this.feature = null;
    this.original_geometry = null;
    this.editedFeatureOverlay = null;
    this.rotateAxisFeatureOverlay = null;
    this.rotateInProgress = false;

    this.is_closing = null;

    view_model.plot_dictionary = {
			default_plot:{
				  type:'rectangle',
    			dim1: 0.9,
    			dim2: 2
			},
			cremation_plot:{
				  type:'rectangle',
    			dim1: 0.5,
    			dim2: 0.5
			}
    };

    view_model.initialise = function(feature){
    	view_model.cleanup_internal();
    	view_model.is_closing = $q.defer();
        //create feature overlay to highlight current plot being edited
    	if(!view_model.editedFeatureOverlay){
    		view_model.editedFeatureOverlay =
    	    	featureOverlayService.addFeatureOverlay({
    	    		name: 'edited-plots',
    	    		group: 'add_grave',
    	    		layerName: ['plot', 'available_plot', 'pet_grave'],
    	    		style: window.addedStyleFunction
    	    	});
    	}
    	view_model.feature = feature;
    	//create feature overlay to highlight current plot being edited
    	view_model.editedFeatureOverlay.addFeature({
			name: feature.getId(),
			feature: feature,
			layer: feature.get('marker_type')
		});
		//save original coordinates
		view_model.original_geometry = feature.getGeometry().clone();
		//add move plot interaction
		view_model.movePlotInteraction(feature);
    layerSelectionService.setFeature(feature);
		return view_model.is_closing.promise;
    };

    view_model.floatingOptionsHandler = function(eventName, option) {
      console.log('view_model.floatingOptionsHandler');
      if (view_model.feature) {
    	  var feature = view_model.feature;
          var layerName = feature.get('marker_type');
          console.log(layerName);
    	var geometry = feature.getGeometry();
        var featureCoordinates = angular.copy(geometry.getCoordinates());
        switch (eventName) {
          case 'rotatePlot':
            view_model.removeMovePlotInteraction();
            view_model.rotatePlotInteraction(feature);
            break;
          case 'selectShape':
        	  var value = option;
        	  feature.setGeometry(geometryHelperService.createPolygonGeometry(view_model.plot_dictionary[value].type,
        			  geometry.getInteriorPoints().getFirstCoordinate(),
        			  view_model.plot_dictionary[value].dim1,
        			  view_model.plot_dictionary[value].dim2));
              break;
          case 'savePlot':
            var oldLayer = layerName, newLayer = layerName;
            if (oldLayer === view_model.addedGraveplotLayer)
            	newLayer = view_model.availablePlotLayer;
            view_model.savePlot(feature, newLayer);
            break;
          case 'deletePlot':
          	notificationHelper.createConfirmation(messages.toolbar.plot.delete.confirmation.title, messages.toolbar.plot.delete.confirmation.text, function(){
                view_model.deletePlot(featureHelperService.getFeatureId(feature), layerName);
          	});
            break;
          case 'cancel':
        	notificationHelper.createConfirmation(messages.toolbar.plot.cancel.confirmation.title, messages.toolbar.plot.cancel.confirmation.text, function(){
                var oldLayer = layerName, newLayer = layerName;
                if (oldLayer === view_model.addedGraveplotLayer)
                	newLayer = view_model.availablePlotLayer;
	            view_model.savePlot(feature, newLayer);
        	}, function(){
        		view_model.cancelSave();
        	});
            break;
          default:
        	  return; //do default
        }
      }
    };

    view_model.rotatePlotInteraction = function(feature){
    	 if (feature) {
	        if(!view_model.rotateAxisFeatureOverlay){
	        	view_model.rotateAxisFeatureOverlay =
              featureOverlayService.addFeatureOverlay({
                name: 'add_grave',
                group: 'add_grave',
                layerName: view_model.addedGraveplotLayer,
                style: styleService.drawInteractionStyleFunction
              });
	        }
          if (view_model.rotateInProgress) {
            view_model.stopPlotRotate(feature);
            //add move plot interaction
            view_model.movePlotInteraction(feature);
          }
          else
            view_model.plotRotate(feature);
      }
    };

    view_model.plotRotate = function(feature) {
      if (feature) {
				// disable memorial popups
				personInteractionService.detailsOnHoverEvent(false);
        //adding a feature overlay to show the rotation axis
        view_model.rotateAxisFeatureOverlay.removeAllFeatures();

        geometryHelperService.rotateFeature(feature);
        view_model.rotateInProgress = true;
      }
    };

    view_model.stopPlotRotate = function(feature) {
      if(view_model.rotateAxisFeatureOverlay)
        view_model.rotateAxisFeatureOverlay.removeAllFeatures();
      if(feature){
        geometryHelperService.stopRotateFeature(feature);
      }
			view_model.rotateInProgress = false;

			// enable memorial popups
			personInteractionService.detailsOnHoverEvent(true);
    };

    view_model.movePlotInteraction = function(feature) {
        interactionService.pushInteraction({
          group: 'add_grave',
          type: 'translate',
          parameters: {
            feature: {
              featureId: feature.getId(),
              layerName: feature.get('marker_type')
            }
          }
        });
    };

    view_model.removeMovePlotInteraction = function() {
      interactionService.removeInteractionsByGroup('add_grave');
    };


    view_model.savePlot = function(feature, newLayerName) {
      //http post to save plot, which send as response a geojson of only that plot
      var cloned_feature = feature.clone();
      featureHelperService.setFeatureId(cloned_feature, feature.getId());
      oldLayerName = feature.get('marker_type');
      var url = null;
      if (oldLayerName === view_model.addedGraveplotLayer)
        url = '/mapmanagement/addAvailablePlot/';
      else
        url = '/mapmanagement/updatePlot/';
      var geojsonFormatter = new ol.format.GeoJSON();
      var geoJSONFeature = geojsonFormatter.writeFeature(feature);
      var jsonObject = angular.fromJson(geoJSONFeature);
      jsonObject.id = featureHelperService.getFeatureId(feature);
      if (oldLayerName === view_model.addedGraveplotLayer)
        jsonObject.properties.marker_type = newLayerName;
      $http.post(url, {
            'geojsonFeature': angular.toJson(jsonObject)
      })
      .then(function(response) {
        let data = response.data;
        let geometry = data.geometry;
        console.log('success');
        console.log(geometry);
        var returnedFeature = geojsonFormatter.readFeature(geometry);
        featureHelperService.setFeatureId(returnedFeature, returnedFeature.get('id'));
        if(newLayerName!=oldLayerName){
          featureHelperService.removeFeatureFromLayer(feature, oldLayerName);
          featureHelperService.addFeatureToLayer(returnedFeature, newLayerName);
        }
        let text = "";
        if (data['updated_section'] || data['updated_subsection']) {
          text = "Graveplot's ";
          let sectionAndSubsection = data['updated_section'] && data['updated_subsection'];
          
          if (data['updated_section']) 
            text += "section";

          if (sectionAndSubsection)
            text += " and ";
          
          if (data['updated_subsection'])
            text += "subsection";

          if (sectionAndSubsection)
            text += " have";
          else
            text += " has";

          text += " been updated for the new location."
        }
        notificationHelper.createSuccessNotification(messages.toolbar.plot.save.success.title, text);
        view_model.cleanup();
      })
      .catch(function(response) {
        let text = "";
        if (response.data['error_updating_section']) {
          text = "There was an error updating the graveplot's section and/or subsection:\<br>" + response.data['error_updating_section'];
        }
        notificationHelper.createErrorNotification(messages.toolbar.plot.save.fail.title, text);
      });
    };

    view_model.cancelSave = function(){
    view_model.feature.setGeometry(view_model.original_geometry);
    view_model.cleanup();
    };

    view_model.deletePlot = function(featureId, layerName) {
      if (layerName === view_model.availablePlotLayer || layerName === view_model.reservedPlotLayer) {
        $http.post('/mapmanagement/deletePlot/', {
          'plot_id': featureId,
          'layer_name': layerName
        }).
        success(function(data, status, headers, config) {
          console.log('success');
          console.log(data);
          featureHelperService.removeFeatureFromLayer(featureId, layerName);
          notificationHelper.createSuccessNotification(messages.toolbar.plot.delete.success.title);
          view_model.cleanup();
        }).
        error(function(data, status, headers, config) {
        notificationHelper.createErrorNotification(messages.toolbar.plot.delete.fail.title);
        });
      }else{
        notificationHelper.createErrorNotification(messages.toolbar.plot.delete.fail.title);
      }
    };

    view_model.cleanup_internal = function(){
        eventService.removeEventsByGroup("burialTools");
        markerService.removeMarkersByGroup("burialTools");
        view_model.stopPlotRotate(view_model.feature);
        view_model.removeMovePlotInteraction();
    };

    view_model.cleanup = function(){
      view_model.cleanup_internal();
        if(view_model.is_closing){
          view_model.is_closing.resolve(true);
        }
//          featureHelperService.removeAllFeaturesFromLayer(view_model.addedGraveplotLayer);
//          if(view_model.feature)
//          	featureHelperService.removeGeometryListener(view_model.feature, view_model.placeToolbarAtFeature);
      };
}]);
