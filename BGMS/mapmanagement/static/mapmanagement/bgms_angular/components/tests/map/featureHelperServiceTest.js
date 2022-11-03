"use strict";

describe("feature helper service", function () {
  var featureHelperService, geometryHelperService, olData, geometry;
  var $compile, $rootScope, scope, element;

  beforeEach(module("bgmsApp"));
//  beforeEach(module("bgmsApp.map"));

  beforeEach(inject(function (_$rootScope_, _$compile_, _featureHelperService_, _olData_, _geometryHelperService_) {
    featureHelperService = _featureHelperService_;
    olData =  _olData_;
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
    scope.mapbox2 = {
            source: {
                type: 'EmptyVector'
            },
              name: 'testlayer2'
        };
        element = angular.element('<openlayers>' +
                '<ol-layer ol-layer-properties="mapbox"></ol-layer>' +
                '<ol-layer ol-layer-properties="mapbox2"></ol-layer>' +
                '</openlayers>');
        element = $compile(element)(scope);
        scope.$digest();
  }));
  
  afterEach(inject(function($rootScope) {
//      $rootScope.$apply();
  }));

  //testing createFeature function
  it("should create a feature", function () {
    var feature = featureHelperService.createFeature(geometry, 'stringId');
    expect(feature.constructor).toEqual(ol.Feature);
    expect(feature.getId()).toEqual('stringId');
    feature = featureHelperService.createFeature(geometry, 1234);
    expect(feature.constructor).toEqual(ol.Feature);
    expect(feature.getId()).toEqual(1234);
  });
  
  it("should fail to create a feature", function () {
    var feature = featureHelperService.createFeature(null, 'stringId');
    expect(feature===null).toEqual(true);
    feature = featureHelperService.createFeature(geometry);
    expect(feature===null).toEqual(true);
  });

  //testing setFeatureGeometry 
  it("should set the geometry to circle", function () {
    var feature = featureHelperService.createFeature(geometry, 'stringId');
    expect(feature.constructor).toEqual(ol.Feature);
    expect(feature.getGeometry()).toBe(geometry);
    var geometry2 = geometryHelperService.createPolygonGeometry('circle', [0,0], 2);
    featureHelperService.setFeatureGeometry(feature, geometry2);
    expect(feature.getGeometry()).toBe(geometry2);
  });

  it("should not change geometry", function () {
    var feature = featureHelperService.createFeature(geometry, 'stringId');
    featureHelperService.setFeatureGeometry(feature, null);
    expect(feature.getGeometry()).toBe(geometry);
  });
    
  //testing setFeatureId 
  it("should set the feature id to stringIdNew", function () {
    var feature = featureHelperService.createFeature(geometry, 'stringId');
    featureHelperService.addFeatureToLayer(feature, 'testlayer')
    featureHelperService.setFeatureId(feature, 'stringIdNew');
    scope.$apply();
    expect(feature.getId()).toBe('stringIdNew');
    var feature = featureHelperService.createFeature(geometry, 'stringId');
    featureHelperService.setFeatureId(feature, 'stringIdNew');
    expect(feature.getId()).toBe('stringIdNew');
  });

  //testing addFeatureToLayer function
  it("should add feature to layer", function () {
    var feature1 = featureHelperService.createFeature(geometry, 'stringId');
    featureHelperService.addFeatureToLayer(feature1, 'testlayer');
    var feature2 = featureHelperService.createFeature(geometry, 1234);
    featureHelperService.addFeatureToLayer(feature2, 'testlayer');
    var d_f1, d_f2;
    var map = window.OLMap;
    console.log('map');
    console.log(map.getLayers());
    console.log(map.getLayers().getArray()[1].get('name'));
    d_f1 = map.getLayers().getArray()[1].getSource().getFeatureById('stringId');
    d_f2 = map.getLayers().getArray()[1].getSource().getFeatureById('1234')
    scope.$digest();
    featureHelperService.addFeatureToLayer(feature1, 'testlayer');
    scope.$digest();
    expect(d_f1).toBe(feature1);
    expect(d_f1.getId()).toEqual('stringId');
    expect(d_f2).toBe(feature2);
  });
  
  //testing getFeatureFromLayer function
  it("should get feature from layer", function () {
    var feature1 = featureHelperService.createFeature(geometry, 'stringId');
    featureHelperService.addFeatureToLayer(feature1, 'testlayer');
    var feature2 = featureHelperService.createFeature(geometry, 1234);
    featureHelperService.addFeatureToLayer(feature2, 'testlayer');
    var df1,df2;
    featureHelperService.getFeatureFromLayer('stringId', 'testlayer').then(function(feature){
      df1 = feature;
    });
    featureHelperService.getFeatureFromLayer(1234, 'testlayer').then(function(feature){
      df2 = feature;
    });
      scope.$digest();
      expect(df1).toBe(feature1);
      expect(df2).toBe(feature2);
  });
  
  //testing removeFeatureFromLayer
  it("should remove feature from layer", function () {
    var feature1 = featureHelperService.createFeature(geometry, 'stringId');
    featureHelperService.addFeatureToLayer(feature1, 'testlayer');
    var feature2 = featureHelperService.createFeature(geometry, 1234);
    featureHelperService.addFeatureToLayer(feature2, 'testlayer');
    scope.$apply();
    var df1, df2, df3;
    featureHelperService.removeFeatureFromLayer('stringId', 'testlayer').then(function(feature){
      df1 = feature;
    });
      scope.$digest();
    expect(df1).toBe(feature1);
    featureHelperService.getFeatureFromLayer('stringId', 'testlayer').then(function(feature){
      df2 = feature;
    });
      scope.$digest();
    expect(df2).toBe(null);
    featureHelperService.getFeatureFromLayer(1234, 'testlayer').then(function(feature){
      df3 = feature; 
    });
      scope.$digest();
      expect(df3).toBe(feature2);
  });
  
  //testing removeAllFeaturesFromLayer
  it("should remove all features from layer", function () {
    var feature1 = featureHelperService.createFeature(geometry, 'stringId');
    featureHelperService.addFeatureToLayer(feature1, 'testlayer');
    var feature2 = featureHelperService.createFeature(geometry, 1234);
    featureHelperService.addFeatureToLayer(feature2, 'testlayer');
    featureHelperService.removeAllFeaturesFromLayer('testlayer');
    scope.$apply();
    featureHelperService.getFeatureFromLayer('stringId', 'testlayer').then(function(feature){
      expect(feature).toBe(null);
    });
    featureHelperService.getFeatureFromLayer(1234, 'testlayer').then(function(feature){
      expect(feature).toBe(null);
    });
  });
  
  // testing moveFeatureBetweenLayers
  it("should move feature from testlayer to testlayer2", function () {
    var feature1 = featureHelperService.createFeature(geometry, 'stringId');
    featureHelperService.addFeatureToLayer(feature1, 'testlayer');
//    scope.$apply();
    featureHelperService.moveFeatureBetweenLayers(feature1, 'testlayer', 'testlayer2');
    scope.$apply();
    var df1, df2;
    featureHelperService.getFeatureFromLayer('stringId', 'testlayer').then(function(feature){
      df1 = feature;
    });
    featureHelperService.getFeatureFromLayer('stringId', 'testlayer2').then(function(feature){
      df2 = feature;
    });
      scope.$digest();
//    expect(df1).toBe(null);
//    expect(df2).toBe(feature1); 
//    expect(df2.getId()).toBe('testlayer2;stringId');
  });
  
  //testing addGeometryListener
  it("should add listener function to feature", function () {
    var feature1 = featureHelperService.createFeature(geometry, 'stringId');
    var changed = false;
    var listener = function(){
      changed = true;
    };
    var ret = featureHelperService.addGeometryListener(feature1, listener);
    expect(ret).not.toEqual(null);
    feature1.setGeometry(null);
    expect(changed).toEqual(true);
  });
  
  //testing removeGeometryListener
  it("should remove listener function by key", function () {
    var feature1 = featureHelperService.createFeature(geometry, 'stringId');
    var changed = false;
    var listener = function(){
      changed = true;
    };
    var ret = featureHelperService.addGeometryListener(feature1, listener);
    featureHelperService.removeGeometryListener(feature1, ret);
    feature1.setGeometry(null);
    expect(changed).toEqual(false);
  });
  
  it("should remove listener function by function", function () {
    var feature1 = featureHelperService.createFeature(geometry, 'stringId');
    var changed = false;
    var listener = function(){
      changed = true;
    };
    var ret = featureHelperService.addGeometryListener(feature1, listener);
    featureHelperService.removeGeometryListener(feature1, listener);
    feature1.setGeometry(null);
    expect(changed).toEqual(false);
  });
  
});