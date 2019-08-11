import Vue from 'vue';
import Vuex from 'vuex';
import Es6Promise from 'es6-promise';
import DjangoAPI from '../services/api/DjangoService';

Es6Promise.polyfill();
Vue.use(Vuex);

export const state = {
    navBarVisible: false,
    user: null,
    username: null,
};

export const mutations = {
    toggleNavBar (state) {
        state.navBarVisible = !state.navBarVisible;
    },
    setUser (state, payload) {
        state.user = payload.username;
    },
};

export const actions = {
    submitLoginInfo(username, password) {

    },
    createNewUser({}, payload) {
        try {
            const response = DjangoAPI.createNewUser(payload);
            if (Promise.resolve(response).data === 'Success') {

            }
        } catch (e) {
            throw e;
        }
    },
};

export default new Vuex.Store({
    state,
    mutations,
    actions
})