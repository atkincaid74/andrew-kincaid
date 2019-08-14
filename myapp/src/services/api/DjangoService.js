import axios from 'axios';

export default {
    createNewUser(payload) {
        return axios
            .post('/api/create_user/', payload)
            .then(response => (response))
            .catch(err => {console.log(err); throw err.response})
    },
    getToken(payload) {
        return axios
            .post('/api/auth/', payload)
            .then(response => (response))
            .catch(err => {console.log(err); throw err.response})
    },
    getUserInfo(payload) {
        return axios
            .post('/api/get_user_info/', payload)
            .then(response => (response))
            .catch(err => {console.log(err); throw err.response})
    }
}
