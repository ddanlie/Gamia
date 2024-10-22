import axios from "axios"

const api = axios.create({
    baseURL: 'http://192.168.0.108:5000/api/',
    timeout: 1000,
    responseType: 'json',
    withCredentials: true
    });

export default api