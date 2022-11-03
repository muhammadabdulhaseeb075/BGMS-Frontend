import Vue from 'vue';
import VueRouter from 'vue-router';
import router from '@/analytics/router';
import store from '@/analytics/store';
import vuetify from '@/plugins/vuetify';
import AnalyticsApp from './AnalyticsApp.vue'

Vue.use(VueRouter);

new Vue({
    el: '#analytics-app',
    router,
    store,
    vuetify,
    render: (h) => h(AnalyticsApp),
} as any);

Vue.config.devtools = process.env.NODE_ENV === 'development';
