import Circle from 'ol/style/Circle';
import Fill from 'ol/style/Fill';
import Icon from 'ol/style/Icon';
import Stroke from 'ol/style/Stroke';
import Style from 'ol/style/Style';
import Text from 'ol/style/Text';
import GeoJSON from 'ol/format/GeoJSON';

/**
 * Defines styles for all layers
 * 
 * Note: the OpenLayers angular directive is looking for styles as a function.
 * But for most objects, we do not want to create a new style object each time.
 * Hence, save a style and return it to OpenLayers in a function.
 * 
 * Note: patterns make this tricky as they need to be loaded async.
 */
export default class LayerStyles {

  /******** Cluster layer ********/
  private clusterMemorialStore = {};
  cluster = (feature) => { 
    /*
    	size string can be: '8x8', '16x16', '24x24', '32x32', '48x48', '64x64'
    */
    var size = feature.get('features').length;
    var source, textSize = 1;
    if (size === 1) {
      source = require('@/mapmanagement/static/images/layers/gravestone_8x8.png');
      // textSize = 0;
    } else if (size < 10) {
      source = require('@/mapmanagement/static/images/layers/gravestone_16x16.png');
      // textSize = 10;
    } else if (size < 100) {
      source = require('@/mapmanagement/static/images/layers/gravestone_24x24.png');
      // textSize = 12;
    } else if (size < 1000) {
      source = require('@/mapmanagement/static/images/layers/gravestone_32x32.png');
      // textSize = 14;
    } else {
      source = require('@/mapmanagement/static/images/layers/gravestone_48x48.png');
      // textSize = 14;
    }

    let style = this.clusterMemorialStore[size.toString()];
    if (!style) {
      this.clusterMemorialStore[size.toString()] = new Style({
        image: new Icon({
          opacity: 1,
          src: source,
          crossOrigin: location.hostname,
        }),
        text: new Text({
          text: size.toString(),
          scale: textSize,
          fill: new Fill({
            color: '#000000'
          })
        })
      });
    }
    return [this.clusterMemorialStore[size.toString()]];
  }


  /******** Memorial layers ********/
  private defaultStyle: Style[] = this.polygonStyleFunction('#319FD3', 'rgba(224, 239, 253, 0.4)', 1.5);
  default = () => { return this.defaultStyle; }

  private gravestoneStyle: Style[] = this.polygonStyleFunction('rgba(41, 88, 237, 0.7)', 'rgba(41, 88, 237, 0.7)');
  gravestone = () => { return this.gravestoneStyle; }

  private plaqueStyle: Style[] = this.polygonStyleFunction('rgba(128, 125, 104, 1)', '#FFC64B', 1);
  plaque = () => { return this.plaqueStyle; }

  private statueStyle: Style[] = this.polygonStyleFunction('rgba(0, 0, 0, 0.44)', 'rgba(255, 255, 255,1)');
  statue = () => { return this.statueStyle; }
  
  private stone_vaseStyle: Style[] = this.polygonStyleFunction('rgb(127, 127, 127)', 'rgba(108, 165, 35,1)', 2);
  stone_vase = () => { return this.stone_vaseStyle; }
  
  private obeliskStyle: Style[] = this.polygonStyleFunction('rgba(0, 0, 0, 0.44)', 'rgba(255, 255, 255,1)');
  obelisk = () => { return this.obeliskStyle; }
  
  private pavestoneStyle: Style[] = this.polygonStyleFunction('rgba(31, 25, 9, 0)', 'rgba(31, 25, 9, 0.4)');
  pavestone = () => { return this.pavestoneStyle; }
  
  private table_tombStyle: Style[] = this.polygonStyleFunction('#417bbd', '#417bbd');
  table_tomb = () => { return this.table_tombStyle; }
  
  private chest_tombStyle: Style[] = this.polygonStyleFunction('rgb(32,52,84)', 'rgb(32,52,84)');
  chest_tomb = () => { return this.chest_tombStyle; }
  
  private crossStyle: Style[] = this.polygonStyleFunction('#91908e', '#614126', 1.5);
  cross = () => { return this.crossStyle; }
  
  private grave_slabStyle: Style[] = this.polygonStyleFunction('rgb(199, 166, 126)', 'rgb(199, 166, 126)');
  grave_slab = () => { return this.grave_slabStyle; }
  
  private windowStyle: Style[] = this.polygonStyleFunction('rgba(181, 0, 180, 0.8)', 'rgba(181, 0, 180, 0.4)');
  window = () => { return this.windowStyle; }
  
  private war_graveStyle: Style[] = this.polygonStyleFunction('rgb(182, 7, 7)', 'rgba(255, 255, 255,1)');
  war_grave = () => { return this.war_graveStyle; }
  
  private war_memorialStyle: Style[] = this.polygonStyleFunction('rgb(242, 160, 36)', 'rgba(255, 255, 255,1)');
  war_memorial = () => { return this.war_memorialStyle; }
  
  private coffin_tombStyle: Style[] = this.polygonStyleFunction('rgba(41, 88, 237, 0.4)', 'rgba(227, 125, 19, 0.7)');
  coffin_tomb = () => { return this.coffin_tombStyle; }
  
  private memorials_lych_gateStyle: Style[] = this.polygonStyleFunction('rgb(135, 159, 228)', 'rgb(204, 153, 255)');
  memorials_lych_gate = () => { return this.memorials_lych_gateStyle; }
  
  private memorial_treeStyle: Style[] = this.polygonStyleFunction('#614126', 'rgba(242, 160, 36, 0.7)', 2);
  memorial_tree = () => { return this.memorial_treeStyle; }
  
  private memorial_bush_shrubStyle: Style[] = this.polygonStyleFunction('rgb(112, 146, 68)', 'rgba(112, 146, 68, 1)', 1.5);
  memorial_bush_shrub = () => { return this.memorial_bush_shrubStyle; }
  
