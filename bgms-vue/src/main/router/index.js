import Vue from 'vue';
import VueRouter from 'vue-router';

const HOME = () => import('@/main/components/Home');

const CONTACT = () => import('@/main/components/Contact');

const BOOKING = () => import('@/main/components/Booking/Booking');
const CALENDAR = () => import('@/main/components/Booking/Calendar');
const FUNERALBOOKINGS = () => import('@/main/components/Booking/FuneralBookings');
const BOOKINGDIALOG = () => import(/* webpackChunkName: "booking-dialog" */ '@/main/components/Booking/BookingDialog');
const FUNERALBOOKINGFORM = () => import(/* webpackChunkName: "booking-dialog" */ '@/main/components/Booking/FuneralBookingForm.vue')
const DATETIME = () => import(/* webpackChunkName: "booking-dialog" */ '@/main/components/Booking/BookingFormComponents/DateTime.vue')
const DECEASED = () => import(/* webpackChunkName: "booking-dialog" */ '@/main/components/Booking/BookingFormComponents/Deceased.vue')
const FUNERALDIRECTOR = () => import(/* webpackChunkName: "booking-dialog" */ '@/main/components/Booking/BookingFormComponents/FuneralDirector.vue')
const BURIAL = () => import(/* webpackChunkName: "booking-dialog" */ '@/main/components/Booking/BookingFormComponents/Burial.vue')
const NEXTOFKIN = () => import(/* webpackChunkName: "booking-dialog" */ '@/main/components/Booking/BookingFormComponents/NextOfKin.vue')
const FUNERALBOOKINGSTATUS = () => import(/* webpackChunkName: "booking-dialog" */ '@/main/components/Booking/BookingFormComponents/FuneralBookingStatus.vue')

Vue.use(VueRouter);

/**
 * These routes are used by more than one parent.
 * @param {*} parentRouteID User as prefix for route names.
 *                0 - calendar parent
 */
function getBookingDialogRoutes(parentRouteID) {
  return {
    path: ':siteID/:id/:eventTypeID',
    component: BOOKINGDIALOG,
    name: parentRouteID + "_bookingdialog",
    props: true,
    children: [
      {
        path: 'funeral',
        component: FUNERALBOOKINGFORM,
        name: parentRouteID + "_funeralbooking",
        props: true,
        children: [
          {
            path: 'da',
            component: DATETIME,
            name: parentRouteID + "_datetime",
            props: true,
          },
          {
            path: 'de',
            component: DECEASED,
            name: parentRouteID + "_deceased",
            props: true,
          },
          {
            path: 'fu',
            component: FUNERALDIRECTOR,
            name: parentRouteID + "_funeralDirector",
            props: true,
          },
          {
            path: 'bu',
            component: BURIAL,
            name: parentRouteID + "_burial",
            props: true,
          },
          {
            path: 'nk',
            component: NEXTOFKIN,
            name: parentRouteID + "_nextOfKin",
            props: true,
          },
          {
            path: 'ch',
            component: FUNERALBOOKINGSTATUS,
            name: parentRouteID + "_funeralBookingStatus",
            props: true,
          }
        ]
      }
    ]
  }
}

const calendarDialogChildren = getBookingDialogRoutes(0);
const bookingTableDialogChildren = getBookingDialogRoutes(1);

const router = new VueRouter({
  routes: [
    {
      path: '/',
      name: 'home',
      component: HOME
    },
    {
      path: '/contact',
      name: 'contact',
      component: CONTACT,
    },
    {
      path: '/booking',
      component: BOOKING,
      children: [
        {
          path: '',
          name: 'calendar',
          component: CALENDAR,
          meta: { parentRouteID: 0 },
          children: [
            calendarDialogChildren
          ]
        },
        {
          path: 'funerals',
          name: 'funeralBookings',
          component: FUNERALBOOKINGS,
          meta: { parentRouteID: 1 },
          children: [
            bookingTableDialogChildren
          ]
        }
      ]
    }
  ]
})

export default router;