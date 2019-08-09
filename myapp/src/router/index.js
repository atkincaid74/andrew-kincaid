import Vue from 'vue'
import Router from 'vue-router'
import store from '../store';

import HelloWorld from "../components/HelloWorld";
import Login from "../components/home/Login";

Vue.use(Router);

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HelloWorld,
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
    },
];

const router = new Router({
    mode: 'history',
    routes
});

export { router, routes }