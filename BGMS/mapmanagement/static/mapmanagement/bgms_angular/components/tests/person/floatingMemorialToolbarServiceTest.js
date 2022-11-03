"use strict";

describe("floating memorial toolbar service", function () {
  var floatingMemorialToolbarService, geometryHelperService, featureHelperService, $httpBackend, $rootScope, $compile;
  var feature, scope, element, geometry;
  
  beforeEach(module("bgmsApp"));

  beforeEach(inject(function (_$httpBackend_, _$rootScope_, _$compile_, _floatingMemorialToolbarService_, _featureHelperService_, _geometryHelperService_) {
	  //creating map, geometry and layer
	  featureHelperService = _featureHelperService_;
	  geometryHelperService = _geometryHelperService_;
	  geometry = _geometryHelperService_.createPolygonGeometry('rectangle', [0,0], 2);
	  $rootScope = _$rootScope_;
	  $compile = _$compile_;
	  scope = $rootScope.$new();  
	  scope.mapbox = {
		        source: {
		            type: 'EmptyVector'
		        },
	            name: 'testlayer'
		    };
      element = angular.element('<openlayers>' +
              '<ol-layer ol-layer-properties="mapbox"></ol-layer>' +
              '</openlayers>');
      element = $compile(element)(scope);
      scope.$digest();
      feature = featureHelperService.createFeature(geometry, 'stringId');
	  featureHelperService.addFeatureToLayer(feature, 'testlayer');
      scope.$digest();

      //setting up http backend

	  $httpBackend =  _$httpBackend_;
      
	  floatingMemorialToolbarService = _floatingMemorialToolbarService_;
	  floatingMemorialToolbarService.initialise(feature);

  }));

  
//  //testing deleteMemorial
  it("should delete memorial from testlayer", function(){
	  $httpBackend.expectPOST('/mapmanagement/deleteHeadstone/', {
          'memorial_id': 'stringId',
          'marker_type': 'testlayer'
        }).respond(200, '{"status":"OK"}');
	  floatingMemorialToolbarService.deleteMemorial('stringId', 'testlayer');
	  $httpBackend.flush();
      scope.$digest();
	  var returnedFeature = 0;
	  featureHelperService.getFeatureFromLayer('stringId', 'testlayer').then(function(returnedFeature){
		  expect(returnedFeature).toBe(null);
	  });
      scope.$digest();
  });
  
  it("should fail to delete memorial from testlayer", function(){
	  $httpBackend.expectPOST('/mapmanagement/deleteHeadstone/', {
          'memorial_id': 'stringId',
          'marker_type': 'testlayer'
        }).respond(400, 'Memorial has person attached');
	  floatingMemorialToolbarService.deleteMemorial('stringId', 'testlayer');
	  $httpBackend.flush();
	  var returnedFeature = 0;
	  featureHelperService.getFeatureFromLayer('stringId', 'testlayer').then(function(returnedFeature){
		  expect(returnedFeature).toBe(feature);
	  });
      scope.$digest();
  });
  
  //testing cancleSave
  it("should restore the feature to original location", function(){
	  feature.setGeometry(geometryHelperService.createPolygonGeometry('rectangle', [0,0], 2));
	  floatingMemorialToolbarService.cancelSave();
	  expect(feature.getGeometry().getCoordinates()).toEqual(geometry.getCoordinates());	  
  });
  
});