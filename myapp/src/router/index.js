import Vue from 'vue'
import Router from 'vue-router'
import store from '../store';

import App from "../App";

Vue.use(Router);

const routes = [
    {
        path: '/',
        name: 'Home',
        component: App,
    }
];

const router = new Router({
    mode: 'history',
    routes
});

export { router, routes }