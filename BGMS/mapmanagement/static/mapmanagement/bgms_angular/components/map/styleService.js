angular.module('bgmsApp.map').service('styleService', ['offlineService', function(offlineService) {
  // most of this has been migrated into a vuex store

  var view_model = this;

  view_model.drawLayerStore = {};

  view_model.drawInteractionStyleFunction = function(feature, resolution) {
    if (!view_model.drawLayerStore['drawInteractionStyle']) {
      view_model.drawLayerStore['drawInteractionStyle'] = new ol.style.Style({
        fill: new ol.style.Fill({
          color: 'rgba(255, 255, 255, 0.2)'
        }),
        stroke: new ol.style.Stroke({
          color: 'rgba(0, 0, 0, 0.5)',
          lineDash: [10, 10],
          width: 2
        }),
        image: new ol.style.Circle({
          radius: 5,
          stroke: new ol.style.Stroke({
            color: 'rgba(0, 0, 0, 0.7)'
          }),
          fill: new ol.style.Fill({
            color: 'rgba(255, 255, 255, 0.2)'
          })
        })
      });
    }
    return [view_model.drawLayerStore['drawInteractionStyle']];
  };

  //text style for map export tool
  view_model.createTextStyle = function(feature_id, fontSize, outlineWidthp, color='black', align='center', placement='point') {
    var baseline = 'middle';
    var size = fontSize + 'px';
    var offsetX = 0;
    var offsetY = 0;
    var weight = 'bold';
    // var rotation = parseFloat(dom.rotation.value);
    var font = weight + ' ' + size + ' Verdana';
    // var fillColor = dom.color.value;
    var outlineColor = '#ffffff';
    var outlineWidth = typeof outlineWidthp !== 'undefined' ? outlineWidthp : 3;

    return new ol.style.Text({
      textAlign: align,
      textBaseline: baseline,
      font: font,
      text: feature_id,
      fill: new ol.style.Fill({
        color: color
      }),
      stroke: new ol.style.Stroke({
        color: outlineColor,
        width: outlineWidth
      }),
      offsetX: offsetX,
      offsetY: offsetY,
      // rotation: rotation,
      overflow: true,
      placement: placement
    });
  };
}]);
