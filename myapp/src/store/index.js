import Vue from 'vue';
import Vuex from 'vuex';
import Es6Promise from 'es6-promise';
import DjangoAPI from '../services/api/DjangoService';

Es6Promise.polyfill();
Vue.use(Vuex);

export const state = {
    navBarVisible: false,
    username: null,
    userFirstName: '',
    userLastName: '',
    userPaid: false,
    displaySnackbar: false,
    snackbarMessage: '',
    snackbarColor: 'error',
};

export const mutations = {
    toggleNavBar (state) {
        state.navBarVisible = !state.navBarVisible;
    },
    setUser (state, payload) {
        state.username = payload;
    },
    setUserFirstName (state, payload) {
        state.userFirstName = payload;
    },
    setUserLastName (state, payload) {
        state.userLastName = payload;
    },
    setUserPaid (state, payload) {
        state.userPaid = payload;
    },
    toggleDisplaySnackbar (state) {
        state.displaySnackbar = !state.displaySnackbar;
    },
    setSnackbarMessage (state, payload) {
        state.snackbarMessage = payload;
    },
    setSnackbarColor (state, payload) {
        state.snackbarColor = payload;
    },
};

export const actions = {
    submitLoginInfo(username, password) {

    },
    async createNewUser({ commit, state }, payload) {
        const response = await DjangoAPI.createNewUser(payload);
        console.log(response);
        const data = response.data;

        if (data === 'Success') {
            commit('setUser', payload.username);
            commit('setUserFirstName', payload.firstName);
            commit('setUserLastName', payload.lastName);
        } else if (data.startsWith('Email already')) {
            commit('setSnackbarMessage', 'Email already associated with an account');
            commit('setSnackbarColor', 'error');
            commit('toggleDisplaySnackbar');
        } else if (data.startsWith('Username')) {
            commit('setSnackbarMessage', 'Username already taken');
            commit('setSnackbarColor', 'error');
            commit('toggleDisplaySnackbar');
        } else {
            commit('setSnackbarMessage', 'Email hasn\'t been approved. Email nflpickem6.9@gmail.com with problems.');
            commit('setSnackbarColor', 'error');
            commit('toggleDisplaySnackbar');
        }
    },
};

export default new Vuex.Store({
    state,
    mutations,
    actions
})