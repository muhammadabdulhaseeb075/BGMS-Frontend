import layersStore from '@/mapmanagement/store/modules/MapLayers';
import angularMapControllerStore from '@/mapmanagement/store/modules/AngularMapController';
import Text from 'ol/style/Text';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import Style from 'ol/style/Style';
import Icon from 'ol/style/Icon';

// TODO migrate contents of memorialService.js to here with corresponding vuex store

/*export default class Memorial {
}*/


export enum VISUALISATIONENUM {"image" = 1, "graveLink" = 2,"gravenumber"=3}

/**
 * Display which memorials have no images
 */
export function showMemorialIndicators(type) {
  const allLayers = (window as any).OLMap.getLayers().getArray();
  console.log(allLayers)
  let memorialLayers = [];
  console.log(memorialLayers)
  for (var i = 0; i < allLayers.length; i++) {
    if(allLayers[i].get('groupName') === "memorials") {
      memorialLayers.push(allLayers[i]);
    }
  }

  for (let i = 0; i < memorialLayers.length; i++) {

    const layerName = memorialLayers[i].get('name');
    console.log(layerName)
    const style = getLayerStyle(layerName);
    const fill = style.fill;
    const stroke = style.stroke;

    // Get all the memorials in the layer
    const memorials = memorialLayers[i].getSource().getFeatures();
    console.log(memorials)
    for (let j = 0; j < memorials.length; j++) {
      showMemorialIndicatorForSingleMemorial(type, memorials[j], layerName, fill, stroke);
    }
  }
}

/**
 * Retrun object containing fill and stroke styles for given layer
 * @param layerName
 */
function getLayerStyle(layerName): {fill, stroke} {
  let fill, stroke, styleLayer;

  // Get the layer style, fill color and stroke color
  if (layerName != 'memorials_bench') {
    if (typeof layersStore.state.layerStyles[layerName] === "function") {
      styleLayer = layersStore.state.layerStyles[layerName]()[0];
    } else {
      styleLayer = layersStore.state.layerStyles['default']()[0];
    }

    fill = styleLayer.getFill();
    stroke = styleLayer.getStroke();
  }

  return { fill: fill, stroke: stroke };
}

export function showMemorialIndicatorForSingleMemorial(type, memorial, layerName, fill=null, stroke=null) {

  if (!fill || !stroke) {
    const style = getLayerStyle(layerName);
    fill = style.fill;
    stroke = style.stroke;
  }

  let check = false;

  if (type === VISUALISATIONENUM.image)
    // Determine if the memorial has any images
    check = memorial.get('images_count') > 0;
  else if (type === VISUALISATIONENUM.graveLink)
    // Determine if the memorial has any links to graves
    check = memorial.get('linked_graves_count');
    else if (type === VISUALISATIONENUM.gravenumber)
    // Determine if the memorial has any links to graves
    check = memorial.get('grave_number');

  // Set text and colour
  let text = '';
  let textColor = '';
  if(check) {
    text = '\uf00c'; //FontAwesome 'check'
    textColor = 'rgb(0, 140, 0)';
  } else {
    text = '\uf00d'; //FontAwesome 'cross'
    textColor = 'rgb(255, 0, 0)';
  }

  // Override the layer style
  if (layerName == 'memorials_bench') {
    // Passes a ol.StyleFunction (a function which OpenLayers runs every time the
    // zoom level changes) as the bench icon needs to resize when zooming in/out
    memorial.setStyle(createMemorialBenchImageOverlay(type, false, memorial));
  } else {
    memorial.setStyle(createMemorialImageOverlay(fill, stroke, text, textColor, 10));
  }
}

