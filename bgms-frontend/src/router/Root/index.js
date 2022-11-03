
export default {
    path: "/",
    name: "root",
    component: () => import("./Root.vue"),
    meta: {},
    props: {
        title: "View 1"
    },
};