  private grave_kerbStyle: Style[] = this.polygonStyleFunction('#91908e', 'rgba(0, 0, 0, 0)', 1.5);
  grave_kerb = () => { return this.grave_kerbStyle; }
  
  private gravestone_with_kerbStyle: Style[] = this.polygonStyleFunction('#91908e', 'rgba(65, 123, 189, 0.4)', 1.5);
  gravestone_with_kerb = () => { return this.gravestone_with_kerbStyle; }
  
  private kerb_with_crossStyle: Style[] = this.polygonStyleFunction('#91908e', '#cc6600', 1.5);
  kerb_with_cross = () => { return this.kerb_with_crossStyle; }
  
  private plaque_with_kerbStyle: Style[] = this.polygonStyleFunction('#91908e', 'rgba(248, 155, 62, 0.4)', 1.5);
  plaque_with_kerb = () => { return this.plaque_with_kerbStyle; }

  memorials_bench = (feature, resolution, feature_id, fontSize) => {
    var feature_geom = feature.getGeometry();
    var scale = this.getScale(resolution);
    var textFeature: any = '';
    if (feature_geom.getType() === 'MultiPolygon') {
      feature_geom = feature_geom.getInteriorPoints();
    }
    if (feature_id !== undefined && fontSize !== undefined) {
      textFeature = this.createTextMemorialBenchStyle(feature_id, fontSize);
    }
    return [
      new Style({
        stroke: new Stroke({
          color: 'rgba(47, 74, 118, 1)',
          width: 2,
          lineDash: [10, 10],
        })
      }),
      new Style({
        image: new Icon({
          opacity: 1,
          src: require('@/mapmanagement/static/images/layers/Memorial-Bench.png'),
          scale: scale,
          crossOrigin: location.hostname,
        }),
        geometry: feature_geom,
        text: textFeature,
      })
    ];
  }

  private unmarked_graveResolution: number = 0;
  private unmarked_graveStyle: Style[] = null;
  unmarked_grave = (feature, resolution) => {

    // only update if resolution has changed
    if (resolution != this.unmarked_graveResolution) {
      var dash = [4,4];
      if (resolution >= 0.14)
        dash = [3,3];
      this.unmarked_graveStyle = this.lineDashStyleFunction('#5e6163', 'rgba(0, 0, 0, 0)', 1.5, dash);
      this.unmarked_graveResolution = resolution;
    }

    return this.unmarked_graveStyle;
  };
  
  private catacombStyle: Style[] = this.polygonStyleFunction('rgb(255, 255, 255)', '#91908e', 1.5);
  catacomb = () => { return this.catacombStyle; }


  /******** Natural Surface layers ********/
  private grassStyle: Style[] = null;
  grass = () => { return this.grassStyle; }

  private plantingStyle: Style[] = this.polygonStyleFunction('#765632', '#e0c89b', 0.7);
  planting = () => { return this.plantingStyle; }
  
  private shrublandStyle: Style[] = null;
  shrubland = () => { return this.shrublandStyle; }
  
  private woodlandStyle: Style[] = null;
  woodland = () => { return this.woodlandStyle; }
  
  private waterStyle: Style[] = this.polygonStyleFunction('#bdd7ff', '#bdd7ff');
  water = () => { return this.waterStyle; }
  
  private streamStyle: Style[] = this.polygonStyleFunction('#b3b3b3','#bdd7ff');
  stream = () => { return this.streamStyle; }
  
  private recreationStyle: Style[] = this.polygonStyleFunction('white','#dc7e41');
  recreation = () => { return this.recreationStyle; }
  
  private other_surfaceStyle: Style[] = this.polygonStyleFunction('#92b79f', '#92b79f');
  other_surface = () => { return this.other_surfaceStyle; }


  /******** Plot layers ********/
  private available_plotResolution: number = 0;
  private available_plotStyle: Style[] = null;
  available_plot = (feature, resolution) => {

    // only update if resolution has changed
    if (resolution != this.available_plotResolution) {
      let dash = [6,4];
      let lineWidth = 2;
      if (resolution >= 0.14) {
        lineWidth = 1.5;
        dash = [4,2.5];
      }
      this.available_plotStyle = this.lineDashStyleFunction('#33CC33', 'rgba(224, 255, 207, 0)', lineWidth, dash);
      this.available_plotResolution = resolution;
    }

    return this.available_plotStyle;
  };
  
  private pet_graveResolution: number = 0;
  private pet_graveStyle: Style[] = null;
  pet_grave = (feature, resolution) => {

    // only update if resolution has changed
    if (resolution != this.pet_graveResolution) {
      let dash = [6,4];
      let lineWidth = 2;
      if (resolution >= 0.14) {
        lineWidth = 1.5;
        dash = [4,2.5];
      }
      this.pet_graveStyle = this.lineDashStyleFunction('#673AB7', 'rgba(224, 255, 207, 0)', lineWidth, dash);
      this.pet_graveResolution = resolution;
    }

    return this.pet_graveStyle;
  };
  
  private plotResolution: number = 0;
  private plotStyle: Style[] = null;
  plot = (feature, resolution) => {

    // only update if resolution has changed
    if (resolution != this.plotResolution) {
      let dash = [2,4];
      if (resolution >= 0.14) {
        dash = [1,3];
      }
      this.plotStyle = this.lineDashStyleFunction('#5e6163', 'rgba(224, 239, 253, 0)', 1, dash);
      this.plotResolution = resolution;
    }

    return this.plotStyle;
  };
  
  private reserved_plotResolution: number = 0;
  private reserved_plotStyle: Style[] = null;
  reserved_plot = (feature, resolution) => {

    // only update if resolution has changed
    if (resolution != this.reserved_plotResolution) {
      let dash = [6,4];
      let lineWidth = 2;
      if (resolution >= 0.14) {
        lineWidth = 1.5;
        dash = [4,2.5];
      }
      this.reserved_plotStyle = this.lineDashStyleFunction('#EE592A', 'rgba(253, 241, 240, 0)', lineWidth, dash);
      this.reserved_plotResolution = resolution;
    }

    return this.reserved_plotStyle;
  };


