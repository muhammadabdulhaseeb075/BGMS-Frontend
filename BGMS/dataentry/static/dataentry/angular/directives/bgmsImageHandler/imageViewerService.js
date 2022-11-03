angular.module('bgmsApp.dataentry').service('imageViewerService', ['$rootScope', 'openlayersService', function($rootScope, openlayersService){
	
	var view_model = this;
	
	view_model.staticlayer = null;

	/**
	 * @function
	 * @description 
	 * Function to create the image layer object
	 */
	view_model.createImageLayer = function(imageSource, imageExtent){
		view_model.staticlayer = {
          	name:'image',
              source: {
                  type: "ImageStatic",
                  projection: ol.proj.get('pixel'),
                  imageSize: [imageExtent[2], imageExtent[3]],
                  extent: imageExtent,
                  url: imageSource
              }, 
              zIndex: 0
        };
		return view_model.staticlayer;
	};
    
}]);