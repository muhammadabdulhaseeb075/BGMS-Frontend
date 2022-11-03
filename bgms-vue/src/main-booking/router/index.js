import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

const MAINMENU = () => import('@/main-booking/components/BookingMenu');
const CALENDAR = () => import('@/main/components/Booking/Calendar');

const router = new VueRouter({
  routes: [
    {
      path: '/',
      name: 'bookingMenu',
      component: CALENDAR,
    },
    {
      path: '/add-booking',
      name: 'calendar',
      component: MAINMENU,
    }
  ]
})

export default router