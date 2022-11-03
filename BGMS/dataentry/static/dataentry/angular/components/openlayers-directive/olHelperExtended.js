angular.module('openlayers-directive').config(['$provide', function($provide){
    $provide.decorator('olHelpers', ['$delegate', '$log', function($delegate, $log){
    	/** Extending setDefaults to include supports for resolutions **/
    	var setDefaults = $delegate.setDefaults;
    	$delegate.setDefaults = function(scope){
    		var defaults = setDefaults(scope);
    	};

        /** Extending the createView function to include support for resolutions**/

        //saving old function before extending
        var createView = $delegate.createView;
        var createProjection = function(view) {
            var oProjection;
            switch (view.projection) {
                case 'pixel':
                    if (!angular.isDefined(view.extent)) {
                        $log.error('[AngularJS - Openlayers] - You must provide the extent of the image ' +
                                   'if using pixel projection');
                        return;
                    }
                    oProjection = new ol.proj.Projection({
                        code: 'pixel',
                        units: 'pixels',
                        extent: view.extent
                    });
                    break;
                default:
                    oProjection = new ol.proj.get(view.projection);
                    break;
            }
            return oProjection;
        };

        $delegate.createView = function(view) {
            console.log('overridden method createView');
             if(view.resolutions){
                 console.log('overridden method createView has resolutions');
                var projection = createProjection(view);
                console.log(view.extent);
                return new ol.View({
                  extent: view.extent,
                  projection: projection,
                  // resolution:0.5,
                  resolutions: view.resolutions,
                  // resolutions: [1600,800,400,200,100,50,25,10,5,2.5,1,0.5,0.25,0.125,0.0625, 0.03125, 0.015625]
                  // resolutions:  [6.999999999999999, 2.8, 1.4, 0.7, 0.28, 0.14, 0.07, 0.028, 0.014, 0.007],
                  minResolution: view.minResolution,
                  maxResolution: view.maxResolution,
                  // zoom: 12,
                  // maxZoom: 19,
                  // minZoom: 10,
                });
             }
             else{
                 return createView(view);
             }
        };


        /**Extending the detectLayerType Function to include support for Cluster Layer**/

        //saving old function before extending
        var detectLayerType = $delegate.detectLayerType;

        //wrap and override old function
        $delegate.detectLayerType = function(layer){
            // console.log('overridden method detectLayerType');
            if (layer.type) {
                return layer.type;
            } else {
                switch (layer.source.type) {
                    case 'Cluster':
                        return 'Vector';
                        break;
                    default:
                        return detectLayerType(layer);
                }
            }
        };

        /**Extending the createLayer Function to include support for Cluster Layer, and
        name, min and max resolution properties.**/

        //helper function to create source
        var createSource = function(source){
            var oSource;
            switch(source.type){
                case 'GeoJSON':
                	var geoJsonFormatter = new ol.format.GeoJSON();
                	if(source.projection){
                		geoJsonFormatter = new ol.format.GeoJSON({
                			defaultDataProjection: source.projection
                		});
                	}
                    if(source.url){
                        oSource = new ol.source.Vector({
                            url: source.url,
                            format: geoJsonFormatter
                        });
                    } else {
                    	var features = geoJsonFormatter.readFeatures(source.geojson.object);
                        oSource = new ol.source.Vector({
                        	features: features
                        });
                    }
                    break;
                case 'Cluster':
                    var geojsonSource = angular.copy(source);
                    geojsonSource.type = 'GeoJSON';
                    oSource = new ol.source.Cluster({
                        distance: source.distance,
                        source: createSource(geojsonSource)
                    });
                    break;
                case 'EmptyVector':
                    oSource = new ol.source.Vector({
                      source: new ol.source.Vector()
                    });
                    break;
                case 'TileWMTS':
                	oSource = new ol.source.WMTS({
                        format: 'image/png',
                        requestEncoding: 'REST',
                        crossOrigin: 'anonymous',
                        url: source.url,
                        layer: source.layer,
                        matrixSet: source.matrixSet,
                        tileGrid: new ol.tilegrid.WMTS({
                          tileSize: [256, 256],
                          extent: source.extent,
                          resolutions: source.tileGrid.resolutions,
                          matrixIds: source.tileGrid.matrixIds
                        }),
                        style:source.style
                	});
                	break;
                case 'ImageStatic':
                    if (!source.url) {
                        $log.error('[AngularJS - Openlayers] - You need a image URL to create a ImageStatic layer.');
                        return;
                    }
                    var imageExtent;
                    if(source.extent)
                    	imageExtent = source.extent;
                    else
                    	imageExtent = ol.proj.get('pixel').getExtent()
                    oSource = new ol.source.ImageStatic({
                        url: source.url,
//                        attributions: createAttribution(source),
//                        projection: source.projection,
                        imageExtent: imageExtent,
                        imageLoadFunction: source.imageLoadFunction
                    });
                    break;
                default:
                    oSource = null;
            }
            return oSource;
        };

        //saving old function before extending
        var createLayer = $delegate.createLayer;

        //wrap and override old function
        $delegate.createLayer = function(layer, projection) {
            // console.log('overridden method createLayer');
            var oLayer;
            var type = detectLayerType(layer);
            switch (layer.source.type) {
                case 'GeoJSON':
                    if(!(layer.source.url || layer.source.geojson) ){
                        $log.error('[AngularJS - Openlayers - Extended] GeoJSON source needs either source url or geojson object');
                        return;
                    }
                    if(layer.type && layer.type === 'VectorImage' ){
                        //Wrap to use imageVector and change layer style with icons
                        oLayer = new ol.layer.Vector({
												  renderMode: 'image',
												  style: layer.style,
												  source: createSource(layer.source)
												});

                        if (layer.style) {
                                style = layer.style;

                                // not every layer has a setStyle method
                                if (oLayer.setStyle && angular.isFunction(oLayer.setStyle)) {
                                    oLayer.setStyle(style);
                                }else{
                                    // $log.error('[AngularJS - Openlayers - Extended] No Style for layer');
                                }
                        }
                    }else{
                        //Layer.type === Vector : Default if not defined
                        oLayer = new ol.layer.Vector({
                            source: createSource(layer.source)
                        });
                    }
                    break;
                case 'Cluster':
                    if(!(layer.source.distance && (layer.source.text || layer.source.url || layer.source.geojson)) ){
                        $log.error('[AngularJS - Openlayers - Extended] Cluster source needs both distance and text or url or geojson');
                        return;
                    }
                    oLayer = new ol.layer.Vector({
                        source: createSource(layer.source)
                    });
                    break;
                case 'EmptyVector':
                    console.log("created empty vector source");

                    oLayer = new ol.layer.Vector({
                        source: createSource(layer.source)
                    });
                    break;
                case 'TileWMTS':
                    console.log("created TileWMTS source");
                    oLayer = new ol.layer.Tile({
                        source: createSource(layer.source),
                        extent: layer.source.extent,
                        preload: 1
                    });
                    break;
                case 'ImageStatic':
                    oLayer = new ol.layer.Image({
                    	source: createSource(layer.source)
                    });
                    break;
                default:
                    oLayer = createLayer(layer, projection);
                    break;
            }
            if(layer.name)
                oLayer.set('name', layer.name);
            if(layer.groupName)
                oLayer.set('groupName', layer.groupName);
            if(layer.zIndex)
                oLayer.setZIndex(layer.zIndex);
            if(layer.maxResolution)
                oLayer.setMaxResolution(layer.maxResolution);
            if(layer.minResolution)
                oLayer.setMinResolution(layer.minResolution);
            if(!angular.isUndefined(layer.opacity))
            	oLayer.setOpacity(layer.opacity);
            if(layer.defer){
            	oLayer.once('postcompose', function(){
                	layer.defer.resolve(true);
            	})
            }
            return oLayer;
        };
        //return the modified delegate
        return $delegate;
    }]);
}]);





angular.module('openlayers-directive').config(['$provide', function($provide){
    $provide.decorator('olMapDefaults', ['$delegate', '$log', function($delegate, $log){
    	/** Extending setDefaults to include supports for resolutions **/
    	var setDefaults = $delegate.setDefaults;

    	$delegate.setDefaults = function(scope){
    		var defaults = setDefaults(scope);
    		if(scope.defaults && scope.defaults.view)
    			defaults.view.resolutions = scope.defaults.view.resolutions;
    		if(scope.defaults && scope.defaults.center)
        		defaults.center = scope.defaults.center;
    		return defaults;
    	};

        //return the modified delegate
        return $delegate;
    }]);
}]);