  /******** Natural Surface layers ********/
  private tree_canopyStyle: Style[] = null;
  get tree_canopy() {
    if (this.tree_canopyStyle)
      return this.tree_canopyStyle;
    else {
      return new Promise((resolve, reject) => {
        this.makePattern(require('@/mapmanagement/static/images/layers/canopy.png'), 0.7)
        .then(result => {
          this.tree_canopyStyle = this.polygonStylePattern('rgba(143, 178, 107, 1)', 0.7, result);
          resolve(this.tree_canopyStyle);
        });
      });
    }
  }

  private treeHighlighted: boolean = false;
  private treeStyles = {};
  tree = (feature, resolution, highlighted=false) => {

    // only want to create tree layers once. So store in object.
    let treeStyle = this.treeStyles[feature.getId()];
    if (!treeStyle || treeStyle.highlighted!==highlighted) {
      var feature_geom = feature.getGeometry();
      if (feature_geom.getType() === 'Point') {
        feature_geom = feature_geom.getCoordinates();
        var geojsonFormatter = new GeoJSON();
        var geometry = geojsonFormatter.readGeometry(this.tree_polygon);
        var centre = feature_geom.getInteriorPoint().getFirstCoordinate();
        let transform = (input) => {
          this.scaleTransformFunction(centre, feature.getProperties().veg_spread, input);
        }
        feature_geom.applyTransform(transform);
        geometry.translate(feature_geom[0] - centre[0], feature_geom[1] - centre[1]);
      }

      treeStyle = { highlighted: highlighted }

      treeStyle['style'] = [ new Style({
        image: new Icon({
          opacity: 1,
          src: require('@/mapmanagement/static/images/layers/tree_320x320.png'),
          crossOrigin: location.hostname,
        }),
        geometry: geometry,
        fill: new Fill({
          color: highlighted ? this.hightlightFill : 'rgba(169,218,116,0.7)'
        }),
        stroke: new Stroke({
          color: highlighted ? this.hightlightStroke : 'rgba(143, 178, 107, 1)',
          width: 0.7
        })
      }) ];

      this.treeStyles[feature.getId()] = treeStyle;
    }
    
    return treeStyle.style ? treeStyle.style : null;
  };

  private bushHighlighted: boolean = false;
  private bushStyles = {};
  private bushPattern = null;
  bush = (feature, resolution, highlighted=false) => {

    // only want to create bush layers once. So store in object.
    let bushStyle = this.bushStyles[feature.getId()];
    if ((!bushStyle || bushStyle.highlighted!==highlighted) && this.bushPattern) {
      var feature_geom = feature.getGeometry();
      if (feature_geom.getType() === 'Point') {
        feature_geom = feature_geom.getCoordinates();
        var geojsonFormatter = new GeoJSON();
        var geometry = geojsonFormatter.readGeometry(this.bush_polygon);
        var centre = feature_geom.getInteriorPoint().getFirstCoordinate();
        let transform = (input) => {
          this.scaleTransformFunction(centre, feature.getProperties().veg_spread, input);
        }
        feature_geom.applyTransform(transform);
        geometry.translate(feature_geom[0] - centre[0], feature_geom[1] - centre[1]);
      }

      bushStyle = { highlighted: highlighted }

      bushStyle['style'] = [ new Style({
        geometry: geometry,
        fill: new Fill({
          color: highlighted ? this.hightlightFill : this.bushPattern
        }),
        stroke: new Stroke({
          color: highlighted ? this.hightlightStroke : 'rgba(108, 165, 35, 1)',
          width: 0.7
        })
      }) ];

      this.bushStyles[feature.getId()] = bushStyle;
    }
    
    return bushStyle.style ? bushStyle.style : null;
  }

  private treeTrunkResolution: number = 0;
  private treeTrunkHighlighted: boolean = false;
  private treeTrunkStyles = {};
  // Note: trunk is circle polygon and tree_trunk is point with a veg_spread
  tree_trunk = (feature, resolution, highlighted=false) => {

    // reset styles whenever the res changes
    if (this.treeTrunkResolution != resolution) {
      this.treeTrunkStyles = {};
      this.treeTrunkResolution = resolution;
    }

    // only want to create tree trunk layers once. So store in object.
    let treeTrunkStyle = this.treeTrunkStyles[feature.getId()];
    if (!treeTrunkStyle || treeTrunkStyle.highlighted!==highlighted) {
      
      treeTrunkStyle = { highlighted: highlighted }

      // default veg spread of 750
      const vegSpread = feature.get('veg_spread') ? feature.get('veg_spread') : 750;

      treeTrunkStyle['style'] = [ new Style({
        image: new Circle({
          radius: vegSpread / resolution / 1000 / 2 / 3.14,
          fill: new Fill({
            color: highlighted ? this.hightlightFill : '#926239'
          }),
          stroke: new Stroke({
            color: highlighted ? this.hightlightStroke : '#614126',
            width: 2
          })
        })
      }) ];
      this.treeTrunkStyles[feature.getId()] = treeTrunkStyle;
    }
  
    return treeTrunkStyle.style ? treeTrunkStyle.style : null;
  }
  
  private trunkStyle: Style[] = this.polygonStyleFunction('#614126', '#926239', 2);
  trunk = () => { return this.trunkStyle; }


