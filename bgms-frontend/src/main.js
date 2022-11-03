import { createApp } from "vue";

import router, { routes } from "src/router";
import store  from "src/store";
import { setup as httpSetup } from "src/services/http";

//Sentry Remote Tracing Packages
//import * as Sentry from "@sentry/vue";
//import { Integrations } from "@sentry/tracing";

// import all global CSS styles
import "src/styles/main.css";

import App from "./App";

store.commit("addRoutes", routes);

const app = createApp(App);

/*
Sentry.init({
    app,
    dsn: "https://9e9647c1c26d446b90d85b1815f01ae6@sentry.burialgrounds.co.uk/3",
    integrations: [
      new Integrations.BrowserTracing({
        routingInstrumentation: Sentry.vueRouterInstrumentation(router),
        //tracingOrigins: ["localhost", "bgms.com", /^\//],   
        debug:true,     
        attachStacktrace:true,
        xhr: true,
      }),
    ],
    // Set tracesSampleRate to 1.0 to capture 100%
    // of transactions for performance monitoring.
    // We recommend adjusting this value in production
    tracesSampleRate: 1.0,
  });
*/

app.use(router);
app.use(store);
app.use(httpSetup);

app.config.devtools = true;

// Get ready to rock!!!!
app.mount("#main");
