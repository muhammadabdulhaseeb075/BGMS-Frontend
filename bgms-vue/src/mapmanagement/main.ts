// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Router from 'vue-router'
import axios from 'axios'
import store from './store'
import RotateFeatureInteraction from 'ol-rotate-feature';
import router from '@/mapmanagement/router/index.js';
import MapManagementVueApp from '@/mapmanagement/MapManagementVueApp.vue'
import NestedApps from './nestedApps'
import vuetify from '@/plugins/vuetify'

import * as Sentry from "@sentry/vue";
//import * as Sentry from "@sentry/browser";
import { Integrations } from "@sentry/tracing";

import 'ol/ol.css';
import { getTopLeft, getCenter, containsExtent, intersects } from 'ol/extent';
import Feature from 'ol/Feature';
import GeoJSON from 'ol/format/GeoJSON';
import CircleGeom from 'ol/geom/Circle';
import LineString from 'ol/geom/LineString';
import MultiPolygon from 'ol/geom/MultiPolygon';
import Polygon from 'ol/geom/Polygon';
import {fromCircle} from 'ol/geom/Polygon';
import Observable from 'ol/Observable';
import Overlay from 'ol/Overlay';
import Circle from 'ol/style/Circle';
import Fill from 'ol/style/Fill';
import RegularShape from 'ol/style/RegularShape';
import Stroke from 'ol/style/Stroke';
import Style from 'ol/style/Style';
import Text from 'ol/style/Text';

import { messages } from '@/global-static/messages.js'

Vue.use(Router);

Sentry.init({
  Vue,
  dsn: "https://00faab69fe7347469ebd65a7276ff66e@sentry.burialgrounds.co.uk/6",
  integrations: [
    new Integrations.BrowserTracing({
      routingInstrumentation: Sentry.vueRouterInstrumentation(router),
      tracingOrigins: ["localhost", "burialgrounds.co.uk", /^\//],
    }),
  ],
  tracesSampleRate: 1.0,
});

require('focus-visible');

(window as any).messages = messages;
(window as any).RotateFeatureInteraction = RotateFeatureInteraction;

// Openlayers is broken down into component.
// We could import all of ol (npm install openlayers), but this will contain stuff we don't need.
// Once ol is brought into Vue these imports will be for specific vue components.
(window as any).ol = {};
(window as any).ol.extent = {};
(window as any).ol.extent.getTopLeft = getTopLeft;
(window as any).ol.extent.getCenter = getCenter;
(window as any).ol.extent.containsExtent = containsExtent;
(window as any).ol.extent.intersects = intersects;
(window as any).ol.Feature = Feature;
(window as any).ol.format = {};
(window as any).ol.format.GeoJSON = GeoJSON;
(window as any).ol.geom = {};
(window as any).ol.geom.Circle = CircleGeom;
(window as any).ol.geom.LineString = LineString;
(window as any).ol.geom.MultiPolygon = MultiPolygon;
(window as any).ol.geom.Polygon = Polygon;
(window as any).ol.geom.Polygon['fromCircle'] = fromCircle;
(window as any).ol.Observable = Observable;
(window as any).ol.Overlay = Overlay;
(window as any).ol.style = {};
(window as any).ol.style.Circle = Circle;
(window as any).ol.style.Fill = Fill;
(window as any).ol.style.RegularShape = RegularShape;
(window as any).ol.style.Stroke = Stroke;
(window as any).ol.style.Style = Style;
(window as any).ol.style.Text = Text;

// get csrf token from dom. (Could also get from cookie but this would mean we can't use CSRF_COOKIE_HTTPONLY)
const token = (document.getElementsByName("csrfmiddlewaretoken")[0] as HTMLInputElement).value;

axios.defaults.headers.post['X-CSRFToken'] = token;
axios.defaults.headers.put['X-CSRFToken'] = token;
axios.defaults.headers.delete['X-CSRFToken'] = token;
axios.defaults.headers.patch['X-CSRFToken'] = token;

Vue.config.devtools = process.env.NODE_ENV === "development";

// allow AngularJS to dynamically create vue apps
new NestedApps();

new Vue({
  vuetify,
  el: '#mapmanagementapp',
  store,
  router,
  render: (h) => h(MapManagementVueApp)
});
