import Vue from 'vue';
import PortalVue from 'portal-vue';
import VueRouter from 'vue-router';
import Vuetify from 'vuetify';
import VueI18n from 'vue-i18n';
import {cs as csVuetify, en as enVuetify} from 'vuetify/es5/locale';
import colors from 'vuetify/es5/util/colors';
import '../scss/index.scss';

import csLocal from './locale/cs.json';
import App from './App';
import Axios from './axios';
import hasPerm from './user';
import {pageContext} from './utils';

export default function createVue(opts = {}) {
    Vue.use(VueI18n);
    Vue.use(Vuetify);
    Vue.use(VueRouter);
    Vue.use(PortalVue);
    Vue.config.productionTip = false;

    Vue.directive('has-perm', (el, bindings, vnode) => {
        // TODO: think about https://github.com/mblarsen/vue-browser-acl
        if (bindings.arg) {

            let originDisplay = el.style.display;
            el.style.display = 'none';
            bindings.arg && hasPerm(bindings.arg).then((allowed) => {
                el.style.display = allowed ? originDisplay : 'none';
            });
        }
    });

    const {locale} = pageContext;

    const vuetify = new Vuetify({
        lang: {
            locales: {cs: csVuetify, en: enVuetify},
            current: locale,
        },
        theme: {
            themes: {
                light: {
                    primary: colors.orange.base,
                    secondary: colors.brown.base,
                    accent: colors.deepOrange.base,
                    error: colors.pink.base,
                    warning: colors.orange.darken4,
                    info: colors.blue.base,
                    success: colors.green.base,
                },
            },
        },
    });

    const i18n = new VueI18n({
        locale,
        messages: {cs: csLocal, en: {}},
    });

    Axios.get('/api/i18n/catalog', {headers: {'Accept-language': locale}}).then(({data}) => {
        i18n.mergeLocaleMessage(locale, data.catalog);
    });

    const router = new VueRouter({
        routes: [
            {path: '/', component: () => import('./pages/Dashboard/Page'), name: 'dashboard'},
            {path: '/thesis/list', component: () => import('./pages/ThesisList/Page'), name: 'thesis-list'},
            {
                path: '/thesis/prepare',
                component: () => import('./pages/ThesisPrepare/Page'),
                name: 'thesis-prepare',
            },
            {
                path: '/thesis/submit/:id',
                component: () => import('./pages/ThesisSubmit/Page'),
                name: 'thesis-submit',
            },
            {path: '/reservations', component: () => import('./pages/ReservationList/Page'), name: 'reservations'},
            {path: '/exports', component: {template: '<div>Nonono</div>'}, name: 'exports'},
            {path: '/settings', component: {template: '<div>Nonono</div>'}, name: 'settings'},
            {path: '/review/:id', component: () => import('./pages/ReviewSubmit/Page'), name: 'review-submit'},
            {path: '*', component: {template: '<div>Not found :-(</div>'}},
        ],
        mode: 'history',
        base: `${locale}/`,
    });

    return new Vue({
        router,
        vuetify,
        i18n,
        render: h => h(App),
        ...opts,
    });

}