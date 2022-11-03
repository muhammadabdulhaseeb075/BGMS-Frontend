angular.module('bgmsApp.map').service('layerService', ['$timeout', '$http', '$q', '$log', '$rootScope', function($timeout, $http, $q, $log, $rootScope){

    var view_model = this;

    /*
    Gets the layers from Vuex (eventually we won't need this)
    */
    view_model.layers = function(){
      // do not continue until window.MapLayers has a value (it will always have a value)
      if (!window.MapLayers) {
        let interval = setInterval(function() {
          if (window.MapLayers) {
            clearInterval(interval);
            return window.MapLayers.layers;
          }
        }, 50);
      }
      else
        return window.MapLayers.layers;
    };

    /*Functions relating to layer store*/

    view_model.getLayerByName = function(layerName){
      /*
      Gets layer from layer store
      */

      for (var layerkey in view_model.layers()) {
        if (layerkey === layerName)
        return view_model.layers()[layerkey];
      }
      //$log.error('layer '+layerName+' could not be found');
    };

    view_model.getLayersByGroup = function(groupName){
        /*
        Gets all layers in group from the layer store
        */
      var group = {};
        angular.forEach(view_model.layers(), function(layer, layerName){
            if(layer.groupName === groupName)
                group[layer.name] = layer;
        });
        return group;
    };

    view_model.setLayerGroupOpacity = function(groupName, visibility){
        var group = view_model.getLayersByGroup(groupName);
        //set visibility of each layer in group
        angular.forEach(group, function(layer){
          layer.visibility = visibility;
        });

    };

    /**
     * Removes the last numLevels from the tile grid
     * @param  {Object} tileGrid  should have resolutions and matrixIds arrays with the same lenght
     * @param  {Integer} numLevels to be removed
     * @return {Object}           new tileGrid
     */
    view_model.removeDetailLevels = function(tileGrid, numLevels){
      var original = _.cloneDeep(tileGrid);
      try{
        tileGrid.resolutions.splice(numLevels*-1,numLevels);
        tileGrid.matrixIds.splice(numLevels*-1,numLevels);
        return tileGrid;
      }catch(e){
        console.error("removeDetailLevels error");
        return original;
      }
    };
}]);