  /******** Furniture layers ********/
  private benchResolution: number = 0;
  private benchStyles = {};
  bench = (feature, resolution) => {

    // reset styles whenever the res changes
    if (this.benchResolution != resolution) {
      this.benchStyles = {};
      this.benchResolution = resolution;
    }

    // only want to create tree trunk layers once. So store in object.
    let benchStyle = this.benchStyles[feature.getId()];
    if (!benchStyle) {

      let feature_geom = feature.getGeometry();
      if (feature_geom.getType() === 'MultiPolygon') {
        feature_geom = feature_geom.getInteriorPoints();
      } else
        return null;
      const scale = this.getScale(resolution);
      benchStyle = [
        new Style({
          stroke: new Stroke({
            color: 'rgba(47, 74, 118, 1)',
            width: 2,
            lineDash: [10, 10],
          })
        }),
        new Style({
          image: new Icon({
            opacity: 1,
            src: require('@/mapmanagement/static/images/layers/Bench-16.png'),
            crossOrigin: location.hostname,
            scale: scale
          }),
          geometry: feature_geom
        })
      ];
    }

    return benchStyle;
  }

  private binStyle: Style[] = this.polygonStyleFunction('black', 'grey');
  bin = () => { return this.binStyle; }

  private bollardStyle: Style[] = this.polygonStyleFunction('black', 'grey');
  bollard = () => { return this.bollardStyle; }

  private signStyle: Style[] = this.polygonStyleFunction('white', 'black');
  sign = () => { return this.signStyle; }

  private lamppostStyle: Style[] = this.polygonStyleFunction('white','#3e4346');
  lamppost = () => { return this.lamppostStyle; }

  private sundialStyle: Style[] = this.polygonStyleFunction('rgb(255, 191, 0)','rgb(255, 191, 0)');
  sundial = () => { return this.sundialStyle; }


  /******** Utilities layers ********/
  private manholeStyle: Style[] = this.polygonStyleFunction('rgba(90, 98, 78, 1)', 'rgba(90, 98, 78, 0.4)');
  manhole = () => { return this.manholeStyle; }

  private inspection_coverStyle: Style[] = this.polygonStyleFunction('rgba(90, 98, 55, 1)', 'rgba(90, 98, 55, 0.4)');
  inspection_cover = () => { return this.inspection_coverStyle; }
  
  private utility_poleStyle: Style[] = this.polygonStyleFunction('#8a663a', '#8a663a');
  utility_pole = () => { return this.utility_poleStyle; }
  
  private gullyStyle: Style[] = this.polygonStyleFunction('#72c1b6', '#72c1b6');
  gully = () => { return this.gullyStyle; }
  
  private stileStyle: Style[] = this.polygonStyleFunction('#FF5722', '#FF5722', 2);
  stile = () => { return this.stileStyle; }
  
  private tapResolution: number = 0;
  private tapHighlighted: boolean = false;
  private tapStyle: Style[] = null;
  tap = (feature, resolution, highlighted) => {

    // only update if resolution or highlighted has changed
    if (resolution != this.tapResolution || this.tapHighlighted !== highlighted) {
      const scale = this.getScale(resolution);

      let image = new Icon({
        opacity: 1,
        src: require('@/mapmanagement/static/images/layers/tap.png'),
        crossOrigin: location.hostname,
        scale: scale
      });

      if (highlighted) {
        image = new Icon({
          opacity: 1,
          src: require('@/mapmanagement/static/images/layers/tap.png'),
          crossOrigin: location.hostname,
          scale: scale,
          color: this.hightlightFill
        });
      }

      this.tapStyle = [ new Style({ image: image }) ];
      this.tapResolution = resolution;
      this.tapHighlighted = highlighted;
    }

    return this.tapStyle;
  };
  
  private waterTroughResolution: number = 0;
  private waterTroughHighlighted: boolean = false;
  private waterTroughStyle: Style[] = null;
  water_trough = (feature, resolution, highlighted) => {

    // only update if resolution or highlighted has changed
    if (resolution != this.waterTroughResolution || this.waterTroughHighlighted !== highlighted) {
      const scale = this.getScale(resolution);

      this.tapStyle = [
        new Style({
          image: new Icon({
            opacity: 1,
            color: highlighted ? this.hightlightFill :  '#2196F3',
            src: require('@/mapmanagement/static/images/layers/tap.png'),
            crossOrigin: location.hostname,
            scale: scale
          })
        })
      ];
      this.waterTroughResolution = resolution;
      this.waterTroughHighlighted = highlighted;
    }

    return this.tapStyle;
  };


  /******** Divides layers ********/
  private wallStyle: Style[] = this.polygonStyleFunction('#948f8a', '#948f8a', 2);
  wall = () => { return this.wallStyle; }

  private assumed_wallStyle: Style[] = this.lineDashStyleFunction('#948f8a', '#948f8a', 2, [5]);
  assumed_wall = () => { return this.assumed_wallStyle; }

  private hedgeStyle: Style[] = null;
  get hedge() {
    if (this.hedgeStyle)
      return this.hedgeStyle;
    else {
      return new Promise((resolve, reject) => {
        this.makePattern(require('@/mapmanagement/static/images/layers/hedge.png'), 1)
        .then(result => {
          this.hedgeStyle = this.polygonStylePattern('rgba(108, 165, 35, 1)', 0.7, result);
          resolve(this.hedgeStyle);
        });
      });
    }
  }

  private assumed_hedgeStyle: Style[] = null;
  get assumed_hedge() {
    if (this.assumed_hedgeStyle)
      return this.assumed_hedgeStyle;
    else {
      return new Promise((resolve, reject) => {
        this.makePattern(require('@/mapmanagement/static/images/layers/hedge.png'), 0.7)
        .then(result => {
          this.assumed_hedgeStyle = this.polygonStylePatternDash('rgba(108, 165, 35, 1)', 0.7, result, [5]);
          resolve(this.assumed_hedgeStyle);
        });
      });
    }
  }
  
  private assumed_fenceStyle: Style[] = this.lineDashStyleFunction('rgba(85, 52, 0, 1)', 'rgba(85, 52, 0, 0.4)', 2, [5]);
  assumed_fence = () => { return this.assumed_fenceStyle; }
  
