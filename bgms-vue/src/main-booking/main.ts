import Vue from 'vue'
import axios from 'axios'
import vueRouter from 'vue-router'
import MainBookingVueApp from './MainBooking.vue'
import router from '@/main-booking/router/index.js'
import vuetify from '@/plugins/vuetify'
import store from './store'

Vue.use(vueRouter)

Vue.config.devtools = process.env.NODE_ENV === "development";

new Vue({
  vuetify,
  store,
  el: '#mainbooking',
  render: (h) => h(MainBookingVueApp),
  router: router,
  created: function() {
    const token = (document.getElementsByName("csrfmiddlewaretoken")[0] as HTMLInputElement).value;
    axios.defaults.headers.post['X-CSRFToken'] = token;
    axios.defaults.headers.put['X-CSRFToken'] = token;
    axios.defaults.headers.patch['X-CSRFToken'] = token;
    axios.defaults.headers.delete['X-CSRFToken'] = token;

    axios.defaults.withCredentials = true;

    /* this will load all the sites where the user has access to and store the information */
     this.$store.dispatch('getSitesAndSiteManagement');
  }
});

