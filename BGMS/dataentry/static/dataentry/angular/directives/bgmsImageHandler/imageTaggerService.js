angular.module('bgmsApp.dataentry').service('imageTaggerService', ['openlayersService', function(openlayersService){
	
	var view_model = this;

    view_model.name = 'draw';
    view_model.modifyName = 'modify-draw';

	/**
	 * @function
	 * @description 
	 * Function to remove interactions from the map 
	 */
	view_model.clear = function(){
		openlayersService.removeInteraction(view_model.name);
		openlayersService.removeInteraction(view_model.modifyName);
	};

	/**
	 * @function
	 * @description 
	 * Function to get draw interaction style 
	 */
	view_model.drawInteractionStyle = function(){
		return openlayersService.polygonStyleFunction('#614126','rgba(58, 125, 54, 0)',  4);
	};

	/**
	 * @function
	 * @description 
	 * Function to get draw layer style 
	 */
	view_model.drawLayerStyle = function(){
		return openlayersService.polygonStyleFunction('rgb(242, 160, 36)','rgba(58, 125, 54, 0)',  4);
	};
	
}]);