import axios from "axios"

const api = axios.create({
    baseURL: 'http://127.0.0.1:5000/api/',
    timeout: 1000,
    responseType: 'json'
    });

export default api