  private fenceStyle: Style[] = this.lineDashStyleFunction('rgba(85, 52, 0, 1)', 'rgba(85, 52, 0, 0.4)', 2, [8]);
  fence = () => { return this.fenceStyle; }
  
  private gateStyle: Style[] = this.polygonStyleFunction('#936951', '#936951', 2);
  gate = () => { return this.gateStyle; }
  
  private handrailStyle: Style[] = this.polygonStyleFunction('#9C27B0', '#9C27B0', 2);
  handrail = () => { return this.handrailStyle; }
  
  private kerbStyle: Style[] = this.polygonStyleFunction('#91908e', 'rgba(0, 0, 0, 0)', 1.5);
  kerb = () => { return this.kerbStyle; }


  /******** Thoroughfares layers ********/
  private pathStyle: Style[] = null;
  path = () => { return this.pathStyle; }
  
  private roadStyle: Style[] = this.polygonStyleFunction('#c7c07d', 'rgb(227, 214, 120)');
  road = () => { return this.roadStyle; }
  
  private car_parkStyle: Style[] = null;
  get car_park() {
    if (this.car_parkStyle)
      return this.car_parkStyle;
    else {
      return new Promise((resolve, reject) => {
        this.makePattern(require('@/mapmanagement/static/images/layers/carpark.png'), 1)
        .then(result => {
          this.car_parkStyle = this.polygonStylePattern('rgba(143, 178, 107, 1)', 2, result);
          resolve(this.car_parkStyle);
        });
      });
    }
  }
  
  private bridgeStyle: Style[] = this.polygonStyleFunction('rgb(102, 51, 0)', 'rgb(102, 51, 0)');
  bridge = () => { return this.bridgeStyle; }


  /******** Buildings layers ********/
  private buildingResolution: number = 0;
  private buildingStyles = {};
  building = (feature, resolution) => {

    // reset styles whenever the res changes
    if (this.buildingResolution != resolution) {
      this.buildingStyles = {};
      this.buildingResolution = resolution;
    }

    // only want to create tree trunk layers once. So store in object.
    let buildingStyle = this.buildingStyles[feature.getId()];
    if (!buildingStyle) {
      buildingStyle = this.polygonStyleTextFunction('#7B7268', '#D3CDC6', 2, resolution, feature.get('label'));
      this.buildingStyles[feature.getId()] = buildingStyle;
    }

    return buildingStyle;
  }
  
  private tankStyle: Style[] = this.polygonStyleFunction('#eed737', '#7f6f05');
  tank = () => { return this.tankStyle; }
  
  private stepsStyle: Style[] = this.polygonStyleFunction('#727170', '#c2c5c9');
  steps = () => { return this.stepsStyle; }
  
  private lych_gateStyle: Style[] = this.polygonStyleFunction('rgb(135, 159, 228)', '#DCD8D8');
  lych_gate = () => { return this.lych_gateStyle; }
  
  private temp_styleStyle: Style[] = this.polygonStyleFunction('rgb(135, 159, 228)', '#DCD8D8');
  temp_style = () => { return this.temp_styleStyle; }
  
  private mausoleumStyle: Style[] = this.polygonStyleFunction('#f9f19d','#D3CDC6');
  mausoleum = () => { return this.mausoleumStyle; }


  /******** Administration layers ********/
  private microchipStyle: Style[] = [ new Style({
    image: new Circle({
      radius: 1,
      fill: new Fill({ color: '#F41818' })
    })
  }) ];
  microchip = () => { return this.microchipStyle; }
  
  private siteBoundaryResolution: number = 0;
  private siteBoundaryStyle: Style[] = null;
  site_boundary = (feature, resolution) => {

    // only update if resolution has changed
    if (resolution != this.siteBoundaryResolution) {
      if (resolution <= 0.07)
        this.siteBoundaryStyle = this.polygonStyleFunction('rgba(116,67,67, .3)', 'rgba(47, 74, 118, 0)', 12);
      if (resolution <= 0.28)
        this.siteBoundaryStyle = this.polygonStyleFunction('rgba(116,67,67, .3)', 'rgba(47, 74, 118, 0)', 8);
      else
        this.siteBoundaryStyle = this.polygonStyleFunction('rgba(116,67,67, .3)', 'rgba(47, 74, 118, 0)', 4);

      this.siteBoundaryResolution = resolution;
    }

    return this.siteBoundaryStyle;
  };
  
  private gridResolution: number = 0;
  private gridStyles = {};
  grid = (feature, resolution) => {

    // reset styles whenever the res changes
    if (this.gridResolution != resolution) {
      this.gridStyles = {};
      this.gridResolution = resolution;
    }

    // only want to create tree trunk layers once. So store in object.
    let gridStyle = this.gridStyles[feature.getId()];
    if (!gridStyle) {
      let textSize = 12;
      if (resolution >= 0.28)
        textSize = 0;
      else if (resolution >= 0.14)
        textSize = 8;
        let size = textSize + 'px';
        let weight = 'bold';
        let font = weight + ' ' + size + ' Verdana';

        gridStyle = [ new Style({
        fill: new Fill({
          color: 'rgba(85, 45, 0, 0.2)'
        }),
        stroke: new Stroke({
          color: '#765632',
          width: 1
        }),
        text: new Text({
          text: feature.get('label'),
          font: font,
          fill: new Fill({
            color: '#fff'
          })
        })
      }) ];

      this.gridStyles[feature.getId()] = gridStyle;
    }

    return gridStyle;
  }
  
  private sectionResolution: number = 0;
  private sectionStyles = {};
  section = (feature, resolution) => {

    // reset styles whenever the res changes
    if (this.sectionResolution != resolution) {
      this.sectionStyles = {};
      this.sectionResolution = resolution;
    }

    // only want to create layers once. So store in object.
    let sectionStyle = this.sectionStyles[feature.getId()];
    if (!sectionStyle) {
      sectionStyle = this.polygonStyleTextFunction('rgb(203, 15, 1)', 'rgba(203, 15, 1, 0.1)', 1.5, resolution, feature.get('label'), 'rgb(203, 15, 1)', 0.7);
      this.sectionStyles[feature.getId()] = sectionStyle;
    }

    return sectionStyle;
  }
  
