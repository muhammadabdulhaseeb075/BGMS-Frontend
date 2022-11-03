import Vue from 'vue'
import Router from 'vue-router'

import * as Sentry from "@sentry/vue";
import { BrowserTracing } from "@sentry/tracing";

const Index = () => import('@/datamatching/components/Index.vue')
const UserActivity = () => import('@/datamatching/components/UserActivity.vue')
const MemorialStatus = () => import('@/datamatching/components/MemorialStatus.vue')

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/index',
      name: 'Index',
      component: Index
    },
    {
      path: '/useractivity',
      name: 'UserActivity',
      component: UserActivity
    },
    {
      path: '/memorialstatus',
      name: 'MemorialStatus',
      component: MemorialStatus
    },
    { 
      path: '',
      redirect: { name: 'Index' }
    },
  ]
});

/*
Sentry.init({
  Vue,
  dsn: "https://d1eb8523464046c9b09dc9c009ad8406@sentry.burialgrounds.co.uk/5",
  integrations: [
    new Integrations.BrowserTracing({
      routingInstrumentation: Sentry.vueRouterInstrumentation(router),
      tracingOrigins: ["localhost", "my-site-url.com", /^\//],
    }),
  ],
  // Set tracesSampleRate to 1.0 to capture 100%
  // of transactions for performance monitoring.
  // We recommend adjusting this value in production
  tracesSampleRate: 1.0,
});
*/