// TODO: Is there any way to stop this duplication of code?
export function createMemorialBenchImageOverlay(type, selectedIcon, memorial) {

  let feature_geom = memorial.getGeometry();

  if (feature_geom.getType() === 'MultiPolygon') {
    feature_geom = feature_geom.getInteriorPoints();
  }
  
  let check = false;

  if (type === VISUALISATIONENUM.image)
    // Determine if the memorial has any images
    check = memorial.get('images_count') > 0;
  else if (type === VISUALISATIONENUM.graveLink)
    // Determine if the memorial has any links to graves
    check = memorial.get('linked_graves_count');
    else if (type === VISUALISATIONENUM.gravenumber)
    // Determine if the memorial has any links to graves
    check = memorial.get('grave_number');


  // Set text and colour
  let text;

  if(selectedIcon) {
    text = new Text({
      text: '\uf3c5',
      font: '900 24px "Font Awesome 5 Free"',
      fill: new Fill({
        color: 'rgb(255, 0, 0)',
      }),
      stroke: new Stroke({
        color: 'rgb(255, 244, 230)',
        width: 2,
      }),
      overflow: true
    })
  }
  else {
    let textValue;
    let textColor;
    if (check) {
      textValue = '\uf00c'; //FontAwesome 'check'
      textColor = 'rgb(0, 140, 0)';
    } else {
      textValue = '\uf00d'; //FontAwesome 'cross'
      textColor = 'rgb(255, 0, 0)';
    }

    text = new Text({
      text: textValue,
      font: '900 10px "Font Awesome 5 Free"',
      fill: new Fill({
        color: textColor,
      }),
      stroke: new Stroke({
        color: 'white',
        width: 3,
      }),
    });
  }

  var returnStyle = new Style({
    image: new Icon({
      opacity: 1,
      src: require('@/mapmanagement/static/images/layers/Memorial-Bench.png'),
      crossOrigin: location.hostname,
    }),
    geometry: feature_geom,
    text: text
  });

  if (selectedIcon)
    returnStyle.setZIndex(2000);

  return [new Style({
      stroke: new Stroke({
        color: 'rgba(47, 74, 118, 1)',
        width: 2,
        lineDash: [10, 10],
      })
    }),
    returnStyle];
}

/**
 * Removes the image visualisation
 */
export function hideMemorialIndicators() {
  const allLayers = (window as any).OLMap.getLayers().getArray();
  let memorialLayers = [];

  for (let i = 0; i < allLayers.length; i++) {
    if(allLayers[i].get('groupName') === "memorials") {
      memorialLayers.push(allLayers[i]);
    }
  }

  for (let i = 0; i < memorialLayers.length; i++) {
    let memorials = memorialLayers[i].getSource().getFeatures();

    for (var j = 0; j < memorials.length; j++) {
      // Because the visualisation is applied directly to the memorial, setting
      // the style to undefined causes it to fall back to the layer style
      memorials[j].setStyle(undefined);
    }
  }
}

/**
 * The overlay for memorials with/without images
 */
function createMemorialImageOverlay(fill, stroke, text, textColor, fontSize) {
  const style = new Style({
    stroke: stroke,
    fill: fill,
    text: new Text({
      text: text,
      font: '900 ' + fontSize + 'px "Font Awesome 5 Free"',
      fill: new Fill({
        color: textColor,
      }),
      stroke: new Stroke({
        color: 'white',
        width: 3,
      }),
      overflow: true
    }),
  });

  return [style];
}

// 
export function showGraveNumber(type) {
  const allLayers = (window as any).OLMap.getLayers().getArray();
  let memorialLayers = [];
  console.log(memorialLayers)
  for (var i = 0; i < allLayers.length; i++) {
    if(allLayers[i].get('grave_number')) { //using just grave_number produces an empty array on console so switch to default
      memorialLayers.push(allLayers[i]); // appends to memorialLayers
    }
  }

  for (let i = 0; i < memorialLayers.length; i++) {

    const layerName = memorialLayers[i].get('grave_number');
    console.log(layerName)
    const style = getLayerStyle(layerName);
    const fill = style.fill;
    const stroke = style.stroke;

    // Get all the memorials in the layer
    const memorials = memorialLayers[i].getSource().getFeatures();

    for (let j = 0; j < memorials.length; j++) {
      const memorial = memorials[j];
      showMemorialIndicatorForSingleMemorial(type, memorial[j], layerName, fill, stroke);
    }
  }
}
