"use strict";

describe("olex map event directive", function () {
  var $compile, $rootScope, scope, element;

  beforeEach(module("bgmsApp"));
//  beforeEach(module("bgmsApp.map"));

  beforeEach(inject(function (_$compile_, _$rootScope_) {
	  $compile = _$compile_;
	  $rootScope = _$rootScope_;
	  scope = $rootScope.$new();
	  scope.mapbox = {
		        source: {
		            type: 'EmptyVector'
		        },
	            name: 'testlayer'
		    };
	  scope.mapbox2 = {
		        source: {
		            type: 'EmptyVector'
		        },
	            name: 'testlayer2'
		    };
	  scope.event = {
	    		group: 'person',
	    		name: 'clickMemorialDetails',
	    		type: 'click'
	    	};
	  element = angular.element("<openlayers>"+
              						'<ol-layer ol-layer-properties="mapbox"></ol-layer>' +
              						'<ol-layer ol-layer-properties="mapbox2"></ol-layer>' +
			  						"<olex-map-event olex-event-properties='event'></olex-map-event>"+
			  					"</openlayers>");
      element = $compile(element)(scope);
      scope.$digest();
  }));
  
  // testing event callback function
  it("should call scope.apply on event callback", function () {
	  console.log('click on map');
	  scope.event.handler = function(){
		  console.log('click on map');
		  expect($rootScope.$$phase).toBe("$apply");
	  };
	  scope.event.layers = ['mapbox'];
	  element.click();
  });
  
  it("should call event on updated layer", function () {
	  console.log('click on map');
	  scope.event.handler = function(){
		  console.log('click on map');
		  expect($rootScope.$$phase).toBe("$apply");
	  };
	  scope.event.layers = ['mapbox'];
	  element.click();
  });

});