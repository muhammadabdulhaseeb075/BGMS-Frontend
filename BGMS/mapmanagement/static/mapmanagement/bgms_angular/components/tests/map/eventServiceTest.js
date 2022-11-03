"use strict";

describe("event service", function () {
  var eventService, $compile, $rootScope, scope;

  beforeEach(module("bgmsApp"));
//  beforeEach(module("bgmsApp.map"));

  beforeEach(inject(function (_eventService_, _$compile_, _$rootScope_) {
	  eventService = _eventService_;
  }));
  
  //testing MapEvent.addLayerNames
  it("should add layer to layers", function(){
	  var mapEvent =  eventService.pushEvent({
	  		group: 'test',
			name: 'click-test',
			layerNames: ['plot'],
			type: 'click'
		  });
	  mapEvent.addLayerNames('test');
	  expect(mapEvent.layers.length).toBe(2);
	  expect(mapEvent.layers).toContain('test');
	  
	  mapEvent.addLayerNames(['test1', 'test2']);
	  expect(mapEvent.layers.length).toBe(4);
	  expect(mapEvent.layers).toContain('test1');
	  expect(mapEvent.layers).toContain('test2');
  });
  
  // testing getEventsByGroup function
  it("should return events belonging to the group", function () {
	  //add events of group test and not-test and check that it extracts the right events
	  eventService.pushEvent({
  		group: 'test',
		name: 'click-test',
		layerNames: ['plot'],
		type: 'click'
	  });
	  eventService.pushEvent({
	  		group: 'test',
			name: 'hover-test',
			layerNames: ['plot'],
			type: 'pointermove'
	  });
	  eventService.pushEvent({
	  		group: 'not-test',
			name: 'hover-test',
			layerNames: ['plot'],
			type: 'pointermove'
	  });
	  var testEvents = eventService.getEventsByGroup('test');
	  expect(testEvents.length).toBe(2);
	  expect(testEvents[0].group).toBe('test');
	  expect(testEvents[1].group).toBe('test');
	  expect(eventService.getEvents().length).toBe(2);
  });

});