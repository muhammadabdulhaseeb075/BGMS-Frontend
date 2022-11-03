/**
 * Controller for Layer Selection
 * @param  {Angularjs Service} 
 */
angular.module('bgmsApp.map').controller('layerSelectionController', ['floatingMemorialToolbarService', 'layerSelectionService',
  function(floatingMemorialToolbarService, layerSelectionService) {

    var view_model = this;


    // view_model.isDropup = layerSelectionService.isDropup();
    view_model.isDropup = false;


    /**
      * Dictionary layer_groups:
      * Note: Only memorial group is being loaded for dropdown list when adding memorial
      */
    view_model.layer_groups = layerSelectionService.getLayerGroups();

    /**
     * List of groups layers to load
     * When empty will load all groups
     * @type  {array}
     */
    view_model.groups_to_load = ['memorials'];

    /**
     * Floating Option Handler event from layer selection
     * @param  {string} eventName
     * @param  {string} option
     */
    view_model.floatingOptionsHandler = function(eventName, option){
        floatingMemorialToolbarService.floatingOptionsHandler(eventName, option);
    };


    /** Get Request layer groups
     * @param  {} '/mapmanagement/getLayerGroups/'
     * @param  {view_model.groups_to_load}} {'groups_to_load[]'
     */
    // layerSelectionService.getRequestLayerGroups('/mapmanagement/getLayerGroups/',
    //                      {'groups_to_load[]':view_model.groups_to_load});
    
    
    /** Get Request layer groups
     * @param  {} '/mapmanagement/getLayerGroups/'
     * @param  {view_model.groups_to_load}} {'groups_to_load[]'
     */
    view_model.showDropup = function(id_elem){
      return layerSelectionService.isDropup();

    };

    /** Get Request layer groups
     * @param  {} '/mapmanagement/getLayerGroups/'
     */
    view_model.dropUp = function(id_elem){
      return layerSelectionService.showDropup($(id_elem));
    };

}]);
