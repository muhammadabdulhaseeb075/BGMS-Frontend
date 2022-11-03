angular.module('bgmsApp.map').service('floatingMemorialToolbarService', ['$timeout', '$q', '$rootScope', '$http', 'styleService', 'notificationHelper', 'interactionService', 'eventService', 'featureOverlayService', 'geometryHelperService', 'featureHelperService', 'markerService', 'memorialService', 'personService', 'layerService', 'layerGroupService', 'layerSelectionService', 'personInteractionService', 'securityService',
  function ($timeout, $q, $rootScope, $http, styleService, notificationHelper, interactionService, eventService, featureOverlayService, geometryHelperService, featureHelperService, markerService, memorialService, personService, layerService, layerGroupService, layerSelectionService, personInteractionService, securityService) {

    var view_model = this;
    view_model.addedGraveplotLayer = 'add-memorials';
    view_model.defaultMemorialLayer = 'gravestone';
    view_model.layer_type = view_model.defaultMemorialLayer;
    this.feature = null;
    this.feature_under = null;
    this.original_geometry = null;
    this.shape = "gravestone";
    this.editedFeatureOverlay = null;
    this.rotateAxisFeatureOverlay = null;
    this.rotateInProgress = false;
    view_model.mouseMoveMarker = null;
		view_model.isSaving = false;
		view_model.isDeleting = false;

    view_model.memorial_dictionary = {
			square: {
				small: {
					type: 'rectangle',
					dim1: 0.6,
					dim2: 0.6
				},
				large: {
					type: 'rectangle',
					dim1: 0.9,
					dim2: 0.9
				}
			},
			large_square: {
				small: {
					type: 'rectangle',
					dim1: 2,
					dim2: 2
				}
			},
			war_memorial: {
				small: {
					type: 'rectangle',
					dim1: 0.9,
					dim2: 0.9
				}
			},
			circle: {
				small: {
					type: 'circle',
					dim1: 0.65
				}
			},
			gravestone: {
				small: {
					type: 'rectangle',
					dim1: 0.65,
					dim2: 0.18
				}
			},
			plaque: {
				small: {
					type: 'rectangle',
					dim1: 1.15,
					dim2: 0.12
				}
			},
			square_plaque: {
				small: {
					type: 'rectangle',
					dim1: 0.3,
					dim2: 0.3
				}
			},
			window: {
				small: {
					type: 'rectangle',
					dim1: 2,
					dim2: 0.22
				}
			},
			table_tomb: {
				small: {
					type: 'rectangle',
					dim1: 2,
					dim2: 0.9
				}
			},
			rectangle1: {
				 small: {
					type: 'rectangle',
					dim1: 0.2,
					dim2: 0.3
				 }
			}
    };

    this.is_closing = null;


    view_model.initialise = function (feature, feature_under) {
		view_model.cleanup_internal();
		view_model.is_closing = $q.defer();
		view_model.feature = feature;
		view_model.feature_under = feature_under;
		view_model.layer_type = feature.get('marker_type');
		if (!view_model.layer_type || view_model.layer_type == view_model.addedGraveplotLayer){
			view_model.layer_type = view_model.defaultMemorialLayer;
		}
		// feature overlay to highlight current memorial being edited
		//initialise overlay
		if (view_model.editedFeatureOverlay === null) {
			view_model.editedFeatureOverlay = featureOverlayService.addFeatureOverlay({
				name: 'edited-memorials',
				group: 'add_memorial',
				layerGroup: ['memorials'],
				style: window.addedStyleFunction
			});
		}
		view_model.editedFeatureOverlay.addFeature({
			name: feature.getId(),
			feature: feature,
			layer: feature.get('marker_type'),
			isLayerGroup: false
		});
		//add move plot interaction
		view_model.movePlotInteraction(feature, feature_under);
		//save original coordinates
		view_model.original_geometry = feature.getGeometry().clone();
		layerSelectionService.checkLayer(view_model.layer_type);
		//layerSelectionService.setFeature(feature);
		if (!view_model.isGraveAddMarker(feature)) {
			const assignUserAllowedPromise = view_model.assign_user_allowed();
			const assignUserGeneratedPromise = view_model.assign_user_generated_allowed(feature.getId());
			Promise.all([assignUserAllowedPromise, assignUserGeneratedPromise]).then(function () {
			 	// If is AG_staff never remove the interaction translate with the memorial
				if (!view_model.user_allowed && !view_model.user_generated_allowed) {
					view_model.removeMovePlotInteraction();
				}
			})
		}
		return view_model.is_closing.promise;
	};


    view_model.assign_user_allowed = function (){
    	return new Promise( (resolve) => {
			securityService.get_groups().then(function (request) {
				const groups = request.data.groups;
				if (groups) {
					view_model.user_allowed = groups.includes('Superuser') || groups.includes('AG_staff');
				} else {
					view_model.user_allowed = false
				}
				resolve(true)
			});
		});
	}

	view_model.assign_user_generated_allowed = function (feature_id){
    	 return new Promise( (resolve) => {
    	 	memorialService.getBackendMemorialById(feature_id).then(function (request){
				view_model.user_generated_allowed = request.data.user_generated;
				resolve(true)
    	 	});
    	 });
	}

	view_model.isGraveAddMarker = function (feature){
		return feature.get('marker_type') === view_model.addedGraveplotLayer
  	}

    view_model.getMouseMoveMarker = function () {
			if (!view_model.mouseMoveMarker) {
				view_model.mouseMoveMarker = markerService.pushMarker({
					group: 'memorialTools',
					name: 'memorialMessage',
					class: 'tooltip',
					positioning: ['top-center', 'top-center'],
					offset: {
						"top-center": [0, 30]
					}
				});
			}
			return view_model.mouseMoveMarker;
    };

    view_model.addMemorialLinkHandler = function (evt) {
			var marker = view_model.getMouseMoveMarker();
			marker.position = evt.coordinate;
			marker.message = "Click plot to link to memorial";
    };

    view_model.addMemorialMoveHandler = function (evt) {
			var marker = view_model.getMouseMoveMarker();
			marker.position = evt.coordinate;
			marker.message = "Click map to add memorial";
    };

    view_model.editMemorialMoveHandler = function (evt) {
			var marker = view_model.getMouseMoveMarker();
			marker.position = evt.coordinate;
			marker.message = "Click memorial to edit";
    };

    view_model.addMemorialImageMoveHandler = function (evt) {
			var marker = view_model.getMouseMoveMarker();
			marker.position = evt.coordinate;
			marker.message = "Click memorial to add memorial images";
    };

    view_model.addMemorialCaptureMoveHandler = function (evt) {
			var marker = view_model.getMouseMoveMarker();
			marker.position = evt.coordinate;
			marker.message = "Click the memorial you wish to edit";
    };

    view_model.floatingOptionsHandler = function (eventName, option) {
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
            view_model.rotateMemorialInteraction(feature);
            break;
          case 'selectShape':
						var value = option;
						view_model.shape = option;
						feature.setGeometry(geometryHelperService.createPolygonGeometry(view_model.memorial_dictionary[value].small.type,
							geometry.getInteriorPoints().getFirstCoordinate(),
							view_model.memorial_dictionary[value].small.dim1,
							view_model.memorial_dictionary[value].small.dim2));
						break;
          case 'selectLayer':
						var new_layer_type = option;
						var old_layer_type = feature.get('marker_type');
						view_model.layer_type = option;
						feature.setStyle(window.MapLayers.layerStyles[option](feature));
						break;
          case 'saveMemorial':
						view_model.isSaving = true;
						this.isSaving = view_model.isSaving;
            var oldLayer = layerName, newLayer = layerName;
						//            if (oldLayer === view_model.addedGraveplotLayer)
						newLayer = view_model.layer_type;
            view_model.saveMemorial(feature, newLayer, this);
            break;
          case 'linkPlot':
						view_model.selectPlotEvents(view_model.linkPlotHandler);
						break;
          case 'deleteMemorial':
						view_model.isDeleting = true;
						this.isDeleting = view_model.isDeleting;
						var childScope = this;
						notificationHelper.createConfirmation(messages.toolbar.memorial.delete.confirmation.title, messages.toolbar.memorial.delete.confirmation.text, function () {
							view_model.deleteMemorial(featureHelperService.getFeatureId(feature), layerName, childScope);
						}, function () {
							childScope.isDeleting = false;
						});
            break;
          case 'cancel':
						var childScope = this;
						var msgNoti = feature.get('marker_type') === "add-memorials" ? messages.toolbar.memorial.cancel.confirmation.textForNew : messages.toolbar.memorial.cancel.confirmation.text;
        	  	notificationHelper.createConfirmation(messages.toolbar.memorial.cancel.confirmation.title, msgNoti, function () {
							//setting isSaving to true, this is used in add-memorial-toolbar.html to enable/disable save button
							view_model.isSaving = true;
	            	childScope.isSaving = view_model.isSaving;
							view_model.saveMemorial(feature, view_model.layer_type, childScope);
						}, function () {
							view_model.cancelSave();
						});
            break;
          default:
						return; //do default
        }
      }
    };

    view_model.rotateMemorialInteraction = function (feature) {
    	 if (feature) {
				if (!view_model.rotateAxisFeatureOverlay) {
	        	view_model.rotateAxisFeatureOverlay = featureOverlayService.addFeatureOverlay({
						name: 'add_memorial',
						group: 'add_memorial',
						layerName: view_model.addedGraveplotLayer,
						style: styleService.drawInteractionStyleFunction
					});
				}
				if (view_model.rotateInProgress) {
					view_model.stopMemorialRotate(feature);
					//add move plot interaction
					view_model.movePlotInteraction(feature, view_model.feature_under);
				}
				else
					view_model.memorialRotate(feature);
      }
    };

    view_model.memorialRotate = function (feature) {
			if (feature) {
				// disable memorial popups
				personInteractionService.detailsOnHoverEvent(false);

				//adding a feature overlay to show the rotation axis
				view_model.rotateAxisFeatureOverlay.removeAllFeatures();

				geometryHelperService.rotateFeature(feature);
				view_model.rotateInProgress = true;
			}
		};

		view_model.stopMemorialRotate = function (feature) {
			if (view_model.rotateAxisFeatureOverlay)
				view_model.rotateAxisFeatureOverlay.removeAllFeatures();
			if (feature) {
				geometryHelperService.stopRotateFeature(feature);
			}
			view_model.rotateInProgress = false;

			// enable memorial popups
			personInteractionService.detailsOnHoverEvent(true);
		};

		view_model.movePlotInteraction = function (feature, feature_under) {

			var feature_vals = {
				featureId: feature.getId(),
				layerName: feature.get('marker_type'),
			};

			if(typeof feature_under !== 'undefined'){
				feature_vals.featureIdunder = feature_under.getId();
				feature_vals.layerNameunder = feature_under.get('marker_type');
			}

			interactionService.pushInteraction({
				group: 'add_memorial',
				type: 'translate',
				parameters: {
					feature: feature_vals
				}
			});
		};

		view_model.removeMovePlotInteraction = function () {
			interactionService.removeInteractionsByGroup('add_memorial');
		};


		view_model.saveMemorial = function (feature, newLayerName, childScope) {
			//http post to save plot, which send as response a geojson of only that plot
			var cloned_feature = feature.clone();
			featureHelperService.setFeatureId(cloned_feature, feature.getId());
			oldLayerName = feature.get('marker_type');
			var url = null;
			if (oldLayerName === view_model.addedGraveplotLayer)
				url = '/mapmanagement/addHeadstone/';
			else
				url = '/mapmanagement/updateMemorial/';
			var geojsonFormatter = new ol.format.GeoJSON();
			var geoJSONFeature = geojsonFormatter.writeFeature(feature);
			var jsonObject = angular.fromJson(geoJSONFeature);
			jsonObject.id = featureHelperService.getFeatureId(feature);
			//        if (oldLayerName === view_model.addedGraveplotLayer)
			jsonObject.properties.marker_type = newLayerName;
      jsonObject.properties.old_marker_type = oldLayerName;
			$http.post(url, {
				'geojsonFeature': angular.toJson(jsonObject)
			}).
				success(function (data, status, headers, config) {
					console.log('success');
					console.log(data);
					var returnedFeature = geojsonFormatter.readFeature(data);
					view_model.feature = feature;
					if (newLayerName != oldLayerName) {

						//if layer doesn't exist because this it he first memorial of this type
						if (!layerService.getLayerByName(newLayerName)) {
							layer = layerService.createLayer({
								name: newLayerName,
								display_name: newLayerName.replace('_', ' ').replace( /\b./g, function(a){ return a.toUpperCase(); } ),
								show_in_toolbar: true,
								switch_on_off: true,
								group: 'memorials',
								visibility: true,
								source: {
									type: 'EmptyVector'
								},
								index: layerGroupService.getLayerGroupByName('memorials').hierarchy,
								defer: $q.defer(),
								style: window.MapLayers.layerStyles[newLayerName]
							});
              jQuery(document).trigger('addLayer', layer);
							layerGroupService.getLayerGroupByName('memorials').addLayer(layer);

							//wait until layer has been created, then finish saving and refresh person and add-memorial events to include new layer
							layer.defer.promise.then(function () {
								if (oldLayerName === view_model.addedGraveplotLayer)
									featureHelperService.setFeatureId(feature, returnedFeature.get('id'));
								if (!memorialService.getMemorialById(featureHelperService.getFeatureId(feature)))
									memorialService.createMemorialFromGeoJSONFeature(data);
								else {
									memorialService.getMemorialById(featureHelperService.getFeatureId(feature)).layername = newLayerName;
								}
								featureHelperService.removeFeatureFromLayer(feature, oldLayerName);
								featureHelperService.addFeatureToLayer(feature, newLayerName);
								//refreshing events
								var personEvents = eventService.getEventsByGroup('person');
								for (var index in personEvents) {
									personEvents[index].addLayerNames(newLayerName);
								}
							});
						} else {
							if (oldLayerName === view_model.addedGraveplotLayer)
								featureHelperService.setFeatureId(feature, returnedFeature.get('id'));
							if (!memorialService.getMemorialById(featureHelperService.getFeatureId(feature)))
								memorialService.createMemorialFromGeoJSONFeature(data);
							else {
								memorialService.getMemorialById(featureHelperService.getFeatureId(feature)).layername = newLayerName;
							}
							featureHelperService.removeFeatureFromLayer(feature, oldLayerName);
							featureHelperService.addFeatureToLayer(feature, newLayerName);
						}
					}

					notificationHelper.createSuccessNotification(messages.toolbar.memorial.save.success.title);
					if (oldLayerName === view_model.addedGraveplotLayer) {
						this.feature = returnedFeature;
						view_model.isSaving = true;
						if (childScope) {
							childScope.isSaving = view_model.isSaving;
						}
						notificationHelper.createConfirmation(messages.toolbar.memorial.confirmationAfterSuccess.title, messages.toolbar.memorial.confirmationAfterSuccess.text,
							function () {
								view_model.selectPlotEvents(view_model.linkPlotHandler);
								view_model.isSaving = false;
								if (childScope) {
									childScope.isSaving = view_model.isSaving;
								}
							},
							function () {
								view_model.cleanup();
								view_model.isSaving = false;
								if (childScope) {
									childScope.isSaving = view_model.isSaving;
								}
							});
					} else {
						view_model.cleanup();
						view_model.isSaving = false;
						if (childScope) {
							childScope.isSaving = view_model.isSaving;
						}
					}
				}).
				error(function (data, status, headers, config) {
					notificationHelper.createErrorNotification(messages.toolbar.memorial.save.fail.title);
					view_model.isSaving = false;
					if (childScope) {
						childScope.isSaving = view_model.isSaving;
					}
				});
		};

		view_model.cancelSave = function () {
			view_model.feature.setGeometry(view_model.original_geometry);
			view_model.feature.setStyle(undefined);
			view_model.cleanup();
		};

		view_model.selectPlotEvents = function (handlerFunction) {
			//on placing plot, create the floating options handler at plot location
			eventService.pushEvent({
				group: 'add_memorial',
				name: 'select-plot',
				layerNames: ['plot', 'available_plot', 'pet_grave'],
				type: 'click',
				handler: handlerFunction
			});
			eventService.pushEvent({
				group: 'burialTools',
				name: 'addMemorialImageMsj',
				type: 'pointermove',
				handler: view_model.addMemorialLinkHandler
			});
		};

		view_model.linkPlotHandler = function (evt, features, layerNames) {
			if (features[0] && features[0].get('marker_type') === 'plot') {
    		  var memorial_id = featureHelperService.getFeatureId(view_model.feature);
				var memorial_layer = view_model.feature.get('marker_type');
				var plot_id = featureHelperService.getFeatureId(features[0]);
				var url = '/mapmanagement/linkHeadstonePlot/';
				notificationHelper.createConfirmation(messages.toolbar.plot.linkMemorial.confirmation.title, messages.toolbar.plot.linkMemorial.confirmation.text, function () {
					$http.post(url, {
						'memorial_id': memorial_id,
						'plot_id': plot_id
					}).
						success(function (data, status, headers, config) {
							console.log('success');
							console.log(data);
							var geojsonFormatter = new ol.format.GeoJSON();
							var returnedFeature = geojsonFormatter.readFeature(data);
							featureHelperService.setFeatureId(view_model.feature, returnedFeature.get('id'));
							notificationHelper.createSuccessNotification(messages.toolbar.plot.linkMemorial.success.title);

							view_model.saveMemorial(view_model.feature, view_model.feature.get('marker_type'));
							view_model.cleanup();
						}).
						error(function (data, status, headers, config) {
							notificationHelper.createErrorNotification(messages.toolbar.plot.linkMemorial.fail.title);
						});
				}, view_model.cleanup);
			} if (features[0] && features[0].get('marker_type') === 'available_plot') {
    		  notificationHelper.createErrorNotification(messages.toolbar.plot.linkMemorial.error.title);
			}

		};

		view_model.deleteMemorial = function (featureId, layerName, childScope) {

      // Detect if the memorial is linked to a person
			personService.getPersonsByMemorialIds([featureId])
			.then(function(result) {
				let persons = result.persons;
				if (persons && persons.length > 0) {
					notificationHelper.createErrorNotification(messages.toolbar.memorial.delete.attatchedPersonFail.title);
					view_model.isDeleting = false;
					if (childScope) {
						childScope.isDeleting = view_model.isDeleting;
					}
				}
				else {
					$http.post('/mapmanagement/deleteHeadstone/', {
						'memorial_id': featureId,
						'marker_type': layerName
					}).
					success(function (data, status, headers, config) {
						console.log('success');
						console.log(data);
						featureHelperService.removeFeatureFromLayer(featureId, layerName);
						notificationHelper.createSuccessNotification(messages.toolbar.memorial.delete.success.title);
						view_model.cleanup();
						view_model.isDeleting = false;
						if (childScope) {
							childScope.isDeleting = view_model.isDeleting;
						}
					}).
					error(function (data, status, headers, config) {
						notificationHelper.createErrorNotification(messages.toolbar.memorial.delete.fail.title + data);
						view_model.isDeleting = false;
						if (childScope) {
							childScope.isDeleting = view_model.isDeleting;
						}
					});
				}
			});
		};

		view_model.cleanup_internal = function () {
			eventService.removeEventsByGroup("burialTools");
			markerService.removeMarkersByGroup("memorialTools");
			view_model.mouseMoveMarker = null;
			view_model.stopMemorialRotate(view_model.feature);
			view_model.removeMovePlotInteraction();

		};

		view_model.cleanup = function () {
			view_model.cleanup_internal();
			if (view_model.is_closing) {
				view_model.is_closing.resolve(true);
			}
			//          featureHelperService.removeAllFeaturesFromLayer(view_model.addedGraveplotLayer);
			//          if(view_model.feature)
			//          	featureHelperService.removeGeometryListener(view_model.feature, view_model.placeToolbarAtFeature);
		};
	}]);
