import Vue from 'vue'
import axios from 'axios'
import vueRouter from 'vue-router'
import store from './store'
import DataMatchingVueApp from './DataMatchingVueApp.vue'
import router from '@/datamatching/router/index.js'

Vue.use(vueRouter)

Vue.config.devtools = process.env.NODE_ENV === "development";

new Vue({
  el: '#dmapp',
  store,
  render: (h) => h(DataMatchingVueApp),
  router: router,
  created: function() {
    const token = (document.getElementsByName("csrfmiddlewaretoken")[0] as HTMLInputElement).value;
    axios.defaults.headers.post['X-CSRFToken'] = token;
    axios.defaults.headers.delete['X-CSRFToken'] = token;
  }
});
