// // creating a webpack context to load dynamic routes in the router folder
// let context = require.context('./', true, /(([A-Z])\w+)\/index.js$/);
// let routeFiles = context.keys();
// let routes = [];

// routeFiles.forEach(pathFile => {
//   // saving the route declarations
//   routes.push(context(pathFile).default);
// });

// /* @TODO: setting the 404 view */

// export default routes;

import Booking from "src/router/Booking";

export default [
    Booking,
];
