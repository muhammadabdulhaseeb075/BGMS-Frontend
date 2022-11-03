angular.module('openlayers-directive').service('olexInteractionHelper', ['olexHelper', '$rootScope', function(olexHelper, $rootScope){

	//the interactions don't affect dom(according to ol-api) so are moved to a service

	var view_model = this;

	/*Function to create draw interaction */
	view_model.createDrawInteraction = function(parameters, drawSource, handlers){
		//creating a new interaction
		parameters = angular.copy(parameters);
		parameters.source = drawSource;
		var drawInteraction = new ol.interaction.Draw(parameters);
		if(angular.isDefined(handlers)){
			if(angular.isDefined(handlers.drawstart))
				drawInteraction.on('drawstart', handlers.drawstart);
			if(angular.isDefined(handlers.drawend))
				drawInteraction.on('drawend', handlers.drawend);
			// if(angular.isDefined(handlers.drawFeatureChanged))
			// 	drawInteraction.on('drawend', handlers.drawend);
		}

		return drawInteraction;
	};

	view_model.createModifyInteraction = function(layer, handlers, features, style){
		if(!angular.isDefined(features))
			features = new ol.Collection(layer.getSource().getFeatures())
		var modifyInteraction = new ol.interaction.Modify({
		                features: features,
		                style: style
		            });

		if(angular.isDefined(handlers) && angular.isDefined(handlers.modifyend)){
			// var oldHandleEent = modifyInteraction.handleEvent;
			// modifyInteraction.handleEvent = handlers.handleEvent;
			 modifyInteraction.on('modifyend', handlers.modifyend)
		}
		return modifyInteraction;
	};

	view_model.createSelectInteraction = function(layer, parameters, handlers){
		var selectInteraction = new ol.interaction.Select({
			condition: parameters.condition,
			addCondition: parameters.addCondition,
			removeCondition: parameters.removeCondition,
			style: parameters.style,
			layers: [layer]
		});
		console.log(selectInteraction.getProperties());
		if(handlers && handlers.handleSelect){
			selectInteraction.getFeatures().on('add', angular.bind(selectInteraction, handlers.handleSelect));
		}
		if(handlers && handlers.handleUnselect){
			selectInteraction.getFeatures().on('remove', angular.bind(selectInteraction, handlers.handleUnselect));
		}
		return selectInteraction;
	};

	view_model.createPointerInteraction = function(handlers){
		// var creatorObject = {};
		// creatorObject[getPointerType(pointerType)] = handlerFunction;
		return new ol.interaction.Pointer(handlers);
	};

	view_model.createTranslateInteraction = function(features, layer, handlers){
		if(!angular.isDefined(features))
			features = olexHelper.getOlLayers(map, names, isLayerName);
		return new ol.interaction.Translate({features:features});
	};

	view_model.createInteraction = function(properties, layer, features){
		var interaction;
		switch(properties.type){
			case 'draw':
				interaction = view_model.createDrawInteraction(properties.parameters, layer.getSource(), properties.handlers);
				break;
			case 'modify':
				interaction = view_model.createModifyInteraction(layer, properties.handlers, features, properties.parameters.style);
				break;
			case 'select':
				interaction = view_model.createSelectInteraction(layer, properties.parameters, properties.handlers);
				break;
			case 'pointer':
				interaction = view_model.createPointerInteraction(properties.handlers);
				break;
			case 'translate':
				interaction = view_model.createTranslateInteraction(features, layer);
				break;
			default:
				interaction = null;
		}
		return interaction;
	};

}]);