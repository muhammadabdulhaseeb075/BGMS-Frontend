angular.module('openlayers-directive').directive('olexFeatureOverlay', ['olHelpers', 'olexHelper', function(olHelpers, olexHelper) {
	/*extending openlayers-directive to add a draw function */

	/**
	 * @function
	 * @description
	 * Adds listeners to layers to listen for changes in opacity i.e. if the layer is hidden, it
	 * removes the feature overlay, and when the layer is made visible again, it adds back the
	 * feature overlay.
	 */
	var addLayerListeners = function(olLayers, layerKey, features, featureOverlay, map){
		if(olLayers != {}){
            angular.forEach(olLayers, function(olLayer, index, collection){
                if(olLayer){
                    var lk2 = olLayer.on('change:opacity', function(evt){
                        console.log('change:opacity');
                        if(olLayer.getOpacity()===0)
                            featureOverlay.setMap(null);
                        else
                            featureOverlay.setMap(map);
                    });
                    layerKey.push(lk2);
                    if(olLayer.getSource().constructor===ol.source.Cluster){
                        //if it is a cluster source, wait for the clusters to be redrawn and then redraw feature overlay
//                        if(!olLayer.get(scope.properties.name)){
//                            olLayer.set(scope.properties.name, true);
                            var lk3 = olLayer.on('change', function(evt){
                                console.log('changefeature');
                                featureOverlay.getSource().clear(true);
                                // featureOverlay.getSource().addFeatures(olexHelper.getOlFeatures(features, collection, map));
                            });
                            layerKey.push(lk3);
//                        }
                    }
                }
            });
        }
	};

    return {
        restrict: 'E',
        scope: {
            /*
                Properties are of the type
                {
                    'name': name,
                    'style': style as used in openlayers-angular-directive or style function
                }
            */
            properties: '=olexFeatureOverlayProperties'
        },
        replace: false,
        require: '^openlayers',
        link: function(scope, element, attrs, controller) {
            var isDefined   = angular.isDefined;
            var equals      = angular.equals;
            var createStyle = olHelpers.createStyle;
            var olScope     = controller.getOpenlayersScope();

            olScope.getMap().then(function(map) {
                console.log(featureOverlay);
                scope.view = map.getView();
                scope.olLayers = {};
                scope.layerKey = [];
                var featureOverlay = new ol.layer.Vector({
                    style: scope.properties.style,
                    map: map,
                    source: new ol.source.Vector({
                        useSpatialIndex: false // optional, might improve performance
                      }),
                    updateWhileAnimating: true, // optional, for instant visual feedback
                    updateWhileInteracting: true // optional, for instant visual feedback
                });
                scope.$watchCollection('properties.features', function(newFeatures, oldFeatures){
                    console.log('added features to '+scope.properties.name);
                  //  debugger;
                  	console.log(newFeatures);
                    for (var index in newFeatures){
                    	var feature = newFeatures[index];
                    	// if(!scope.olLayers[feature.layer] && feature.layer != "cluster"){
                    	if(!scope.olLayers[feature.layer]){
                    		var layers = olexHelper.getOlLayers(map, feature.layer, !feature.isLayerGroup);
                    		addLayerListeners(layers, scope.layerKey, newFeatures, featureOverlay, map)
                    		angular.extend(scope.olLayers, layers);
                    	}
                    }
                    //TODO: ISSUE possibly is here for clustering keep highlighting.
                    scope.layerKey.push(lk1);
                    
                    featureOverlay.getSource().clear(true);
                    featureOverlay.getSource().addFeatures(olexHelper.getOlFeatures(newFeatures, scope.olLayers, map));
                    //FIN: TODO
                });

                var lk1 = scope.view.on('change:resolution', function(evt){
                        console.log('change:resolution:'+evt.target.getResolution());
                        featureOverlay.getSource().clear(true);
                        //featureOverlay.getSource().getFeatures()
                        featureOverlay.getSource().addFeatures(olexHelper.getOlFeatures(scope.properties.features, scope.olLayers, map));
                });

                scope.$on('$destroy', function() {
                    console.log("scope.on destroy start");
                    // featureOverlay.getSource().clear(true);
                    featureOverlay.setMap(null);
                    ol.Observable.unByKey(key);
                    for (var i = scope.layerKey.length - 1; i >= 0; i--) {
                        console.log("scope.on destroy");
                        ol.Observable.unByKey(scope.layerKey[i]);
                    }
                    console.log("scope.on destroy end");
                });

            });
        }
    };
}]);
