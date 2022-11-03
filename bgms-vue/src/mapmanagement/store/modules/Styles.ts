import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import Style from 'ol/style/Style';
import Text from 'ol/style/Text';
import Circle from 'ol/style/Circle';
import Icon from 'ol/style/Icon';

const markerText = new Text({
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

const state = {
  markerText: markerText,
  highlightedGraveStyle: new Style({
    fill: new Fill({
      color: 'rgba(238, 89, 42, 0.4)'
    }),
    stroke: new Stroke({
      color: 'rgba(238, 89, 42, 1)',
      width: 2
    }),
    text: markerText
  }),
  highlightedMemorialStyle: new Style({
    fill: new Fill({
      color: 'rgba(238, 89, 42, 1)'
    }),
    text: markerText
  }),
  drawLayerStyle: null,
  addedStyleFunction: (feature, resolution) => {
    return [new Style({
      fill: new Fill({
        color: 'rgba(204, 153, 0, 0.4)'
        // color: 'transparent'
      }),
      stroke: new Stroke({
        color: 'rgba(204, 153, 0, 1)',
        width: 2
      }),
      image: new Icon({
        opacity: 1,
        src: require('@/mapmanagement/static/images/added_8x8.png'),
        crossOrigin: location.hostname,
      })
    })];
  }
}

// getters
const getters = {
  drawLayerStyleFunction: state => () => {
    if (!state.drawLayerStyle) {
      state.drawLayerStyle = new Style({
        fill: new Fill({
          color: 'rgba(255, 255, 255, 0.2)'
        }),
        stroke: new Stroke({
          color: '#ffcc33',
          width: 2
        }),
        image: new Circle({
          radius: 7,
          fill: new Fill({
            color: '#ffcc33'
          })
        })
      });
    }
    return [state.drawLayerStyle];
  },
}

// actions
const actions = {
}

// mutations
const mutations = {
}

export default {
  state,
  getters,
  //actions,
  //mutations
};

(window as any).addedStyleFunction = state.addedStyleFunction;