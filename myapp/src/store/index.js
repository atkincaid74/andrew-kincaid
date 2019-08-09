import Vue from 'vue';
import Vuex from 'vuex';
import Es6Promise from 'es6-promise';

Es6Promise.polyfill();
Vue.use(Vuex);

export const state = {
    navBarVisible: false,
    user: null,
    userName: null,
};

export const mutations = {
    toggleNavBar (state) {
        state.navBarVisible = !state.navBarVisible;
    }
};

export const actions = {

};

export default new Vuex.Store({
    state,
    mutations,
    actions
})