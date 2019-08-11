import axios from 'axios';

export default {
    async createNewUser(payload) {
        try {
            return Promise.resolve(axios.post('/api/create_user/', payload))
        } catch(err) {
            throw Promise.reject(err)
        }
    },
}