  private subsectionResolution: number = 0;
  private subsectionStyles = {};
  subsection = (feature, resolution) => {

    // reset styles whenever the res changes
    if (this.subsectionResolution != resolution) {
      this.subsectionStyles = {};
      this.subsectionResolution = resolution;
    }

    // only want to create layers once. So store in object.
    let subsectionStyle = this.subsectionStyles[feature.getId()];
    if (!subsectionStyle) {
      subsectionStyle = this.polygonStyleTextFunction('rgb(2, 114, 202)', 'rgba(2, 114, 202, 0.1)', 1.5, resolution, feature.get('label'), 'rgb(2, 114, 202)');
      this.subsectionStyles[feature.getId()] = subsectionStyle;
    }

    return subsectionStyle;
  }


  /******** Watermark layer ********/
  private watermarkResolution: number = 0;
  private watermarkStyle: Style[] = null;
  private watermarkCanvas = null;
  private getWatermarkCanvas() {
    if (this.watermarkCanvas)
      return this.watermarkCanvas;
    else
      return this.makeImage(require('@/mapmanagement/static/images/layers/watermark.png'));
  }
  get watermark() {
    return new Promise((resolve, reject) => {
      let watermarkCanvas = this.getWatermarkCanvas();

      Promise.resolve(watermarkCanvas)
      .then(canvas => {
        resolve((feature, resolution) => {
          if (this.watermarkResolution != resolution) {
            this.watermarkStyle = null;
            this.watermarkResolution = resolution;
          }

          // change transparency as user zooms in
          if (!this.watermarkStyle) {
            let alpha = 0.06;
            if (resolution < 0.015)
              alpha = 0.04;

            let pattern = this.makePaternFromImage(canvas, alpha);
            this.watermarkStyle = this.polygonStylePattern('rgba(0, 0, 0, 0)', 0.1, pattern);
          }
          return this.watermarkStyle;
        });
      })
    });
  }


  /**
   * Constructor
   */
  constructor() {
    // Construct styles that require an async function.
    // Note: these styles could also be returned using an async function like hedge, canopy or watermark
    this.makePattern(require('@/mapmanagement/static/images/layers/bush.png'), 0.5)
    .then(result => {
      this.bushPattern = result;
    });

    this.makePattern(require('@/mapmanagement/static/images/layers/grass.png'), 1)
    .then(result => {
      this.grassStyle = this.polygonStylePattern('#d0f48e', 1, result);
    });

    this.makePattern(require('@/mapmanagement/static/images/layers/shrubland.png'), 1)
    .then(result => {
      this.shrublandStyle = this.polygonStylePattern('rgb(226, 233, 110)', 1, result);
    });

    this.makePattern(require('@/mapmanagement/static/images/layers/woodland.png'), 1)
    .then(result => {
      this.woodlandStyle = this.polygonStylePattern('#a9da64', 1, result);
    });

    this.loadImageAndSwitchSrcThroughCanvas().then((cleanupImage) => {
      this.makePattern(cleanupImage, 1)
      .then(result => {
        this.pathStyle = this.polygonStylePattern('#c7c07d', 1, result);
      });
    })
  }


