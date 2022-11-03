// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Router from "vue-router"
import axios from 'axios'
import SecurityMixin from '@/mixins/securityMixin'
import MainVueApp from './MainVueApp.vue'
import router from '@/main/router/index.js'
import vuetify from '@/plugins/vuetify'
import store from './store'
//import * as Sentry from "@sentry/vue";
import * as Sentry from "@sentry/browser";
import { Integrations } from "@sentry/tracing";

require('focus-visible');

//Vue.use(Router);

/*
Sentry.init({
  Vue,
  dsn: "https://00faab69fe7347469ebd65a7276ff66e@sentry.burialgrounds.co.uk/6",
  integrations: [
    new Integrations.BrowserTracing({
      routingInstrumentation: Sentry.vueRouterInstrumentation(router),
      tracingOrigins: ["localhost", "burialgrounds.co.uk", /^\//],      
    }),
  ],
  logErrors: true, //also send errors to console
  tracesSampleRate: 1.0,
});//TODO://change dev/production based on process.env.NODE_ENV === "development"
*/
/*
Sentry.init({
  dsn: "https://00faab69fe7347469ebd65a7276ff66e@sentry.burialgrounds.co.uk/6",
  integrations: [new Integrations.BrowserTracing()],
  //
  tracesSampleRate: 1.0,
});
*/

new Vue({
  vuetify,
  el: '#mainapp',
  store,
  router: router,
  mixins: [SecurityMixin],
  render: (h) => h(MainVueApp),
  created: function() {
    // get csrf token from dom. (Could also get from cookie but this would mean we can't use CSRF_COOKIE_HTTPONLY)
    const csrfElement = (document.getElementsByName("csrfmiddlewaretoken")[0] as HTMLInputElement);
    if (csrfElement) {
      const token = csrfElement.value;
      axios.defaults.headers.post['X-CSRFToken'] = token;
      axios.defaults.headers.put['X-CSRFToken'] = token;
      axios.defaults.headers.patch['X-CSRFToken'] = token;
      axios.defaults.headers.delete['X-CSRFToken'] = token;

      axios.defaults.withCredentials = true;
    }

    axios.get('/userAccess/')
    .then(response => {
      this.$store.commit('commitAccess', response.data);
    })
    .catch(response => {
      console.warn('Couldn\'t get data from server: ' + response);
    });
  }
}).$mount('#app');

Vue.config.devtools = process.env.NODE_ENV === "development";

