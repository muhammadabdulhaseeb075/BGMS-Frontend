/**
 * Map Controller
 * @constructor
 * @ngInject
 */
angular.module('bgmsApp.map').controller('MapCtrl', ['$scope', '$element', 'MapService', 'layerService', 'interactionService', 'markerService',
	'featureOverlayService', 'personService', 'eventService', 'memorialService', 'layerGenerator', 'securityService', 'reservedPersonService', 'layerSelectionService',
  function($scope, $element, MapService, layerService, interactionService, markerService, featureOverlayService, personService,
		eventService, memorialService, layerGenerator, securityService, reservedPersonService, layerSelectionService) {
    // using view_model instead of this to avoid ambiguity inside functions
    var view_model = this;

    //initialize the models
    /**
    * @type {object}
    * @export
    */
    // do not continue until window.MapLayers has a value (it will always have a value)
    if (!window.MapLayers) {
      var interval = setInterval(function() {
        if (window.MapLayers) {
          view_model.layers = window.MapLayers.layers;
          clearInterval(interval);
        }
      }, 50);
    }
    else
      view_model.layers = window.MapLayers.layers;
    /**
     * @type {object}
     * @export
     */
    view_model.interactions = interactionService.getInteractions();
    /**
     * @type {object}
     * @export
     */
    view_model.events = eventService.getEvents();
    /**
     * @type {object}
     * @export
     */
    view_model.markers = markerService.getMarkers();
    /**
     * @type {object}
     * @export
     */
    view_model.featureOverlays = featureOverlayService.getFeatureOverlayStore();

    //load reserved persons
    reservedPersonService.loadReservedPersonsFromGeoJson();

    //load layer groups
    layerSelectionService.getRequestLayerGroups('/mapmanagement/getLayerGroups/',
                         {'groups_to_load[]':layerSelectionService.groups_to_load});
    //debugger;
    //Set size of the map according to the size of the screen
    window.OLMap.setSize([window.innerWidth, window.innerHeight - $('header').height() - 2]);

    //Disable rotation touch screen function and alt + shift + drag rotation in the map
    // var interactions = map.getInteractions().getArray();
    // var pinchRotateInteraction = interactions.filter(function(interaction) {
    //   return interaction instanceof ol.interaction.PinchRotate;
    // })[0];
    // pinchRotateInteraction.setActive(false);
    // var altShiftDragRotate = interactions.filter(function(interaction) {
    //   return interaction instanceof ol.interaction.DragRotate;
    // })[0];
    // altShiftDragRotate.setActive(false);

    // change style control reset ratation
    MapService.changeResetButtonIcon();

    window.OLMap.updateSize();

    view_model.stopPan = function(allowedExtent, mapevent){
      var currentExtent = mapevent.frameState.extent;
      if(!ol.extent.containsExtent(allowedExtent, currentExtent)){
//    		  var pan = new ol.animation.pan({source:mapevent.map.getView().getCenter()});
//    		  mapevent.map.beforeRender(pan);
        var newExtent = ol.extent.getIntersection(allowedExtent, currentExtent);
        if(!ol.extent.intersects(allowedExtent, currentExtent))
          newExtent = allowedExtent;
        mapevent.map.getView().fit(newExtent);
      }
    };

    securityService.get_group_required_value(['SiteAdmin', 'SiteWarden']).then(function(group_required_value) {
        view_model.group_required_value = group_required_value;

        if (!group_required_value) {
          securityService.group_required_value = null;
          securityService.get_group_required_value(['MemorialPhotographer']).then(function(group_required_value) {
            view_model.memorial_photography_group = group_required_value;
          });
        }
    });
  }
]);
