"use strict";

describe("add grave service", function () {
  var addGraveService, httpBackend;

  beforeEach(module("bgmsApp"));
//  beforeEach(module("bgmsApp.map"));

  beforeEach(inject(function (_addGraveService_, _$httpBackend_) {
    addGraveService = _addGraveService_;
    httpBackend =  _$httpBackend_;
  }));

//  it("should create rectangle of multipolygon geometry", function () {
//	  var geometry = addGraveService.createPolygonGeometry('rectangle', [2,3], 1, 2);
//	  expect(geometry.constructor === ol.geom.MultiPolygon).toEqual(true);	  
//  });
//  
//  it("should create circle of multipolygon geometry", function () {
//	  var geometry = addGraveService.createPolygonGeometry('circle', [2,3], 1);
//	  expect(geometry.constructor === ol.geom.MultiPolygon).toEqual(true);	
//  });

//  it("should get an angle of 90", function () {
//	  var geometry = addGraveService.createPolygonGeometry('circle', [2,3], 1);
//	  expect(geometry.constructor === ol.geom.MultiPolygon).toEqual(true);	
//  });
//
//  it("should get an angle of 0", function () {
//	  var geometry = addGraveService.createPolygonGeometry('circle', [2,3], 1);
//	  expect(geometry.constructor === ol.geom.MultiPolygon).toEqual(true);	
//  });
//
//  it("should create circle of multipolygon geometry", function () {
//	  var geometry = addGraveService.createPolygonGeometry('circle', [2,3], 1);
//	  expect(geometry.constructor === ol.geom.MultiPolygon).toEqual(true);	
//  });
  
//  it("should set create feature and set feature id and marker_type", function () {
//	  var geom = addGraveService.createPolygonGeometry('rectangle', [1,2], 1, 2);
//	  var feature = addGraveService.createFeature(geom, 'available_plot', '1234');
//	  expect(feature.constructor === ol.Feature).toEqual(true);
//	  expect(feature.get('id') === ('available_plot'+';'+'1234')).toEqual(true);
//	  expect(feature.get('marker_type') === 'available_plot').toEqual(true);
//  });
//  
//  it("should create polygon", function () {
//    layerService.addLayer('baseLayer', 'Layer').then(function(subreddits) {
//      expect(subreddits).toEqual(["golang", "javascript"]);
//    });
//    httpBackend.flush();
//  });
//  
//  it("should create polygon", function () {
//    layerService.addLayer('baseLayer', 'Layer').then(function(subreddits) {
//      expect(subreddits).toEqual(["golang", "javascript"]);
//    });
//    httpBackend.flush();
//  });
  
});