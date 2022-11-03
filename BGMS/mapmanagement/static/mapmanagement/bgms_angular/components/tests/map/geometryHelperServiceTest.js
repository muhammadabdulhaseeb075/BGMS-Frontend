"use strict";

describe("geometry helper service", function () {
  var geometryHelperService, httpBackend;

  beforeEach(module("bgmsApp"));
//  beforeEach(module("bgmsApp.map"));

  beforeEach(inject(function (_geometryHelperService_, _$httpBackend_) {
	geometryHelperService = _geometryHelperService_;
    httpBackend =  _$httpBackend_;
  }));

  // testing createPolygonGeometry function
  it("should create rectangle of multipolygon geometry", function () {
	  var geometry = geometryHelperService.createPolygonGeometry('rectangle', [2,3], 1, 2);
	  //test that a multipolygon is created
	  expect(geometry.constructor === ol.geom.MultiPolygon).toEqual(true);	  
	  //tests that it is a rectangle i.e. it has coordinates, with start and end being the same
	  expect(geometry.getCoordinates()[0][0].length === 5).toEqual(true);
	  expect(geometry.getCoordinates()[0][0][0]).toEqual(geometry.getCoordinates()[0][0].pop());
	  expect(geometry.getArea()).toEqual(2);
  });
  
  it("should create square of multipolygon geometry", function () {
	  var geometry = geometryHelperService.createPolygonGeometry('rectangle', [2,3], 1);
	  //test that a multipolygon is created
	  expect(geometry.constructor === ol.geom.MultiPolygon).toEqual(true);	  
	  //tests that it is a rectangle i.e. it has coordinates, with start and end being the same
	  expect(geometry.getCoordinates()[0][0].length === 5).toEqual(true);
	  expect(geometry.getArea()).toEqual(1);
  });
  
  it("should create circle of multipolygon geometry", function () {
	  var geometry = geometryHelperService.createPolygonGeometry('circle', [2,3], 1);
	  //test that a multipolygon is created
	  expect(geometry.constructor === ol.geom.MultiPolygon).toEqual(true);	
	  //tests that it is a circle i.e. it has no. of coordinates>30, with start and end being the same
	  expect(geometry.getCoordinates()[0][0].length>30).toEqual(true);
	  expect(geometry.getCoordinates()[0][0][0]).toEqual(geometry.getCoordinates()[0][0].pop());
  });

  // testing getRotationAngle function
  it("should get a rotation angle of -45", function () {
	  var angle = geometryHelperService.getRotationAngle([0,0], [1, 1]);
	  expect(angle).toEqual(-Math.PI/4);	
  });

  it("should get a rotation angle of -90", function () {
	  var angle = geometryHelperService.getRotationAngle([0,0], [1, 0]);
	  expect(angle).toEqual(-Math.PI/2);
  });

  it("should get a rotation angle of 0", function () {
	  var angle = geometryHelperService.getRotationAngle([0,0], [0, 1]);
	  expect(angle).toEqual(0);	
  });
  
  // testing rotateTransformFunction function

  it("should get the same array when rotation angle is 0", function () {
	  // input array - straight line parallel to x axis
	  var inputArray = [2,2,3,2]
	  var outputArray = geometryHelperService.rotateTransformFunction([0,0],0, inputArray);
	  expect(outputArray).toEqual(inputArray);	
  });

  it("should get a rotated array when rotation angle is 90", function () {
	  // input array - straight line parallel to x axis
	  var inputArray = [2,2,3,2]
	  var outputArray = geometryHelperService.rotateTransformFunction([2,2], Math.PI/2, inputArray);
	  expect(outputArray).toEqual([2,2,2,3]);	
  });
  
  it("should get a rotated array when rotation angle is 45", function () {
	  // input array - straight line parallel to x axis
	  var inputArray = [2,2,3,2]
	  var outputArray = geometryHelperService.rotateTransformFunction([2,2], Math.PI/4, inputArray);
	  expect(outputArray).toEqual([2,2,2+1/Math.sqrt(2),2+1/Math.sqrt(2)]);	
  });
  
  // testing translateGeometry function
//  it("should move a polygon to be centred at new location", function () {
//	  var square = geometryHelperService.createPolygonGeometry('rectangle', [0,0], 2);
//  });
  
});