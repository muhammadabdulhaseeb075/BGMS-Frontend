angular.module('bgmsApp.map').service('exportMapService', ['$http', 'layerService', 'styleService', 'personInteractionService', 'featureOverlayService', '$window', 'subdomain','securityService', 'markerService',
  function($http, layerService, styleService, personInteractionService, featureOverlayService, $window, subdomain, securityService, markerService) {

    var vm = this;
    vm.memorialsFeaturesId = {};
    vm.groupNameLabels = 'memorials';
    vm.groupNamePlots = 'plots'; //geometriespublic_featuregroup
    vm.widthMap = 0;
    vm.heightMap = 0;
    vm.ratioWidthA4 = 0;
    vm.widthBackground = 0;

    vm.createMemorialLabelStyle = function(feature_id, fillColor, strokeColor, fontSize) {
      var style = new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: strokeColor,
          width: 1
        }),
        fill: new ol.style.Fill({
          color: fillColor,
        }),
        text: styleService.createTextStyle(feature_id, fontSize)
      });
      return [style];
    };

    vm.createMemorialBenchLabelStyle = function(feature_id, fillColor, strokeColor, feature, resolution, fontSize) {
      var vectorStyle = window.MapLayers.layerStyles.memorials_bench(feature,resolution, feature_id, fontSize);
      //add text to bench
      // if(vectorStyle[0] !== undefined){
        // vectorStyle[0].getText().setText(vm.createTextStyle(feature_id));
        // vectorStyle[0].getText().setText(feature_id);
      // }
      // var style = new ol.style.Style({
			// 	image: new ol.style.Icon({
		  //       		opacity: 1,
		  //       		src: jsAngularInterface.mainPartialFileLocation+'mapmanagement/assets/img/Memorial-Bench.png',
		  //       		scale: 1,
			// 					crossOrigin: location.hostname,
		  //       	}),
      //   geometry: feature.getGeometry().getInteriorPoints(),
			// 	text: vm.createTextStyle(feature_id)
			// });
      return vectorStyle;
    };

    vm.getolLayersByGroup = function(groupName, map){
      var angularGroupLayers = layerService.getLayersByGroup(groupName);
      // var gravestoneAngularLayer = layerService.getLayerByName('gravestone');
      // var gravestoneLayer = map.getLayers().getArray()[gravestoneAngularLayer.zIndex]; //TODO: wrong z-index in layerangular vs OpenLayers
      var groupLayers = {};
      var layers = map.getLayers().getArray();
      for (var i = 0; i < layers.length; i++) {
        for (var mlayer in angularGroupLayers) { 
          if (layers[i].getProperties().name == mlayer) {
            groupLayers[mlayer] = layers[i];
            // angularGroupLayers[mlayer].style = styleService["temp_style"];
            break;
          }
        }
      }
      return groupLayers;
    };
    vm.changeAllMemorialsLabel = function(fontSize, graveplotlist_string){
      var graveplotlist = JSON.parse(graveplotlist_string);
      var memorialsGroupLayers = vm.getolLayersByGroup(vm.groupNameLabels, window.OLMap);
      for (var ollayer in memorialsGroupLayers) {
        var olFeatures = memorialsGroupLayers[ollayer].getSource().getFeatures();
        var styleLayer,fillColor,strokeColor='';
        for (i = 0; i < olFeatures.length; i++) {
          if( olFeatures[i].values_ &&
            (graveplotlist[olFeatures[i].values_.real_feature_id] || graveplotlist[olFeatures[i].values_.feature_id]) ){
            let grave_number = graveplotlist[olFeatures[i].values_.real_feature_id] ? graveplotlist[olFeatures[i].values_.real_feature_id] : graveplotlist[olFeatures[i].values_['feature_id']];
            if(ollayer != 'memorials_bench'){
              // Get style layer, in case does not exist fill with default layer
              if(typeof window.MapLayers.layerStyles[ollayer] === "function"){
              styleLayer = window.MapLayers.layerStyles[ollayer]()[0]; 
              }else{
                styleLayer = window.MapLayers.layerStyles['default']()[0];
              }
              fillColor = styleLayer.getFill().getColor();
              strokeColor = styleLayer.getStroke().getColor();
              olFeatures[i].setStyle(vm.createMemorialLabelStyle(grave_number.toString(),
                  fillColor, strokeColor, fontSize));
            }else {
                olFeatures[i].setStyle(vm.createMemorialBenchLabelStyle(grave_number.toString(),
                  fillColor, strokeColor, olFeatures[i], window.OLMap.getView().getResolution(), fontSize));
              }
          }
        }
      }
    };
    vm.burialNumber = function(fontSize, graveplotlist_string){
      var graveplotlist = JSON.parse(graveplotlist_string);
      // var graveplotlist = JSON.parse(JSON.stringify(graveplotlist_string))
      var memorialsGroupLayers = vm.getolLayersByGroup(vm.groupNameLabels, window.OLMap);
      for (var ollayer in memorialsGroupLayers) {
        var olFeatures = memorialsGroupLayers[ollayer].getSource().getFeatures();
        var styleLayer,fillColor,strokeColor='';
        for (i = 0; i < olFeatures.length; i++) {
          if( olFeatures[i].values_ &&
              (graveplotlist[olFeatures[i].values_.real_feature_id] || graveplotlist[olFeatures[i].values_.feature_id]) ){
            let burial_number = graveplotlist[olFeatures[i].values_.real_feature_id] ? graveplotlist[olFeatures[i].values_.real_feature_id] : graveplotlist[olFeatures[i].values_['id']];
            if(ollayer != 'memorials_bench'){
              // Get style layer, in case does not exist fill with default layer
              if(typeof window.MapLayers.layerStyles[ollayer] === "function"){
                styleLayer = window.MapLayers.layerStyles[ollayer]()[0]; 
              }else{
                styleLayer = window.MapLayers.layerStyles['default']()[0];
              }
              fillColor = styleLayer.getFill().getColor(); 
              strokeColor = styleLayer.getStroke().getColor();
              olFeatures[i].setStyle(vm.createMemorialLabelStyle(burial_number.burial_number,
                  fillColor, strokeColor, fontSize));
            }else {
                olFeatures[i].setStyle(vm.createMemorialBenchLabelStyle(burial_number.burial_number,
                  fillColor, strokeColor, olFeatures[i], window.OLMap.getView().getResolution(), fontSize));
              }
          }
        }
      }
    };
    vm.changeAllMemorialsText = function(fontSize){
      var memorialsGroupLayers = vm.getolLayersByGroup(vm.groupNameLabels, window.OLMap);

      for (var ollayer in memorialsGroupLayers) {
        var olFeatures = memorialsGroupLayers[ollayer].getSource().getFeatures();
        var styleLayer,fillColor,strokeColor='';

        for (i = 0; i < olFeatures.length; i++) {
          if(ollayer != 'memorials_bench'){
            // Get style layer, in case does not exist fill with default layer
            if(typeof window.MapLayers.layerStyles[ollayer] === "function"){
              styleLayer = window.MapLayers.layerStyles[ollayer]()[0];
            }else{
              styleLayer = window.MapLayers.layerStyles['default']()[0];
            }
            fillColor = styleLayer.getFill().getColor();
            strokeColor = styleLayer.getStroke().getColor();
            olFeatures[i].setStyle(vm.createMemorialLabelStyle(
              (olFeatures[i].get("feature_id") !== null) ? (olFeatures[i].get("feature_id")).toString() : '',
              fillColor, strokeColor, fontSize));
          } else {
            olFeatures[i].setStyle(vm.createMemorialBenchLabelStyle(
              (olFeatures[i].get("feature_id") !== null) ? (olFeatures[i].get("feature_id")).toString() : '',
              fillColor, strokeColor, olFeatures[i], window.OLMap.getView().getResolution(), fontSize));
          }
        }
      }
    };

    vm.restoreMemorialsStyle = function() {
      var memorialsGroupLayers = vm.getolLayersByGroup(vm.groupNameLabels, window.OLMap);
      for (var ollayer in memorialsGroupLayers) {
        var olFeatures = memorialsGroupLayers[ollayer].getSource().getFeatures();
        for (i = 0; i < olFeatures.length; i++) {
          olFeatures[i].setStyle(undefined);
        }
      }
    };

    vm.createPrintingArea = function() {
      vm.widthMap = $(window).width();
      vm.heightMap = $(window).height() - angular.element(document.querySelector(".top-nav"))[0].clientHeight;
      vm.ratioWidthA4 = Math.ceil((vm.heightMap * 842)/595);
      vm.widthBackground = vm.widthMap-vm.ratioWidthA4;

      //Change to portrait mode the exporting area for square screens
      if(vm.widthBackground <= 155){
        vm.ratioWidthA4 = Math.ceil((vm.heightMap * 595)/842);
        vm.widthBackground = vm.widthMap-vm.ratioWidthA4;
      }

      //Change size background accordingly to the screen size
      angular.element(document.querySelector('.exportMap.left'))[0].style.height = vm.heightMap + "px";
      angular.element(document.querySelector('.exportMap.left'))[0].style.width = vm.widthBackground/2 + "px";
      // angular.element('.exportMap.left').css( 'right', angular.element('.exportMap.left').width() + angular.element('.exportMap.left').offset().left - widthMap );

			angular.element(document.querySelector('.exportMap.right'))[0].style.height = vm.heightMap + "px";
			angular.element(document.querySelector('.exportMap.right'))[0].style.width = vm.widthBackground/2 + "px";
      // angular.element('.exportMap.right').css( 'right', angular.element('.exportMap.right').offset().left);

      //Move mouse position to the printing area
      angular.element(document.querySelector('.olex-mouse-position')).css('left',((vm.widthBackground/2) + 5)+'px');

      //Move scale bar to the printing area
      angular.element(document.querySelector('.ol-scale-line')).css('left',(vm.widthMap - (vm.widthBackground/2) - 92)+'px');
      angular.element(document.querySelector('.ol-scale-line')).css('top',(vm.heightMap - 140) +'px');

      //Move directional arrow to the printing area
      angular.element(document.querySelector('.ol-rotate')).css('left',(vm.widthMap - (vm.widthBackground/2) - 69)+'px');
      angular.element(document.querySelector('.ol-rotate')).css('top',(vm.heightMap - 180)+'px');

      //Add context to the map export (title, date, logo...)
      //move title to the middle
      // var widthTitle = angular.element('.exportMap.float.title').width();
      // angular.element('.exportMap.float.title').css('left',((vm.widthMap/2)-(widthTitle/2)) +'px');

      //move mapDetails to bottom left
      angular.element(document.querySelector('.exportMap.float.mapDetails')).css('left',(vm.widthBackground/2) + 'px');
      angular.element(document.querySelector('.exportMap.float.mapDetails')).css('top', (vm.heightMap - 75) + 'px'); //-Number: gives some padding from the bottom
      angular.element(document.querySelector('.exportMap.float.mapDetails'))[0].style.width = vm.ratioWidthA4 - 30 + 'px';

      //move logo ag to bottom right
      // var widthLogo = angular.element('.exportMap.float.logo').width();
      // //TODO: improve last value to be independable from width image (width logo: 100)
      // angular.element('.exportMap.float.logo').css('left',(vm.widthMap - (vm.widthBackground/2) - 100) + 'px');
      // angular.element('.exportMap.float.logo').css('top', vm.heightMap + 'px');

    };

    vm.changeFontSize = function(fontSize){
      vm.changeAllMemorialsText(fontSize);
    };

    vm.getTitle = function(){
      try{
        return angular.element(document.querySelector('#sitename_id')).text();
      }catch(e){
        return subdomain + " export";
      }
    };

    vm.cleanPopUps = function(){
      if("clicked-memorials" in personInteractionService.featureOverlays){
        personInteractionService.featureOverlays['clicked-memorials'].removeAllFeatures();
        markerService.removeMarkersByGroup('person');
        personInteractionService.detailsOnHoverEvent(true);
      }
    };
  }
]);
