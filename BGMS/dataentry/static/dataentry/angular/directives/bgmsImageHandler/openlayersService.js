angular.module('bgmsApp.dataentry').service('openlayersService', ['olData', '$timeout', '$q', '$rootScope', function(olData, $timeout, $q,$rootScope){
	
	var view_model = this;
	
	view_model.maxRes = 1;
	
	//define pixel projection
    ol.proj.addProjection(new ol.proj.Projection({
        code: 'pixel',
        units: 'pixels',
        extent: [ 0, 0, 0, 0 ]
    }));
    ol.proj.addEquivalentProjections([ol.proj.get('pixel'),ol.proj.get('EPSG:3857')]);
    ol.proj.addEquivalentProjections([ol.proj.get('pixel'),ol.proj.get('EPSG:4326')]);
	
	//define map defaults and centre
	view_model.defaults = {
        view: {
    		extent: [],
    		projection: ol.proj.get('pixel'),
        },
        interactions: {
	        "mouseWheelZoom": true
	    }
    };
    
	//initialise layers, events and extent
	view_model.layers = [];
	view_model.events = [];
	view_model.interactions = [];
	
	//helper functions
	/**
	 * @function
	 * @description 
	 * helper function get the position of an object in an array using 'name' as the key
	 */
	view_model._getPosition = function(name, array){
        for(var index in array){
        	if(array[index].name === name)
        		return index;
        }
        return -1;
	};

	/**
	 * @function
	 * @description 
	 * helper function to add or replace an element in the array using
	 */
	view_model._addElement = function(element, array){
		var position = view_model._getPosition(element.name, array);
        if(position!=-1){
        	array[position] = element;
        } else{
        	array.push(element);
        }
	};
    
	//manage defaults
	/**
	 * @function
	 * @description 
	 * Update default projection in the projection, set view extent
	 * and resolutions.
	 * @param interaction{String} - interaction name
	 */
	view_model.updateDefaultProjection = function(extent, mapSize){
		var newExtent = $q.defer();
		ol.proj.get('pixel').setExtent(extent);
		view_model.defaults.view.projection = ol.proj.get('pixel');
		var mapWidth = mapSize[0];
		var mapHeight = mapSize[1];
		var resWidth = extent[2]/mapWidth;
		var resHeight = extent[3]/mapHeight;
		view_model.maxRes = Math.max(resWidth, resHeight);
		view_model.minRes = Math.min(resWidth, resHeight);
		view_model.defaults.view.resolutions = [view_model.maxRes, view_model.maxRes/2, view_model.maxRes/4, view_model.maxRes/8, view_model.maxRes/16, view_model.maxRes/32];
		view_model.defaults.center = {
			coords: ol.extent.getCenter(extent[0],extent[3]-mapSize[1]*view_model.minRes,extent[2],extent[3]),
	        projection: 'pixel'
		};
		view_model.defaults.view.resolution = view_model.minRes;
		view_model.defaults.view.extent = extent;
	};
	
	//manage layers
	/**
	 * @function
	 * @description 
	 * Adds layer to map
	 * @param layer{Object} - layer
	 */
	view_model.addLayer = function(layer){
		view_model._addElement(layer, view_model.layers);
	};

	/**
	 * @function
	 * @description 
	 * Remove a layer from the layers on the map 
	 * @param {String}layer - name of the layer to remove
	 */
	view_model.removeLayer = function(layer){
		var position = view_model._getPosition(layer, view_model.layers);
		if(position!=-1){
			return view_model.layers.splice(position, 1);
		}		
	};
	
	//manage events
	/**
	 * @function
	 * @description 
	 * Add event to map
	 * @param event{Object} - event
	 */
	view_model.addEvent = function(event){
		view_model._addElement(event, view_model.events);		
	};
	
	//manage interactions
	/**
	 * @function
	 * @description 
	 * Adds interaction to map
	 * @param interaction{Object} - interaction
	 */
	view_model.addInteraction = function(interaction){
		view_model._addElement(interaction, view_model.interactions);		
	};

	/**
	 * @function
	 * @description 
	 * Removes interaction from map
	 * @param interaction{String} - interaction name
	 */
	view_model.removeInteraction = function(interaction){
		var position = view_model._getPosition(interaction, view_model.interactions);
		if(position!=-1){
			return view_model.interactions.splice(position, 1);
		}		
	};

	/**
	 * @function
	 * @description 
	 * Get style of the tag.
	 * returns [ol.style.Style]
	 */
	view_model.polygonStyleFunction = function(lineColor, fillColor, lineWidth){
		if(!lineWidth)
			lineWidth = 1;
		var style = new ol.style.Style({
			fill: new ol.style.Fill({
		      color: fillColor
		    }),
		    stroke: new ol.style.Stroke({
		      color: lineColor,
		      width: lineWidth
		    }),
		    image: new ol.style.Circle({
			      radius: 5,
			      fill: new ol.style.Fill({
			        color: fillColor
			      }),
		    	stroke: new ol.style.Stroke({
			      color: lineColor,
			    }),
		    })
		});
		return [style];
	};

	/**
	 * @function
	 * @description 
	 * Get size of map
	 * returns [mapWidth, mapHeight]
	 */
	view_model.getMapSize = function(){
		var mapSize = $q.defer();
		olData.getMap().then(function(map){
			mapSize.resolve(map.getSize());
		});
		return mapSize.promise;
	};

	
}]);