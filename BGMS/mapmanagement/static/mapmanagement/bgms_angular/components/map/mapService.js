angular.module('bgmsApp.map').service('MapService', ['$timeout', '$rootScope', '$http', '$q', 'eventService', 'layerService', 'styleService', 'memorialService',
  function($timeout, $rootScope, $http, $q, eventService, layerService, styleService, memorialService){
	var view_model = this;

	view_model.extent = null;

  view_model.getDefaults = function(){
      return {
            view:{
              projection: 'EPSG:27700',
              // extent: extent.aerial.extent,
              // extent: [332506.574,  539788.483, 332596.591,  539911.442],
              extent: [],
              // resolutions: [2800.0, 1400.0, 700.0, 350.0, 280, 140, 70, 28.0, 14.0, 7.0, 2.8, 1.4,0.7, 0.28, 0.14, 0.07, 0.028]
              resolutions: [6.999999999999999, 2.8, 1.4, 0.7, 0.28, 0.14, 0.07, 0.028, 0.014, 0.007, 0.0028],
              minResolution: 0.0028,
              maxResolution: 6.999999999999999
            },
              "interactions": {
                    "mouseWheelZoom": true
              },
              controls: {
                  rotateOptions: ({ autoHide: false, }),
                  rotate: true,
              },
         };
  };

	this.getExtent = function(){
		return this.extent;
	};

	this.setExtent = function(extent){
		this.extent = extent;
	};

  /**
   * Change style north arrow (reset button)
   * It can be changed to use any font icon using fontIcon variable
   */
  view_model.changeResetButtonIcon = function(){
    var rbSpam = angular.element(document.querySelector('.ol-rotate-reset')).children();
    rbSpam.html('');
    rbSpam.addClass('glyphicon glyphicon-arrow-up');
  };
}]);
