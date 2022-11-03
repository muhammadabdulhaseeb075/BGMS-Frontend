/**
 * @module layerSelectionService
 *
 * @description
 * This model contains all possible layers by groups.
 *
 */
angular.module('bgmsApp.map').service('layerSelectionService', ['$q', function ($q) {

    var view_model = this;

    /**
     * Dictionary which loads layer by groups in the following format:
     * {'memorials': [
     * {"feature_codes__display_name": "Plaque", "feature_codes__feature_type": "plaque"},
     * {"feature_codes__display_name": "War Grave", "feature_codes__feature_type": "war_grave"},
     * ]};
     * @type {Dictionary}
     *
     * Note: Only memorial group is being loaded for dropdown list when adding memorial
     */
    // view_model.layer_groups = {'memorials': [
    //   {"feature_codes__display_name": "Plaque1", "feature_codes__feature_type": "plaque"},
    //   {"feature_codes__display_name": "War Grave", "feature_codes__feature_type": "war_grave"},
    //   ]};
    view_model.layer_groups = {};

    view_model.groups_to_load = ['memorials'];
    view_model.defaultCheckedDropdown = {
        layer: "gravestone",
    };
    view_model.feature = '';

    /**
   * Return layer type without "memorials_" (case lych gate and bush)
   * @param {String} lyr  layer type to clean
   * @return {String} Layer type clean
   */
    view_model.cleanLayerType = function(lyr){
        var lyrspl = lyr.split('memorials_');
        if(lyrspl.length > 1)
            return lyrspl[1];
        else
            return lyr;
    };


    /**
   * Return layer_groups
   * @return {[Dictionary]}
   */
    view_model.getLayerGroups = function (graveplotUuid) {
        // var promise = view_model.getRequestLayerGroups('/mapmanagement/getLayerGroups/',
                        //  {'groups_to_load[]':view_model.groups_to_load});
        // promise.then(function(values){
        //     view_model.layer_groups = values;
        // });
        // return promise;
        return view_model.layer_groups;
    };

    /**
   * Set true to the layer passed as parameter
   * @param {Dictionary} lg  layer groups
   */
    view_model.checkLayer = function (lyr) {
        lyr = view_model.cleanLayerType(lyr);
        for(var i=0; i<view_model.layer_groups.memorials.length; i++){
            if(view_model.layer_groups.memorials[i].feature_codes__feature_type == lyr){
                view_model.layer_groups.memorials[i].checked = 'checked';
            }else{
                view_model.layer_groups.memorials[i].checked = '';
            }
        }
    };

   /**
   * Set layer_groups and sets the default checked value
   * @param {Dictionary} lg  layer groups
   */
    view_model.setLayerGroups = function (lg) {
        view_model.layer_groups = lg;
        view_model.checkLayer(view_model.defaultCheckedDropdown.layer);
    };


    /**
   * Get request layer groups
   * @param  {[String]} url [description]
   * @return {[type]}     [description]
   */
    view_model.getRequestLayerGroups = function (url, groupsArray) {
        // var layer_groups = $q.defer();
        groupsArray = {'groups_to_load[]':view_model.groups_to_load};
        $.get(url,groupsArray)
            .done(function (data, status, headers, config) {
                data.memorials = JSON.parse(data.memorials)
                console.log(data);
                view_model.setLayerGroups(data);
                // view_model.layer_groups.resolve(data);
                // layer_groups.resolve(data);
            })
            .fail(function (data, status, headers, config) {
                console.log('could not load data from ' + url);
            });
        // return layer_groups.promise;
    };

    /**
   * Set setFeature of feature just placed or selected
   * @param {ol.feature} fc feature
   */
    view_model.setFeature = function (feature) {
        view_model.feature = feature;
    };



    /** Return whether the selection layer dropdown list shuld be shown up or down
     * @param  {string} id element
     * @return {boolean}
     */
    view_model.showDropup = function(id_elem){
        if (view_model.feature !== ''){
            var coordinate = view_model.feature.getGeometry().getFirstCoordinate();
            var pixel = (window as any).OLMap.getPixelFromCoordinate(coordinate);
            //id_elem.parent().height(): height toolbar, 50: space between toolbar and feature, 50: toolbar height
            var bottonPixel = pixel[1] + $(id_elem).height() + $(id_elem).parent().height() + 50 + 50;
            if($(window).height() < bottonPixel){
                $(id_elem).parent().addClass("dropup");
            }else{
                $(id_elem).parent().removeClass("dropup");
            }
        }
        // return false;
    };


    view_model.isDropup = function(){

        var deferred = $q.defer();

        if (view_model.feature !== ''){
            var coordinate = view_model.feature.getGeometry().getFirstCoordinate();
            var pixel = (window as any).OLMap.getPixelFromCoordinate(coordinate);

            deferred.resolve(true);
        }else{
            deferred.resolve(false);
        }

        return deferred.promise;

    };

}]);


angular.module('bgmsApp.map').directive('insideDropdown', ['layerSelectionService', function(layerSelectionService) {

  function showDropup(scope, element, attrs, controller) {
    if(scope.$last){
      var elemq = $('#id_lyrs_floating_toolbar');
      console.log(elemq.height());
      // layerSelectionService.isDropup();
      // console.log(layerSelectionService.isDropup());
      layerSelectionService.showDropup(element.parent());
    }
  }

  return {
    restrict: 'EA',
    link: showDropup
  };
}]);
