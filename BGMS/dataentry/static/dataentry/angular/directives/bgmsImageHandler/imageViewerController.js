/**
 * Image Viewer Controller
 * @constructor
 * @ngInject
 */
angular.module('bgmsApp.dataentry').controller('imageViewerController', ['$scope', '$timeout', 'imageViewerService', 'openlayersService', 'featureHelperService', 'olData',
  function($scope, $timeout, imageViewerService, openlayersService, featureHelperService, olData) {
    // using view_model instead of this to avoid ambiguity inside functions
    var view_model = this;
    
    //setting imageSize on scope
    $scope.imageParameters = imageViewerService.imageParameters;

    view_model.centre = openlayersService.centre;
    
    //setting the initial visible extent 
    view_model.visibleExtent = null;

    
  //initialise layers, events and extent
	view_model.layers = openlayersService.layers;
	view_model.events = openlayersService.events;
	view_model.interactions = openlayersService.interactions;
	view_model.extent = openlayersService.extent;

	/**
	 * @function
	 * @description
	 * Function called from outside angular to resize map when 
	 * the map's target div has changed size.
	 */
    view_model.updateMapSize = function() {
    	olData.getMap().then(function(map) {
        	map.updateSize();
    	});
    };
	
	$scope.$watch('image', function(newImage){
		if(newImage && newImage.extent){
			openlayersService.updateDefaultProjection(newImage.extent, $scope.width);    
		    view_model.defaults = openlayersService.defaults;
			openlayersService.removeLayer('image');
			openlayersService.addLayer(imageViewerService.createImageLayer(newImage.url, newImage.extent));
			if(!view_model.visibleExtent){
				view_model.visibleExtent = newImage.extent;
				openlayersService.getMapSize().then(function(mapSize){
					view_model.visibleExtent = [0,newImage.extent[3]-mapSize[1]*openlayersService.minRes,newImage.extent[2],newImage.extent[3]];
				});
			} else{
				//clearing the image extent and resetting it in next digest cycle to 
				//ensure new image is not bound by old image extents
				view_model.visibleExtent = null;
				$timeout(function(){
					view_model.visibleExtent = newImage.extent;
					openlayersService.getMapSize().then(function(mapSize){
						view_model.visibleExtent = [0,newImage.extent[3]-mapSize[1]*openlayersService.minRes,newImage.extent[2],newImage.extent[3]];
					});
				});
			}
		}
	});

	
	//adding tag layer
	$scope.$watch('imageIdForTags', function(newImageId){
		if(newImageId){
			var style = function(){
				return openlayersService.polygonStyleFunction('rgba(58, 125, 54, 1)','rgba(58, 125, 54, 0)',  4);
			};
			openlayersService.addLayer({
				name:'tags',
				source:{
		            type: 'GeoJSON',
		            url: '/dataentry/getTags/?image_id='+newImageId,
		            projection: ol.proj.get('pixel')
		        },
		        style: style,
				zIndex: 1
			});
		} else{
			openlayersService.removeLayer('tags');
		}
	});
	
	//adding new tag to tag layer
	$scope.$watch('addTag', function(newTag){
		if(newTag){
			var feature = new ol.Feature(ol.geom.Polygon.fromExtent(newTag.extent));
			feature.setId(newTag.id);
			featureHelperService.addFeatureToLayer(feature, 'tags');
		}
	});	

	
	//adding removing deleted tag from tag layer
	$scope.$watch('removeTag', function(tagId){
		if(tagId){
			featureHelperService.removeFeatureFromLayer(tagId, 'tags');
		}
	});	
  }
]);
