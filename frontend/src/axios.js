import axios from 'axios'

const getAPI = axios.create({
    baseURL: 'http://127.0.0.1:5000/classify',
    timeout: 1000,
})

export {
    getAPI
}