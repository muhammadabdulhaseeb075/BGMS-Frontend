"use strict";

describe("person interaction service", function () {
  var personInteractionService, eventService, markerService, layerGroupService;

  beforeEach(module("bgmsApp"));

  beforeEach(inject(function (_personInteractionService_, _eventService_, _markerService_, _layerGroupService_) {
	  personInteractionService = _personInteractionService_;
	  eventService = _eventService_;
	  markerService = _markerService_;
	  layerGroupService = _layerGroupService_;
	  layerGroupService.addLayerGroup(layerGroupService.createLayerGroup({
			name: 'memorials',
			display_name: 'memorials',
			switch_on_off: true,
			visibility: true,
			hierarchy: 1
		}));
	  layerGroupService.addLayerGroup(layerGroupService.createLayerGroup({
			name: 'memorial_cluster',
			display_name: 'memorial_cluster',
			switch_on_off: true,
			visibility: true,
			hierarchy: 2
		}));
  }));
  
  //testing detailsOnHoverEvent
  it("should add/remove event to show details on hover", function(){
	  personInteractionService.detailsOnHoverEvent(true);
	  expect(eventService.getEvents().length).toBe(1);
	  expect(eventService.getEvents()[0].name).toBe('hoverMemorialDetails');
	  expect(eventService.getEvents()[0].type).toBe('pointermove');
	  personInteractionService.detailsOnHoverEvent(false);
	  expect(eventService.getEvents().length).toBe(0);
  });
  
  // testing highlightOnHoverEvent function
  it("should add/remove event to highlight features on hover", function () {
	  personInteractionService.highlightOnHoverEvent(true);
	  expect(eventService.getEvents().length).toBe(1);
	  expect(eventService.getEvents()[0].name).toBe('hoverSelectFeatures');
	  expect(eventService.getEvents()[0].type).toBe('pointermove');
	  personInteractionService.highlightOnHoverEvent(false);
	  expect(eventService.getEvents().length).toBe(0);
  });
  
  // testing toggleDetailsMarker function
  it("should add/remove marker based on whether coordinate is specified", function () {
	  personInteractionService.toggleDetailsMarker('test', [1,1], undefined);
	  expect(markerService.getMarkers().length).toBe(1);
	  expect(markerService.getMarkers()[0].name).toBe('test');
	  personInteractionService.toggleDetailsMarker('test');
	  expect(markerService.getMarkers().length).toBe(0);
  });
  
//  //testing createDetailsTemplate
//  it("should create template", function () {
//	  
//  });

});