import axios from 'axios';

export default {
    createNewUser(payload) {
        return axios
            .post('/api/create_user/', payload)
            .then(response => (response))
            .catch(err => {console.log(err); throw err.response})
    },
}
