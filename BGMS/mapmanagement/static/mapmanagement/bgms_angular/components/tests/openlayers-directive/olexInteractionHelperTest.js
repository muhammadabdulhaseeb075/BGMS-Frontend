"use strict";

describe("add grave service", function () {
  var olexInteractionHelper, featureHelperService, geometryHelperService;

  beforeEach(module("bgmsApp"));
//  beforeEach(module("bgmsApp.map"));

  beforeEach(inject(function (_olexInteractionHelper_, _featureHelperService_, _geometryHelperService_) {
	olexInteractionHelper = _olexInteractionHelper_;
    geometryHelperService =  _geometryHelperService_;
    featureHelperService = _featureHelperService_;
  }));

  it("should create an interaction of type ol.interaction.Translate with specified feature", function () {
	  var geometry = geometryHelperService.createPolygonGeometry('rectangle', [2,3], 1, 2);
	  var feature1 = featureHelperService.createFeature(geometry, 'stringId');
	  var feature_collection = new ol.Collection(feature1);
	  var translate = olexInteractionHelper.createTranslateInteraction(feature_collection);
	  expect(translate.constructor).toEqual(ol.interaction.Translate);
  });
  

});