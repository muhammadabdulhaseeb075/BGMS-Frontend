angular.module('bgmsApp.map').service('geometryHelperService', [function(){
  /*
    Helper Service to create geometries
  */

    var view_model = this;
    let rotate = null;
  
  
   /**
     * @function
   * @description
   * Creates an ol.geom.Multipolygon geometry centred at centre_coordinate
   * @param {string} polygon_shape - either 'rectangle' or 'circle'
   * @param {ol.Coordinate} centre_coordinate - centre of where the polygon should be located
   * @param {number} dim1 - first dimension eg width
   * @param {number} dim2_opt - second dimension eg height (optional)
   * @returns {ol.geom.MultiPolygon} the created polygon
     */
    view_model.createPolygonGeometry = function(polygon_shape, centre_coordinate, dim1, dim2_opt) {
  
      if(dim2_opt===undefined)
        dim2_opt = dim1;
      var polygon, multiPolygon = null;
      switch(polygon_shape){
        case 'rectangle':
          //create geometry with starting coordinate of [0,0], then translate it to 
            //the right location
          var point0 = [0,0];
          var point1 = [dim1, 0];
          var point2 = [dim1, dim2_opt];
          var point3 = [0, dim2_opt]
          polygon = new ol.geom.Polygon([[point0, point1, point2, point3, point0]]);
          var polygon_centre = polygon.getInteriorPoint().getFirstCoordinate();
          polygon.translate(centre_coordinate[0]-polygon_centre[0], centre_coordinate[1]-polygon_centre[1]);
          break;
        case 'circle':
          //create circle then convert it to polygon
          var circle = new ol.geom.Circle([centre_coordinate[0], centre_coordinate[1]], dim1);
          polygon = ol.geom.Polygon.fromCircle(circle);
          break;
        default:
          break;
      }
    if(polygon){
      multiPolygon = new ol.geom.MultiPolygon([polygon.getCoordinates()]);
    }
      return multiPolygon;
    };
    
    /**
     * @function
     * *description
     * Gets the rotation angle between two points by making the first point origin.
     * Rotation angle is angle-pi/2, to ensure it is rotating around the negative y axis 
     * @param {ol.Coordinate} origin - the coordinate to use as origin
     * @param {ol.Coordinate} anglePoint - point to calculate the angle to
     * @returns {number} angle between -3pi/2 to pi/2
     * 
     */
    view_model.getRotationAngle = function(origin, anglePoint){
        var translatedCoordinate = ol.coordinate.add([0,0], anglePoint);
        ol.coordinate.add(translatedCoordinate, [-origin[0], -origin[1]]);
        var angleRadians = Math.atan2(translatedCoordinate[1],translatedCoordinate[0]) - (Math.PI/2);
        return angleRadians;
    };
    
    /**
     * @function
     * @description
     * Transforms an array of input coordinates by rotating them about 
     * the origin by the specified angle. Corresponds to guidelines for
     * ol.TransformFunction
     * @param {ol.Coordinate} origin - origin about which coordinates should be rotated
     * @param {number} rotationAngle - angle by which coordinates should be rotated
     * @param {Array<number>} - input array of coordinates
     * @returns {Array<number>} array of rotated coordinates
     */
    view_model.rotateTransformFunction = function(origin, rotationAngle, inputArray){
      outputArray = inputArray;
      if(!isNaN(rotationAngle)){
        for (var j = 0, lenJ=inputArray.length; j < lenJ; j=j+2) 
            {
                //translate points to make centre as origin
          var coordinate = [inputArray[j], inputArray[j+1]];
                ol.coordinate.add(coordinate, [-origin[0], -origin[1]]);
                //rotate each coordinate
                ol.coordinate.rotate(coordinate, rotationAngle);
                //translate back to original location
                ol.coordinate.add(coordinate, origin);
                outputArray[j] = coordinate[0];
                outputArray[j+1] = coordinate[1];
            };      
      }
      return outputArray;
    };

  
    /**
   * @function
   * @description
   * Rotates an ol feature in place about it's centre using ol-rotate-feature
   * @param feature - feature to be rotated
    */
   view_model.rotateFeature = function(feature, angle) {
    if (!angle) angle = 0;

    view_model.rotate = new RotateFeatureInteraction({
        features: [feature],
        style: view_model.createStyle(),
        angle: angle
      });

      view_model.rotate.overlay_.setZIndex(Infinity);

      window.OLMap.addInteraction(view_model.rotate);
   }

   view_model.stopRotateFeature = function() {
    if (view_model.rotate) {
      window.OLMap.removeInteraction(view_model.rotate);
      view_model.rotate = null;
    }
   }

   view_model.createStyle = function() {
    var white = [ 255, 255, 255, 0.8 ]
    var blue = [ 0, 153, 255, 0.8 ]
    var red = [ 209, 0, 26, 0.9 ]
    var width = 4

    var styles = {
      anchor: [
        new ol.style.Style({
          image: new ol.style.RegularShape({
            fill: new ol.style.Fill({
              color: blue
            }),
            stroke: new ol.style.Stroke({
              color: blue,
              width: 1
            }),
            radius: 4,
            points: 6
          }),
          zIndex: Infinity
        })
      ],
      arrow: [
        new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: white,
            width: width + 5,
            lineDash: [ 12, 10 ]
          }),
          text: new ol.style.Text({
            font: '14px sans-serif',
            offsetX: 25,
            offsetY: -25,
            fill: new ol.style.Fill({
              color: 'blue'
            }),
            stroke: new ol.style.Stroke({
              color: white,
              width: width + 1
            })
          }),
          zIndex: Infinity
        }),
        new ol.style.Style({
          stroke: new ol.style.Stroke({
            color: red,
            width: width + 1,
            lineDash: [ 12, 10 ]
          }),
          zIndex: Infinity
        })
      ]
    }

    return function (feature, resolution) {
      var style
      var angle = feature.get('angle') || 0

      switch (true) {
        case feature.get('rotate-anchor'):
          style = styles[ 'anchor' ]
          style[ 0 ].getImage().setRotation(-angle)

          return style
        case feature.get('rotate-arrow'):
          style = styles[ 'arrow' ]

          var coordinates = feature.getGeometry().getCoordinates()
          // generate arrow polygon
          var geom = new ol.geom.LineString([
            coordinates,
            [ coordinates[ 0 ], coordinates[ 1 ] + 100 * resolution ]
          ])

          // and rotate it according to current angle
          geom.rotate(angle, coordinates)
          style[ 0 ].setGeometry(geom)
          style[ 1 ].setGeometry(geom)
          style[ 0 ].getText().setText(Math.round(-angle * 180 / Math.PI) + '°')

          return style
      }
    }
  }
   
//   view_model.translateGeometry = function(multipolygon_geometry, new_centre) {
//     var current_centre = multipolygon_geometry.getInteriorPoints().getFirstCoordinate();
//     multipolygon_geometry.translate(new_centre[0]-current_centre[0], new_centre[1]-current_centre[1]);
//     return 
//   };
   
   view_model.scaleGeometry = function(multipolygon_geometry, original_coordinates, angle_coordinate) {
     //to be implemented
   };

}]);