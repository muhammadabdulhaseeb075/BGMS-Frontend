"use strict";

describe("person interaction service", function () {
  var openlayersService;

  beforeEach(module("bgmsApp.dataentry"));

  beforeEach(inject(function (_openlayersService_) {
	  openlayersService = _openlayersService_;
  }));
  
  //testing _getPosition
  it("should get position", function(){
	  var array = [];
	  array.push({name:'1'});
	  array.push({name: '2'});
	  expect(openlayersService._getPosition('1', array)).toBe('0');
	  expect(openlayersService._getPosition('4', array)).toBe(-1);
  });
  
});