  loadImageAndSwitchSrcThroughCanvas = function() {
    return new Promise((resolve) =>  {
      let img = document.createElement('img');
      img.crossOrigin = 'anonymous';
      img.src = require('@/mapmanagement/static/images/layers/path.png');

      img.onload = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 150;
        canvas.height = 150;
        ctx.drawImage(img, 0, 0);
        resolve(canvas.toDataURL('image/png'))
      }
    });
  }

  polygonStyleFunction(lineColor, fillColor, lineWidth?): Style[] {
    if (!lineWidth)
      lineWidth = 1;
    var style = new Style({
      fill: new Fill({
        color: fillColor
      }),
      stroke: new Stroke({
        color: lineColor,
        width: lineWidth
      }),
      image: new Circle({
        radius: 5,
        fill: new Fill({
          color: fillColor
        }),
        stroke: new Stroke({
          color: lineColor,
        }),
      })
    });
    return [style];
  }

  polygonStyleTextFunction(lineColor, fillColor, lineWidth, resolution, text, textColor='black', maxResolution=0.28, align='center', placement='point'): Style[] {

    var fontSize = 15, outlineWidth = 4;
    if (resolution >= maxResolution) {
      fontSize = 0;
      outlineWidth = 0;
    }
    else if (resolution >= 0.14){
      fontSize = 10;
      outlineWidth = 2;
    }
    else if (resolution >= 0.07){
      fontSize = 12;
      outlineWidth = 3;
    }

    if (!lineWidth)
      lineWidth = 1;
    var style = new Style({
      fill: new Fill({
        color: fillColor
      }),
      stroke: new Stroke({
        color: lineColor,
        width: lineWidth
      }),
      text: this.createTextStyle(text, fontSize, outlineWidth, textColor, align, placement)
    });
    return [style];
  }

  createTextStyle(feature_id, fontSize, outlineWidthp, color='black', align='center', placement='point'): Text {
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

    return new Text({
      textAlign: align,
      textBaseline: baseline,
      font: font,
      text: feature_id,
      fill: new Fill({
        color: color
      }),
      stroke: new Stroke({
        color: outlineColor,
        width: outlineWidth
      }),
      offsetX: offsetX,
      offsetY: offsetY,
      // rotation: rotation,
      overflow: true,
      placement: placement
    });
  }

  lineDashStyleFunction(lineColor, fillColor, lineWidth, lineDash): Style[] {
    if (!lineWidth)
      lineWidth = 1;
    var style = new Style({
      fill: new Fill({
        color: fillColor
      }),
      stroke: new Stroke({
        color: lineColor,
        width: lineWidth,
        lineDash: lineDash
      }),
    });
    return [style];
  }

  getScale(resolution): number {
    var scale;
    if (resolution === 0.028) {
      scale = 1;
    } else if (resolution === 0.07) {
      scale = 0.5;
    } else if (resolution === 0.14) {
      scale = 0.25;
    } else if (resolution === 0.28) {
      scale = 0.125;
    }
    return scale;
  }

  makePattern(base64Image, alpha): Promise<any> {
    return new Promise<any>(resolve => {
      this.makeImage(base64Image)
      .then((img) => {
        resolve(this.makePaternFromImage(img, alpha));
      });
    });    
  }
  
  makeImage(base64Image): Promise<any> {
    return new Promise<any>(resolve => {
      let img = new Image();
      img.onload = () => {
        resolve(img);
      };
      img.crossOrigin = "anonymous"
      img.src = base64Image;
    });    
  }

  makePaternFromImage(img, alpha) {
    let c = document.createElement('canvas');
    c.width=img.width;
    c.height=img.height;
    let ctx = c.getContext("2d");
    ctx.globalAlpha = alpha;
    ctx.clearRect(0, 0, c.width, c.height);
    let pat = ctx.createPattern(img, 'repeat');
    ctx.rect(0, 0, c.width, c.height);
    ctx.fillStyle = pat;
    ctx.fill();
    return ctx.createPattern(c, 'repeat');
  }

  polygonStylePatternDash(lineColor, lineWidth, pattern, lineDash): Style[] {
    let style = this.polygonStylePattern(lineColor, lineWidth, pattern)[0];
    let stroke = style.getStroke();
    stroke.setLineDash(lineDash);
    style.setStroke(stroke);
    return [style];
  }

  polygonStylePattern(lineColor, lineWidth, pattern): Style[] {
    if (!lineWidth)
      lineWidth = 1;
    var style = new Style({
      fill: new Fill({
        color: pattern
      }),
      stroke: new Stroke({
        color: lineColor,
        width: lineWidth
      })
    });
    return [style];
  }

  createTextMemorialBenchStyle(feature_id, fontSize): Text {
    var align = 'center';
    var baseline = 'middle';
    var size = fontSize + 'px';
    var offsetX = 0;
    var offsetY = 0;
    var weight = 'bold';
    // var rotation = parseFloat(dom.rotation.value);
    var font = weight + ' ' + size + ' Verdana';
    // var fillColor = dom.color.value;
    var outlineColor = '#ffffff';
    var outlineWidth = 3;

    return new Text({
      textAlign: align,
      textBaseline: baseline,
      font: font,
      text: feature_id,
      fill: new Fill({
        color: 'black'
      }),
      offsetX: offsetX,
      offsetY: offsetY,
			overflow: true
    });
  }

  scaleTransformFunction(centre, scale, array) {
    if (!isNaN(scale)) {
      for (var j = 0, lenJ = array.length; j < lenJ; j = j + 2) {
        //translate points to resize according to scale
        array[j] = (array[j] - centre[0]) * scale + centre[0];
        array[j + 1] = (array[j + 1] - centre[1]) * scale + centre[1];
      }
    }
    return array;
  }

  /**
   * Returns style for a selected feature
   */
  selectedStyle(feature, resolution) {
    let markerType = feature.getProperties()['marker_type'];
    
    if (markerType === 'gravestone')
      return this.polygonStyleFunction('rgba(238, 89, 42, 1)', 'rgba(238, 89, 42, 1)');
    else if (markerType === 'tap')
      return this.tap(feature, resolution, true);
    else if (markerType === 'tree')
      return this.tree(feature, resolution, true);
      else if (markerType === 'bush')
        return this.bush(feature, resolution, true);
    else if (markerType === 'tree_trunk')
      return this.tree_trunk(feature, resolution, true);
    else if (markerType === 'water_trough')
      return this.water_trough(feature, resolution, true);
    else
      return [new Style({
        fill: new Fill({
          color: this.hightlightFill
        }),
        stroke: new Stroke({
          color: this.hightlightStroke,
          width: 2
        })
      })];
  }

  selectedStyleFunction = (feature, resolution) => {
    return this.selectedStyle(feature, resolution);
  }

  selectedStyleWithMarkerFunction = (feature, resolution) => {
    let style = this.selectedStyleFunction(feature, resolution)[0];

    // Add label to style if label exists
    let textStyle = new Text({
      text: '\uf3c5',
      font: '900 24px "Font Awesome 5 Free"',
      fill: new Fill({
        color: 'rgb(255, 0, 0)',
      }),
      stroke: new Stroke({
        color: 'rgb(255, 244, 230)',
        width: 2
      }),
      overflow: true,
      textBaseline: 'bottom',
      offsetY: 1
    });

    style.setText(textStyle);
    style.setZIndex(2);

    return [style];
  }

  readonly tree_polygon = {
    "type": "Polygon",
    "coordinates": [
      [
        [348763.64379999973, 526386.89389999956],
        [348763.6755, 526386.88199999928],
        [348763.7867, 526386.78680000082],
        [348763.85410000011, 526386.74709999934],
        [348763.9057, 526386.75500000082],
        [348764.00100000016, 526386.69549999945],
        [348764.06840000022, 526386.63199999928],
        [348764.12000000011, 526386.548599999],
        [348764.17960000038, 526386.48509999923],
        [348764.23909999989, 526386.43349999934],
        [348764.3224, 526386.39780000038],
        [348764.39389999956, 526386.34229999967],
        [348764.59630000032, 526386.12],
        [348764.60819999967, 526386.09219999984],
        [348764.60819999967, 526385.98509999923],
        [348764.636, 526385.8739],
        [348764.636, 526385.78659999929],
        [348764.60819999967, 526385.739],
        [348764.52880000044, 526385.6557],
        [348764.49710000027, 526385.59610000066],
        [348764.3958, 526385.50290000066],
        [348764.38989999983, 526385.41750000045],
        [348764.3438, 526385.34889999963],
        [348764.34229999967, 526385.31039999984],
        [348764.2193, 526385.05240000039],
        [348764.12000000011, 526384.95319999941],
        [348764.02880000044, 526384.88969999924],
        [348763.8224, 526384.82220000029],
        [348763.72319999989, 526384.76669999957],
        [348763.64379999973, 526384.76669999957],
        [348763.59619999956, 526384.78649999946],
        [348763.5049, 526384.78649999946],
        [348763.4731, 526384.79839999974],
        [348763.36600000039, 526384.85789999925],
        [348763.23099999968, 526384.973],
        [348763.11589999963, 526385.004799999],
        [348762.90160000045, 526385.02070000023],
        [348762.85400000028, 526385.0603],
        [348762.7429, 526385.11590000056],
        [348762.67939999979, 526385.2072],
        [348762.6754, 526385.27070000023],
        [348762.6278, 526385.37780000083],
        [348762.6398, 526385.50960000046],
        [348762.62380000018, 526385.53659999929],
        [348762.60790000018, 526385.57630000077],
        [348762.60790000018, 526385.6239],
        [348762.56429999974, 526385.67149999924],
        [348762.5603, 526385.70729999989],
        [348762.5444, 526385.72709999979],
        [348762.5444, 526385.766799999],
        [348762.51669999957, 526385.84620000049],
        [348762.51669999957, 526385.92159999907],
        [348762.52809999976, 526385.97870000079],
        [348762.477, 526386.0644000005],
        [348762.47300000023, 526386.13990000077],
        [348762.48489999957, 526386.16369999945],
        [348762.48890000023, 526386.24699999951],
        [348762.52460000012, 526386.28270000033],
        [348762.63179999962, 526386.38189999945],
        [348762.7429, 526386.44539999962],
        [348762.74849999975, 526386.4496],
        [348762.77070000023, 526386.49310000055],
        [348762.8421, 526386.55660000071],
        [348762.9254, 526386.6082000006],
        [348763.0153, 526386.62299999967],
        [348763.03259999957, 526386.64790000021],
        [348763.05640000012, 526386.72330000065],
        [348763.10010000039, 526386.78280000016],
        [348763.21119999979, 526386.87409999967],
        [348763.29449999984, 526386.91770000011],
        [348763.42949999962, 526386.92960000038],
        [348763.489, 526386.90190000087],
        [348763.64379999973, 526386.89389999956]
      ]
    ]
  };
  
  readonly bush_polygon = {
    "type": "Polygon",
    "coordinates": [
      [
        [348766.21339999977, 526386.43799999915],
        [348766.2796, 526386.41819999926],
        [348766.2928, 526386.4049],
        [348766.33910000045, 526386.30570000038],
        [348766.3788, 526386.07090000063],
        [348766.40859999973, 526386.01799999923],
        [348766.41189999972, 526385.9618],
        [348766.43499999959, 526385.87910000049],
        [348766.4912, 526385.79969999939],
        [348766.49789999984, 526385.70050000027],
        [348766.46480000019, 526385.60129999928],
        [348766.3953, 526385.5120000001],
        [348766.32919999957, 526385.38299999945],
        [348766.30269999988, 526385.18119999953],
        [348766.19689999986, 526385.01920000091],
        [348766.1473000003, 526384.98279999942],
        [348766.0844, 526384.97289999947],
        [348766.03809999954, 526384.94639999978],
        [348766.00179999974, 526384.9431],
        [348765.8893, 526384.9001000002],
        [348765.73060000036, 526384.79099999927],
        [348765.54540000018, 526384.73809999973],
        [348765.42300000042, 526384.74799999967],
        [348765.3734, 526384.77109999955],
        [348765.29069999978, 526384.78769999929],
        [348765.21789999958, 526384.83070000075],
        [348765.00960000046, 526384.84390000068],
        [348764.9633, 526384.87360000052],
        [348764.90039999969, 526384.88360000029],
        [348764.86409999989, 526384.91330000013],
        [348764.81439999957, 526384.97949999943],
        [348764.78799999971, 526385.03570000082],
        [348764.69539999962, 526385.15809999965],
        [348764.6722, 526385.18119999953],
        [348764.62920000032, 526385.20109999925],
        [348764.57629999984, 526385.25400000066],
        [348764.54320000019, 526385.3267],
        [348764.48699999973, 526385.40279999934],
        [348764.47049999982, 526385.44910000078],
        [348764.47049999982, 526385.49210000038],
        [348764.49029999971, 526385.76],
        [348764.4539, 526385.86250000075],
        [348764.45729999989, 526385.96509999968],
        [348764.48369999975, 526386.01799999923],
        [348764.49029999971, 526386.07420000061],
        [348764.52670000028, 526386.14699999988],
        [348764.74500000011, 526386.41489999928],
        [348764.84420000017, 526386.57359999977],
        [348764.90039999969, 526386.61329999939],
        [348765.09559999965, 526386.64970000088],
        [348765.27749999985, 526386.72900000028],
        [348765.4263000004, 526386.77529999986],
        [348765.6512000002, 526386.7621],
        [348765.70409999974, 526386.7522],
        [348765.82320000045, 526386.67940000072],
        [348765.83640000038, 526386.65960000083],
        [348765.89589999989, 526386.61989999935],
        [348766.01829999965, 526386.55709999986],
        [348766.10429999977, 526386.52730000019],
        [348766.16380000021, 526386.49090000056],
        [348766.21339999977, 526386.43799999915]
      ]
    ]
  };
  
  readonly hightlightFill = 'rgba(238, 89, 42, 0.4)';
  readonly hightlightStroke = 'rgba(238, 89, 42, 1)';
}