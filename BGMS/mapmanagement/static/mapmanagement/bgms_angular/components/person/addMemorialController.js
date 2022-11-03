angular.module('bgmsApp.map').controller('addMemorialController', ['$scope', '$element', '$http', '$modal', '$sce', '$timeout',
  'memorialService', 'interactionService', 'eventService', 'markerService', 'addMemorialService',
  'toolbarService', 'notificationHelper', 'geometryHelperService', 'featureHelperService', 'floatingMemorialToolbarService',
  'featureOverlayService',
  function($scope, $element, $http, $modal, $sce, $timeout, memorialService, interactionService, eventService,
    markerService, addMemorialService, toolbarService, notificationHelper, geometryHelperService,
    featureHelperService, floatingMemorialToolbarService, featureOverlayService) {
    /*

  It adds/removes the following overlays:
    add-grave-message overlay


  It adds/removes the following layers:
    add-grave-layer


  It adds/removes the following interactions:
    add_grave : select (onselect and onunselect), modify, draw (onDrawEnd)

    It adds/removes the following events
        pointermove
  */

    const sidebarEnum = Object.freeze({"memorialCapture":"memorialCaptureSidebarContainer", "graveLink":"graveLinkSidebarContainer"});

    var view_model = this;

    view_model.toggle = toolbarService.get_toggle();

    view_model.showMemorialCaptureSidebar = false;
    view_model.showGraveLinkSidebar = false;

    /*
     * @param {String} name of event
     * @return {undefined}
     */
    view_model.memorialToolbarHandler = function(eventType, $event) {

      switch (eventType) {
        case 'create_memorial':
          toolbarService.toggle_option('create_memorial').then(function(is_selected){
            if(is_selected){
                view_model.createMemorialInteraction();
            } else {
              addMemorialService.stopBurialTools();
            }
          });
        break;
        case 'edit_memorial':
            toolbarService.toggle_option('edit_memorial').then(function(is_selected){
              if(is_selected){
                view_model.editMemorialInteraction();
              } else {
                addMemorialService.stopBurialTools();
                }
            });
          break;
        case 'memorial_capture':
          toolbarService.toggle_option('memorial_capture').then(function(is_selected) {
            if (is_selected) {
              view_model.memorialCaptureInteraction();
            } else {
              addMemorialService.stopBurialTools();
            }
          });
          break;
          case 'grave_link':
            toolbarService.toggle_option('grave_link').then(function(is_selected) {
              if (is_selected) {
                view_model.graveLinkInteraction();
              } else {
                addMemorialService.stopBurialTools();
              }
            });
            break;
        default:
          return;
      }
    };

    view_model._generateUUID = function() {
      var d = new Date().getTime();
      if(performance && typeof performance.now === "function"){
          d += performance.now(); // use high-precision timer if available
      }
      var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
          var r = (d + Math.random()*16)%16 | 0;
          d = Math.floor(d/16);
          return (c=='x' ? r : (r&0x3|0x8)).toString(16);
      });
      return uuid;
    };

    view_model.createMemorialInteraction = function() {
      //create a plot and add it to the layer
      var geometry = geometryHelperService.createPolygonGeometry(floatingMemorialToolbarService.memorial_dictionary.gravestone.small.type, [0, 0], floatingMemorialToolbarService.memorial_dictionary.gravestone.small.dim1, floatingMemorialToolbarService.memorial_dictionary.gravestone.small.dim2);
      var memorial_feature = featureHelperService.createFeature(geometry, view_model._generateUUID());
      featureHelperService.addFeatureToLayer(memorial_feature, addMemorialService.addedMemorialsLayer);

      //add events
        eventService.pushEvent({
          group: 'add_memorial',
          name: 'move-plot',
          type: 'pointermove',
          handler: angular.bind(view_model, addMemorialService.memorialMoveHandler, memorial_feature)
        });

      //on placing plot, create the floating options handler at plot location
      eventService.pushEvent({
        group: 'add_memorial',
        name: 'place-plot',
        type: 'click',
        handler: angular.bind(view_model, view_model.placeMemorialHandler, memorial_feature, addMemorialService.addedGraveplotLayer)
      });

      eventService.pushEvent({
        group: 'burialTools',
        name: 'addPlot',
        type: 'pointermove',
        handler: floatingMemorialToolbarService.addMemorialMoveHandler
      });
    };

    view_model.editMemorialInteraction = function(){
        view_model.selectMemorialEvents(view_model.editMemorialHandler, 'select-plot');
        eventService.pushEvent({
            group: 'burialTools',
            name: 'editPlot',
            type: 'pointermove',
            handler: floatingMemorialToolbarService.editMemorialMoveHandler
        });
      eventService.pushEvent({
            group: 'add_memorial',
            name: 'highlight-memorial',
            layerGroup: ['memorials'],
            type: 'pointermove',
            handler: addMemorialService.highlightHoveredMemorials
        });
    };

    view_model.memorialCaptureInteraction = function() {

      view_model.openSidebar(sidebarEnum.memorialCapture);

      view_model.selectMemorialEvents(view_model.selectMemorialForMemorialCapture, 'memorial-capture-open');

      eventService.pushEvent({
        group: 'add_memorial',
        name: 'highlight-memorial',
        layerGroup: ['memorials'],
        type: 'pointermove',
        handler: addMemorialService.highlightHoveredMemorials
      });
    };

    view_model.graveLinkInteraction = function() {

      view_model.openSidebar(sidebarEnum.graveLink);

      view_model.selectMemorialEvents(view_model.selectMemorialForGraveLink, 'memorial-capture-open');

      eventService.pushEvent({
        group: 'add_memorial',
        name: 'highlight-memorial',
        layerGroup: ['memorials'],
        type: 'pointermove',
        handler: addMemorialService.highlightHoveredMemorials
      });
    };

    view_model.selectMemorialEvents = function(handlerFunction, name) {
      //on placing plot, create the floating options handler at plot location
      eventService.pushEvent({
        group: 'add_memorial',
        name: name,
        layerGroup: ['memorials'],
        type: 'click',
        handler: handlerFunction
      });
    };

    view_model.editMemorialHandler = function(evt, features, layerNames) {
      if (features[0]) {
        addMemorialService.stopBurialTools();

      //Get extra features clicked like lych_gate or bench
      var fu = addMemorialService.getFeatureUnderneath(evt);
      //Used only when closing floating toolbar
      // floatingMemorialToolbarService.initialise(features[0]).then(function(is_closing){
      floatingMemorialToolbarService.initialise(features[0],fu).then(function(is_closing){
        if(is_closing){
          //toggle off when toolbar is removed
          toolbarService.simulated_click('edit_plot');
          featureHelperService.removeGeometryListener(features[0], addMemorialService.placeToolbarAtFeature);
        }
      });

      addMemorialService.placeToolbarAtFeature({target:features[0]});
      featureHelperService.addGeometryListener(features[0], addMemorialService.placeToolbarAtFeature);

      }
    };

    view_model.defaultWidth = 280;

    /**
     * Open a sidebar
     */
    view_model.openSidebar = function(name) {

      if (name === sidebarEnum.memorialCapture) {
        view_model.showMemorialCaptureSidebar = true;
        view_model.showGraveLinkSidebar = false;
      }
      else if (name === sidebarEnum.graveLink) {
        view_model.showMemorialCaptureSidebar = false;
        view_model.showGraveLinkSidebar = true;
      }

      // hide/move these controls
      document.getElementById('horizontalToolsAccordion').style.display = "none";
      document.getElementById('layersAccordion').style.top = "55px";

      // attach events the the vue app will trigger
      jQuery(document).one('closeSidebar', function() {view_model.closeSidebar(name)});
      jQuery(document).on('narrowSidebar', function() {view_model.setSidebarWidth(280, name)});
      jQuery(document).on('wideSidebar', function() {view_model.setSidebarWidth(400, name)});
    };

    /**
     * Close a sidebar
     */
    view_model.closeSidebar = function(name) {
      // hide the sidebar
      document.getElementById(name).style.width = "0px";

      // allow annimation before removing component
      window.setTimeout(view_model.closeVueComponent, 500);

      if (name === sidebarEnum.memorialCapture) {
        //toggle the memorial_capture checkbox (i.e. turn it off)
        $scope.memorial.toggle.memorial_capture = false;
        view_model.memorialToolbarHandler('memorial_capture');
      }
      else if (name === sidebarEnum.graveLink) {
        //toggle the grave_link checkbox (i.e. turn it off)
        $scope.memorial.toggle.grave_link = false;
        view_model.memorialToolbarHandler('grave_link');
      }

      // show these controls again
      document.getElementById('horizontalToolsAccordion').style.display = "inline-flex";
      document.getElementById('layersAccordion').style.top = "100px";
      document.getElementById('layersAccordion').style.right = "5px";

      // remove events
      jQuery(document).off('narrowSidebar');
      jQuery(document).off('wideSidebar');
    };
    
    /**
     * close vue component
     */
    view_model.closeVueComponent = function() {
      view_model.showMemorialCaptureSidebar = false;
      view_model.showGraveLinkSidebar = false;
    }

    view_model.setSidebarWidth = function(width, elementID) {
      // set layers accordion horizontal position
      document.getElementById('layersAccordion').style.right = parseInt(width + 5) + "px";
      
      // set the sidebar width
      document.getElementById(elementID).style.width = parseInt(width) + "px";
      
      view_model.defaultWidth = width;
    };

    /**
     * Called when a memorial has been selected. Updates the sidebar.
     */
    view_model.selectMemorialForMemorialCapture = function(evt, features) {

      // If a feature has been clicked
      if (features[0]) {

        // Reload if the user isn't logged in
        //if(data.indexOf('loginModal') > -1)
        //  location.reload();
        
        jQuery(document).trigger('memorialSelectedForMemorialCapture', features[0]);
      }
    };

    /**
     * Called when a memorial has been selected. Updates the sidebar.
     */
    view_model.selectMemorialForGraveLink = function(evt, features) {

      // If a feature has been clicked
      if (features[0]) {

        // Reload if the user isn't logged in
        //if(data.indexOf('loginModal') > -1)
        //  location.reload();
        
        jQuery(document).trigger('memorialSelectedForGraveLink', features[0]);
      }
    };

    view_model.placeMemorialHandler = function(feature, layerName, evt) {
      floatingMemorialToolbarService.cleanup();
      floatingMemorialToolbarService.initialise(feature).then(function(is_closing){
        if(is_closing){
          //toggle off when toolbar is removed
          toolbarService.simulated_click('create_memorial');
          featureHelperService.removeGeometryListener(feature, addMemorialService.placeToolbarAtFeature);
        }
      });
        console.log('view_model.placeRectangle');
        addMemorialService.placeToolbarAtFeature({target:feature});
        featureHelperService.addGeometryListener(feature, addMemorialService.placeToolbarAtFeature);
        eventService.removeEventsByGroup('add_memorial');
    };

  }
]);
