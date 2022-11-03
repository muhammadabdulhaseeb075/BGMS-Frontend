angular.module('openlayers-directive').directive('olexMapInteraction', ['olexInteractionHelper', 'olexHelper', function(olexInteractionHelper, olexHelper) {
	/*extending openlayers-directive to add a draw function */

    return {
        restrict: 'E',
        scope: {
            properties: '=olexInteractionProperties'
        },
        replace: false,
        require: '^openlayers',
        link: function(scope, element, attrs, controller) {
            var isDefined   = angular.isDefined;
            var equals      = angular.equals;
            var olScope     = controller.getOpenlayersScope();
            var createInteraction = olexInteractionHelper.createInteraction;

            olScope.getMap().then(function(map) {
            	var olexInteraction;
                scope.$on('$destroy', function() {
                    map.removeInteraction(olexInteraction);
                });

                if (!isDefined(scope.properties)) {
                    return;
                }

                scope.$watch('properties', function(properties, oldProperties) {
                    if (!isDefined(properties.type)) {
                        return;
                    }

                    var interactionLayer, interactionFeatures;
                    if(isDefined(properties.parameters) && isDefined(properties.parameters.layer)){                        
                        map.getLayers().forEach(function(layer){
                            if(layer.get('name') === properties.parameters.layer)
                                interactionLayer = layer;
                        });
                    }
                    if(isDefined(properties.parameters) && isDefined(properties.parameters.selectFeatures)){
                        interaction = map.getInteractions().forEach(function(element){
                            if(element.constructor === ol.interaction.Select)
                                interactionFeatures = element.getFeatures();
                        });
                    } else if(isDefined(properties.parameters) && isDefined(properties.parameters.layerName)){
                        var layers = olexHelper.getOlLayers(map, properties.parameters.layerName, true);
                        interactionFeatures = new ol.Collection();
                        for (var l in layers){
                        	interactionFeatures.extend(layers[l].getSource().getFeatures());
                        }
                    } else if(isDefined(properties.parameters) && isDefined(properties.parameters.feature)){
                        // Move multiple features together that are in different layers and were passed as parameters
                    	var featureId = properties.parameters.feature.featureId;
                    	var layerName = properties.parameters.feature.layerName;
                    	
                    	var layers = olexHelper.getOlLayers(map, layerName, true);
                    	
                        var feature_collection = [layers[layerName].getSource().getFeatureById(featureId)];

                        if (isDefined(properties.parameters.feature.featureIdunder) && isDefined(properties.parameters.feature.layerNameunder)){
                            var featureId2 = properties.parameters.feature.featureIdunder;
                            var layerName2 = properties.parameters.feature.layerNameunder;
                            var layers2 = olexHelper.getOlLayers(map, layerName2, true);
                            feature_collection.push(layers2[layerName2].getSource().getFeatureById(featureId2));
                        }
                    	interactionFeatures = new ol.Collection(feature_collection);
                    }
                    if (!isDefined(olexInteraction)) {
                        olexInteraction = createInteraction(properties, interactionLayer, interactionFeatures);
                        map.addInteraction(olexInteraction);
                    } else {
                        if (isDefined(oldProperties) && !equals(properties, oldProperties)) {
                            if (!equals(properties.name, oldProperties.name)) {
                                return;
                            } else{
                                var interactionCollection = map.getInteractions();
                                for (var j = 0; j < interactionCollection.getLength(); j++) {
                                    var currentInteraction = interactionCollection.item(j);
                                    if (currentInteraction === olexInteraction) {
                                        interactionCollection.removeAt(j);
                                        olexInteraction = createInteraction(properties, interactionLayer);
                                        if (isDefined(olexInteraction)) {
                                            interactionCollection.insertAt(j, olexInteraction);
                                        }
                                    }
                                }
                            }

                        }
                    }
                }, true);
            });
        }
    };
}]);