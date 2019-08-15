import Vue from 'vue'
import Router from 'vue-router'
import store from '../store';

import HelloWorld from "../components/HelloWorld";
import Login from "../components/home/Login";
import UserHomepage from "../components/home/UserHomepage";

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
    {
        path: '/userhome',
        name: 'UserHome',
        component: UserHomepage,
    }
];

const router = new Router({
    mode: 'history',
    routes
});

export { router, routes }