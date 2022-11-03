angular.module('openlayers-directive').directive('olexMapEvent', ['olexHelper', '$rootScope', function(olexHelper, $rootScope) {
    //extending openlayers-directive to add map event handlers

    // used when events are called back to back on the same pixel
    let currentPixel;
    let featuresAtPixel = {};

    var getOLFeatures = function(map, layers, coordinate, pixel, resolution, memorialCapture){
      let features = [], layerNames = [];

      if (!currentPixel || currentPixel != pixel) {
        currentPixel = pixel;
        featuresAtPixel = {};

        if (pixel) {
          // get all features at pixel
          map.forEachFeatureAtPixel(pixel, function (feature) {
            const layer = feature.values_.marker_type;
            if (featuresAtPixel[layer])
              featuresAtPixel[layer].push(feature);
            else
              featuresAtPixel[layer] = [feature];
          });
        }
      }

      angular.forEach(layers, function(layer, layerName){
        if(layer && layer.getMinResolution()<=resolution && resolution<layer.getMaxResolution() && layer.getOpacity()>0){
          var layerFeatures = [];
          if(featuresAtPixel[layerName])
            layerFeatures.push.apply(layerFeatures, featuresAtPixel[layerName]);

          if(layer.getSource().constructor === ol.source.Cluster){
            console.log('cluster layer');
            // need to deal with points in cluster
            var extent = ol.extent.boundingExtent([coordinate]);
            extent = ol.extent.buffer(extent, 7*resolution);
            layer.getSource().forEachFeatureInExtent(extent, function(feature){
              layerFeatures.push(feature);
            });
          }
          else if(layerName === 'memorials'){
            //dealing with memorial points temporarily, very bad fix though
            var extent = ol.extent.boundingExtent([coordinate]);
            extent = ol.extent.buffer(extent, 5*resolution);
            layerFeatures.push.apply(layerFeatures, layer.getSource().getFeaturesInExtent(extent));
          }
          // if memorial capture is enabled, layer is a 'Memorial' group, and there has been no direct hit on a feature, add a buffer
          else if(memorialCapture && layerFeatures.length===0){
            var extent = ol.extent.boundingExtent([coordinate]);
            extent = ol.extent.buffer(extent, 0.5); //0.5m
            var featuresInExtent = layer.getSource().getFeaturesInExtent(extent);
            if (featuresInExtent.length > 1)
              layerFeatures.push.apply(layerFeatures, [layer.getSource().getClosestFeatureToCoordinate(coordinate)]);
            else
              layerFeatures.push.apply(layerFeatures, featuresInExtent);
          }
          for ( var i = layerFeatures.length-1; i>=0; i--) {
            // This is a bit of a hack to make sure other memorials are prioritiesed over grave_kerbs.
            // There must be a way to do this using hierarchy...
            if (layerNames === "grave_kerb") {
              features.push(layerFeatures[i]);
              layerNames.push(layerName);
            }
            else {
              features.unshift(layerFeatures[i]);
              layerNames.unshift(layerName);
            }
          }
        }
      });

      // If true, this means multiple features in different layers are within the extent.
      // We need to find the closest memorial regardless of what layer it is in.
      if (memorialCapture && features.length>1) {
        var vectorSource = new ol.source.Vector();
        vectorSource.addFeatures(features);

        var closestFeature = vectorSource.getClosestFeatureToCoordinate(coordinate);
        features = [closestFeature];
        layerNames = [closestFeature.get("name")];
      }

      return [features, layerNames];
    };

    var hoverCurrentCoordinate = null;
    var lastHoverFeatures = [];

    var handlerFunction = function(event){

      var eventType = this.parameters.type;
      var eventName = this.parameters.name;
      var delay = 0;

      const hoverPointerMoveEvent = eventType==='pointermove' && eventName.indexOf("hover")===0;

      // For pointermove events with a name begining with 'hover'
      // add a 150ms delay. This pervents the event being called excessively.
      // No delay if previous coord was over a feature.
      if (hoverPointerMoveEvent) {
        hoverCurrentCoordinate = event.coordinate;
        delay = lastHoverFeatures.length ? 0 : 150;
      }

      window.setTimeout(function() {
        // if delay is on, the mouse mustn't have moved during the duration of the timeout
        if (!delay || event.coordinate === hoverCurrentCoordinate) {

          if(eventType != 'pointerdrag' && event.dragging){
            return;
          } else if(eventType === 'pointerdrag' && event.dragging){
              // stop map moving on drag
              event.preventDefault();
          }

          var callback = this.parameters.handler;
          var layers = this.olLayers;
          var coordinate = event.coordinate;
          var resolution = event.frameState.viewState.resolution;
    
          if(layers){
            var featuresAtCoordinate = getOLFeatures(event.map, layers, coordinate, event.pixel, resolution, eventName.substring(0,16) === "memorial-capture");
            var features = featuresAtCoordinate[0];
            var layerNames = featuresAtCoordinate[1];

            if (hoverPointerMoveEvent)
              lastHoverFeatures = features;

            $rootScope.$apply(function(){
              callback(event, features, layerNames);
            });
          }
        }
      }.bind(this), delay);
    };

    return {
        restrict: "E",
        scope: {
            parameters: '=olexEventProperties'
        },
        replace: false,
        require: '^openlayers',
        link: function( scope, element, attrs ) {
          console.log('map');
          var map = window.OLMap;
          var layerNames = scope.parameters.layers;
          var eventType = scope.parameters.type;
          scope.olLayers = null;
          if(layerNames)
            scope.olLayers = olexHelper.getOlLayers(map, layerNames, true);
          var handler = angular.bind(scope, handlerFunction);
          map.on(scope.parameters.type, handler);
          scope.$on('$destroy', function() {
              map.un(scope.parameters.type, handler);
          });

          scope.$watchCollection('parameters.layers', function(newLayers, oldLayers){
              if(newLayers){
                scope.olLayers = olexHelper.getOlLayers(map, newLayers, true);
              }
          });
        }
    }
}]);
