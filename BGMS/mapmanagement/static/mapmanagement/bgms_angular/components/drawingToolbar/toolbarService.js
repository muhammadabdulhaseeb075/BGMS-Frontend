angular.module('bgmsApp.map').service('toolbarService', ['$q', 'addGraveService', 'addMemorialService', 'personInteractionService', 'eventService', 'notificationHelper', 'memorialService',
  function($q, addGraveService, addMemorialService, personInteractionService, eventService, notificationHelper, memorialService){

    var view_model = this;

    view_model.toggle = {
      //Other tools
      exportPDF: false,
	    siteFiles: false,
      //Burial Tools
      create_plot: false,
      edit_plot: false,
      //Memorial Tools
      create_memorial: false,
      edit_memorial: false,
      memorial_capture: false,
      grave_link: false,
      //Drawing tools
      draw_line: false,
      draw_polygon: false,
      modify_drawing: false,
      delete_drawing: false,
    };

    // Stores the permanent notification so it can be removed later
    view_model.memorialCaptureNotification = null;

    view_model.create_plot_question = messages.toolbar.toggleOption.text;

    view_model.removedEvents = [];
    view_model.removedEventsSub = [];

    view_model.get_toggle = function(){
    	return view_model.toggle;
    };

    view_model.toggle_option_noDisableEvents = function(current_selection){
    	var is_selected = $q.defer();
  		view_model.__toggle_option(current_selection);
  		is_selected.resolve(view_model.toggle[current_selection]);
    	return is_selected.promise;
    };

    view_model.toggle_option = function(current_selection){
    	var is_selected = $q.defer();
    	if((current_selection !='create_plot' && view_model.toggle['create_plot']) || (current_selection==='create_plot' && !view_model.toggle['create_plot']))
    		notificationHelper.createConfirmation(messages.toolbar.toggleOption.title, view_model.create_plot_question,
				function(){
					view_model.__toggle_option(current_selection);
					if(view_model.isEnabled()){
						view_model.removeEvents();
					} else{
						view_model.restoreEvents();
					}
					is_selected.resolve(view_model.toggle[current_selection]);
				},
				function(){
					view_model.toggle[current_selection] = false;
					view_model.toggle['create_plot'] = true;
					is_selected.resolve(view_model.toggle[current_selection]);
    		});
    	else{
    		view_model.__toggle_option(current_selection);
    		if(view_model.isEnabled()){
				view_model.removeEvents();
			} else{
				view_model.restoreEvents();
			}
    		is_selected.resolve(view_model.toggle[current_selection]);
    	}
    	return is_selected.promise;
    };

    view_model.simulated_click = function(current_selection){
    	view_model.toggle[current_selection] = !view_model.toggle[current_selection];
    	view_model.__toggle_option();
    	if(view_model.isEnabled()){
			view_model.removeEvents();
		} else{
			view_model.restoreEvents();
		}
    };

    view_model.__toggle_option = function(current_selection){
      view_model.stopActions();
      //deselect other options
      for (var key in view_model.toggle) {
        if (key != current_selection) {
          view_model.toggle[key] = false;
        }
      }
    };

    view_model.isEnabled = function(){
		for(var key in view_model.toggle){
			if(view_model.toggle[key]===true)
				return true;
		}
		return false;
    };

    view_model.removeEvents = function(){
      var events = eventService.removeEventsByGroupAndType('person', 'click');
      if (events && events.length > 0) {
        view_model.removedEvents.push.apply(view_model.removedEvents,events);
      }
      events = eventService.removeEventByName('hoverSelectFeatures');
      if (events && events.length > 0) {
        view_model.removedEvents.push.apply(view_model.removedEvents,events);
      }
      events = eventService.removeEventByName('hoverMemorialDetails');
      if (events && events.length > 0) {
        view_model.removedEvents.push.apply(view_model.removedEvents,events);
      }
    };

    view_model.restoreEvents = function() {
      // alert("restore events...controller...");
      if (view_model.removedEvents && view_model.removedEvents.length>0) {
        for (var i = view_model.removedEvents.length - 1; i >= 0; i--) {
          view_model.removedEvents[i].createLayers();
          eventService.pushEvent(view_model.removedEvents[i]);
        }
        view_model.removedEvents = [];
      }
    };

    // A second level for removing and restoring events
    view_model.removeEventsSub = function(){
        var events = eventService.removeEventsByGroupAndType('person', 'click');
        if (events && events.length > 0) {
        	view_model.removedEventsSub.push.apply(view_model.removedEventsSub,events);
        }
        events = eventService.removeEventByName('hoverSelectFeatures');
        if (events && events.length > 0) {
        	view_model.removedEventsSub.push.apply(view_model.removedEventsSub,events);
        }
    };

    view_model.restoreEventsSub = function() {
        // alert("restore events...controller...");
        if (view_model.removedEventsSub && view_model.removedEventsSub.length>0) {
          for (var i = view_model.removedEventsSub.length - 1; i >= 0; i--) {
        	  view_model.removedEventsSub[i].createLayers();
        	  eventService.pushEvent(view_model.removedEventsSub[i]);
          }
          view_model.removedEventsSub = [];
        }
    };

    view_model.stopActions = function(){
		//remove drawing interactions
		jQuery(document).trigger('stopDrawing');
		// remove burial tools interactions
		addGraveService.stopBurialTools();
		// remove burial tools interactions
		addMemorialService.stopBurialTools();
    };

}]);
