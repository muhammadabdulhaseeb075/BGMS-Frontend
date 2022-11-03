import { createRouter, createWebHashHistory } from "vue-router";
import routes from "./routes";

// Adding complementary library for managment routes in vue.js
// Create a router
const router = createRouter({
    history: createWebHashHistory(),
    routes
});
// Sync vuex state with the router's data

export default router;
export {
    routes
};
