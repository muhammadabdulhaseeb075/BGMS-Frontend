import Router from 'vue-router'
import Index from '@/analytics/router/Views/Index/index.vue' ;
import Report from '@/analytics/router/Views/Report/index.vue';

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Index',
            component: Index
        },
        {
            path: '/report',
            name: 'Report',
            component: Report
        }
    ]
});
