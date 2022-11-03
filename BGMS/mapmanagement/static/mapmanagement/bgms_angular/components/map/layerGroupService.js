angular.module('bgmsApp.map').service('layerGroupService', ['$log', '$rootScope', 'layerService', function($log, $rootScope, layerService){

    var view_model = this;

    /*
    Gets the layers from Vuex (eventually we won't need this)
    */
   view_model.layerGroups = function(){
    // do not continue until window.MapLayers has a value (it will always have a value)
    if (!window.MapLayers) {
      let interval = setInterval(function() {
        if (window.MapLayers) {
          clearInterval(interval);
          return window.MapLayers.layerGroups;
        }
      }, 50);
    }
    else
      return window.MapLayers.layerGroups;
  };

    view_model.getLayerGroupByName = function(groupName){
      /*
      Gets layer from layer store
      */

    	for (var layerkey in view_model.layerGroups()) {
    		if (layerkey === groupName)
			  return view_model.layerGroups()[layerkey];
    	}
    	$log.error('layer group '+groupName+' could not be found');
    };

}]);
