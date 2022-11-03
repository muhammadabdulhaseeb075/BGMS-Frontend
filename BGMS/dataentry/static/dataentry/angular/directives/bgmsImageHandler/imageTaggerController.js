/**
 * Image Viewer Controller
 * @constructor
 * @ngInject
 */
angular.module('bgmsApp.dataentry').controller('imageTaggerController', ['$scope', 'imageTaggerService', 'openlayersService', 'featureHelperService',
  function($scope, imageTaggerService, openlayersService, featureHelperService) {
    // using view_model instead of this to avoid ambiguity inside functions
    var view_model = this;

    view_model.layers = openlayersService.layers;
    view_model.name = imageTaggerService.name;
    view_model.modifyName = imageTaggerService.modifyName;


    view_model.toggle = {
      //Tagging tools
      draw_tag: false,
      modify_tag: false,
      delete_tag: false,
    };

    view_model.toggle_option = function(current_selection){
//    	view_model.stopActions();
		//deselect other options
		for(var key in view_model.toggle){
			if(key!=current_selection)
				view_model.toggle[key] = false;
		}
    };

    //add draw layer
	openlayersService.addLayer({
		name:'draw',
		source:{
			type:'EmptyVector'
		},
		style: imageTaggerService.drawLayerStyle,
		zIndex: 2
	});

	/**
	 * @function
	 * @description
	 * Function called from partial when user clicks the buttons
	 */
	view_model.selectInteraction = function(eventType, $event) {
  	  imageTaggerService.clear();
      switch (eventType) {
        case 'draw_tag':
        	view_model.toggle_option('draw_tag');
        	view_model.addDrawTagInterction();
          break;
        case 'modify_tag':
        	view_model.toggle_option('modify_tag');
        	view_model.addModifyTagInterction();
          break;
        case 'delete_tag':
        	view_model.toggle_option('delete_tag');
        	view_model.addDeleteTagInterction();
          break;
        default:
          return;
      }
    };

	/**
	 * @function
	 * @description
	 * Function to add draw interaction to the map so that user can draw new tag
	 */
    view_model.addDrawTagInterction = function(){
    	openlayersService.addInteraction({
        	name: view_model.name,
            type: 'draw',
            parameters: {
              type: 'LineString',
              layer: 'draw',
              style: imageTaggerService.drawInteractionStyle,
              maxPoints: 2,
              geometryFunction: function(coordinates, geometry) {
                  if (!geometry) {
                      geometry = new ol.geom.Polygon(null);
                    }
                    var start = coordinates[0];
                    var end = coordinates[1];
                    geometry.setCoordinates([
                      [start, [start[0], end[1]], end, [end[0], start[1]], start]
                    ]);
                    return geometry;
                }
            },
            handlers: {
              drawend: function(evt){
            	  imageTaggerService.clear();
            	  $scope.imageTag.extent = evt.feature.getGeometry().getExtent();
            	  view_model.toggle['draw_tag'] = false;
            	  $scope.$apply();
              }
            }
          });
        };


    	/**
    	 * @function
    	 * @description
    	 * Function to add modify interaction to the map so that user can edit tag
    	 */
        view_model.addModifyTagInterction = function(){
          openlayersService.addInteraction({
            name: view_model.name,
            type: 'select',
            parameters: {
              condition: ol.events.condition.click,
              layer: view_model.name,
              style: imageTaggerService.drawInteractionStyle,
            },
            handlers: {
              handleUnselect: function(event){
            	  $scope.imageTag.extent = event.element.getGeometry().getExtent();
            	  imageTaggerService.clear();
            	  view_model.toggle['modify_tag'] = false;
            	  $scope.$apply();
              }
            }
          });
          openlayersService.addInteraction({
            name: view_model.modifyName,
            type: 'modify',
            parameters: {
              selectFeatures: 'select',
              style: imageTaggerService.drawInteractionStyle
            },
            handlers: {
            	modifyend: function(evt){
              	  $scope.imageTag.extent = evt.features.getArray()[0].getGeometry().getExtent();
            	  $scope.$apply();
                }
            },
          });
        };

    	/**
    	 * @function
    	 * @description
    	 * Function to add delete interaction to map to enable user to delete tag
    	 */
        view_model.addDeleteTagInterction = function(){
        	openlayersService.addInteraction({
        	  name: view_model.name,
              type: 'select',
              parameters: {
                condition: ol.events.condition.click,
                layer: view_model.name
              },
              handlers: {
                handleSelect: function(feature){
	              $scope.imageTag.extent = undefined;
            	  imageTaggerService.clear();
            	  view_model.toggle['delete_drawing'] = false;
            	  $scope.$apply();
                }
              }
            });
          };


          $scope.$watchCollection('imageTag', function(newImageTag){
        	  if(!newImageTag.extent){
        		  featureHelperService.removeAllFeaturesFromLayer(view_model.name);
            	  imageTaggerService.clear();
            	  view_model.toggle_option();
        	  }	else if(newImageTag.id && newImageTag.extent){
    				featureHelperService.removeFeatureFromLayer(newImageTag.id, 'tags').then(function(feature){
    					featureHelperService.addFeatureToLayer(feature, 'draw');
    				});
        	  }
          });

  }
]);
