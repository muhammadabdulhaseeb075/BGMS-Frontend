import * as constants from "./constants";

import Index from "./pages/Index.vue";

export default {
    path: "/booking",
    name: constants.BOOKING_NAME,
    component: Index,
    meta: { 
        linkLabel: "Bookings",
        icon: "fa-calendar-alt"
    },
    children: [
        {
            path: "",
            component: () => import("./pages/Booking.vue"),
        },
        {
            path: "calendar",
            name: constants.BOOKING_SPLIT_VIEW,
            component: () => import("./pages/SplitView.vue"),
            meta: {
                linkLabel: "Calendar",
                icon: "fa-calendar-alt"
            },
        },
        /*{
            path: "calendar",
            name: constants.BOOKING_CALENDAR,
            component: () => import("./pages/Calendar.vue"),
            meta: {
                linkLabel: "Calendar",
                icon: "fa-calendar-alt"
            },
        },*/
        {
            path: "add-event",
            name: constants.BOOKING_ADD_NAME,
            component: () => import("./pages/AddEvent.vue"),
            meta: {
                linkLabel: "Booking",
                icon: "fa-plus"
            },
        },
        {
            path: "search-event",
            name: constants.BOOKING_SEARCH_NAME,
            component: () => import("./pages/SearchEvent.vue"),
            meta: {
                linkLabel: "Search",
                icon: "fa-search"
            },
        },
        {
            path: "status-event",
            name: constants.BOOKING_STATUS_NAME,
            component: () => import("./pages/StatusBooking.vue"),
            meta: {
                linkLabel: "Status",
                icon: "fa-file"
            },
        },
    ],
};
