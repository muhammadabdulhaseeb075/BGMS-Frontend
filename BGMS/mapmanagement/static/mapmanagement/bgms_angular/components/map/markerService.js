 /**
  * @module markerService
  *
  * @description
  * Map overlays are represented by an object of the type
  * {
  * 	group: 'if it belongs to a user action eg draw, layerswitch, personselect etc'
  * 	name: unique name for identification
  * 	positioning: ['bottom-left','top-left'], //array of 2 positionings
  * 	tooltip: { //optional arrow class, keys correspond to the 2 positionings
  *              "bottom-left":"ol-popup-bottom",
  *              "top-left": "ol-popup-top"
  *          },
  * 	offset: { //keys correspond to the 2 positionings
  *              "bottom-left":[-47, -21],
  *              "top-left":[-47, 21]
  *          },
  *          class: class(es) of the overlay as space seperated string
  *          message: html message to be displayed in overlay
  *              or
  *          template: {
  *              url: 'partial url'
  *              scope: 'varibles+functions to be added to scope of the template'
  *          }
  *      }
  */
/**
 * @module markerService
 *
 * @description
 * A model-service used to add or remove overlays to the map.
 */
angular.module('bgmsApp.map').service('markerService', [function(){
	/**
	 * @typedef {Object} Marker
	 * @property {string} name - unique name for identification
	 * @property {string} group - if it belongs to a user action eg draw, layerswitch, personselect etc
	 * @property {Array<string>=} positioning - array of two ol.OverlayPositioning strings, eg. ['bottom-left','top-left'].
	 * First one is default, second is implemented if the default generated the overlay offscreen
	 * @property {Object} tooltip - optional tooltip arrow classes to be implemented for each positioning,
	 * keys correspond to the positoning strings eg. { "bottom-left":[-47, -21], "top-left":[-47, 21] }
	 * @property {Object} offset - two ol.Overlay.offset Arrays to be implemented for each positioning,
	 * keys correspond to the positoning strings
	 * @property {string=} message - html message to be displayed in overlay
	 * @property {Object=} template - Object of type { url: 'partial url', scope: 'varibles+functions to be added to scope of the template'}
	 *
	*/

    var view_model = this;

    this.getMarkers = function(){
        return window.MapMarkers;
    };

    this.getMarkerPositionInStack = function(key, value){
        //optimise this
        var positions = [-1];
        var i = 0;
        angular.forEach(window.MapMarkers, function(marker, index) {
            if(marker[key] === value){
                positions[i++] = index; //TODO: position could be returned here
            }

        });
        return positions;
    };

    this.getMarkerByName = function(markerName){
        try{
            return window.MapMarkers[this.getMarkerPositionInStack('_name', markerName)[0]]
        }
        catch(e){
            return undefined;
        }
    };

    this.removeMarkerByName = function(markerName){
        window.setTimeout(() => {
            jQuery(document).trigger('removeMarkerByName', markerName);
        });
    };

    this.removeMarkerById = function(id){
        window.setTimeout(() => {
            jQuery(document).trigger('removeMarkerById', id);
        });
    };

    this.removeMarkersByGroup = function(markerGroup){
        jQuery(document).trigger('removeMarkersByGroup', markerGroup);
    };

    this.pushMarker = function(marker){
        jQuery(document).trigger('pushMarker', marker);
        return this.getMarkerByName(marker.name);
    };

    /**
	 * @function
	 * @description
	 * Returns offset for the toolbar based on feature pixel
	 * @param {array} pixel 
	 * @return {array} offset 
	 */
    this.getFloatingToolbarOffset = function(position){
        var defaulty = 50, defaultx = 100, toolbarheight = 50, floatingtoolbarheight = 50;
        var pixel = window.OLMap.getPixelFromCoordinate(position);
        var resolution = window.OLMap.getView().getResolution();

        var x,y = 0;
        if(pixel[0] - defaultx > 0){
            x = -defaultx;
        }else{
            x = 0;
        }

        //pixel[1] + defaulty + toolbarheight (default distance toolbar y)
        if (resolution === 0.007) defaulty += 50;
        if(pixel[1] + defaulty + toolbarheight + floatingtoolbarheight < $(window).height()){
            y = defaulty;
        }else{
            y = -defaulty * 2;
        }
        
        return [x,y];
    };

    /**
	 * @function
	 * @description
	 * Returns offset for the toolbar based on feature pixel center
	 * @param {ol.feature} feature 
	 */
    this.relocateFloatingToolbar = function(feature){
        var tmpft = this.getMarkerByName("floating-toolbar");
        if(feature !== undefined){
            var fe = feature.getGeometry().getExtent();
            var fcenter = ol.extent.getCenter(fe);
            // var newoffset = this.getFloatingToolbarOffset(feature.getGeometry().getFirstCoordinate());
            var newoffset = this.getFloatingToolbarOffset(fcenter);
            // tmpft.position = feature.getGeometry().getFirstCoordinate();
            tmpft.position = fcenter;
            tmpft.offset = {
                  "bottom-left": newoffset,
                  "top-left": newoffset
            };            
        }
    };

    /**
	 * @function
	 * @description
	 * Returns offset for the toolbar based on feature pixel
	 * @param {ol.feature} feature
	 */
    this.handleRelocationFloatingToolbar = function(feature){
        // view_model.mapevent = mapevent;
        var tmpft = view_model.getMarkerByName("floating-toolbar");
        if(tmpft !== undefined){
            view_model.relocateFloatingToolbar(feature);
        }
    };

    /**
	 * @function
	 * @description
	 * Binds mapevent to call handleRelocationFloatingToolbar
	 * @param {ol.feature} feature 
	 */
    this.handleDragFeatureFloatingToolbar = function(feature){
        view_model.handleRelocationFloatingToolbar(feature);
    };
}]);
