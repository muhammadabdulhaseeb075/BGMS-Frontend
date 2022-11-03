import Select from 'ol/interaction/Select';
import Collection from 'ol/Collection';
import { Draw, Modify, Pointer, Translate } from 'ol/interaction';
import { getOlLayers } from '@/mapmanagement/components/Map/models/Layer';

export default class MapInteraction {

  group;
  type;
  parameters;
  handlers;
  interactionLayer;
  interactionFeatures
  interaction;

  constructor(interaction) {
    this.group = interaction.group;
    this.type = interaction.type;
    this.parameters = interaction.parameters;
    this.handlers = interaction.handlers;

    let map = (window as any).OLMap;

    if (this.parameters && this.parameters.layer) {
      map.getLayers().forEach(layer => {
        if(layer.get('name') === this.parameters.layer)
            this.interactionLayer = layer;
      });
    }

    if(this.parameters && this.parameters.selectFeatures){
      interaction = map.getInteractions().forEach(element => {
        if(element.constructor === Select)
          this.interactionFeatures = element.getFeatures();
      });
    } 
    else if(this.parameters && this.parameters.layerName){
      let layers = getOlLayers(this.parameters.layerName, true);
      this.interactionFeatures = new Collection();
      for (var l in layers){
        this.interactionFeatures.extend(layers[l].getSource().getFeatures());
      }
    } 
    else if(this.parameters && this.parameters.feature){
      // Move multiple features together that are in different layers and were passed as parameters
      let featureId = this.parameters.feature.featureId;
      let layerName = this.parameters.feature.layerName;
      
      let layers = getOlLayers(layerName, true);
    
      let feature_collection = [layers[layerName].getSource().getFeatureById(featureId)];

      if (this.parameters.feature.featureIdunder && this.parameters.feature.layerNameunder){
        const featureId2 = this.parameters.feature.featureIdunder;
        const layerName2 = this.parameters.feature.layerNameunder;
        let layers2 = getOlLayers(layerName2, true);
        feature_collection.push(layers2[layerName2].getSource().getFeatureById(featureId2));
      }
    
      this.interactionFeatures = new Collection(feature_collection);
    }

    switch(this.type){
      case 'draw':
        console.log(this.parameters);
        this.interaction = createDrawInteraction(this.parameters, this.interactionLayer.getSource(), this.handlers);
        break;
      case 'modify':
        this.interaction = createModifyInteraction(this.interactionLayer, this.handlers, this.interactionFeatures, this.parameters.style);
        break;
      case 'select':
        this.interaction = createSelectInteraction(this.interactionLayer, this.parameters, this.handlers);
        break;
      case 'pointer':
        this.interaction = createPointerInteraction(this.handlers);
        break;
      case 'translate':
        this.interaction = createTranslateInteraction(this.interactionFeatures, this.interactionLayer);
        break;
      default:
        this.interaction = null;
    }
  }

  addInteractionToMap() {
    (window as any).OLMap.addInteraction(this.interaction);
  }

  removeInteractionFromMap() {
    (window as any).OLMap.removeInteraction(this.interaction);
  }
}

/*Function to create draw interaction */
function createDrawInteraction(parameters, drawSource, handlers){
  //creating a new interaction
  parameters = JSON.parse(JSON.stringify(parameters));
  parameters.source = drawSource;
  var drawInteraction = new Draw(parameters);
  if(handlers){
    if(handlers.drawstart)
      drawInteraction.on('drawstart', handlers.drawstart);
    if(handlers.drawend)
      drawInteraction.on('drawend', handlers.drawend);
  }

  return drawInteraction;
}

function createModifyInteraction(layer, handlers, features, style){
  if(!features)
    features = new Collection(layer.getSource().getFeatures())
  let modifyInteraction = new Modify({
    features: features,
    style: style
  });

  if(handlers && handlers.modifyend){
    modifyInteraction.on('modifyend', handlers.modifyend)
  }
  return modifyInteraction;
}

function createSelectInteraction(layer, parameters, handlers){
  let selectInteraction = new Select({
    condition: parameters.condition,
    addCondition: parameters.addCondition,
    removeCondition: parameters.removeCondition,
    style: parameters.style,
    layers: [layer]
  });
  console.log(selectInteraction.getProperties());
  if(handlers && handlers.handleSelect){
    selectInteraction.getFeatures().on('add', handlers.handleSelect.bind(selectInteraction));
  }
  if(handlers && handlers.handleUnselect){
    selectInteraction.getFeatures().on('remove', handlers.handleUnselect.bind(selectInteraction));
  }
  return selectInteraction;
}

function createPointerInteraction(handlers){
  return new Pointer(handlers);
}

function createTranslateInteraction(features, layer){
  if(!features)
    features = getOlLayers(layer.name, true);
  return new Translate({features:features});
}