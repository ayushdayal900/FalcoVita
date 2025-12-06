import axios from 'axios';
import store from '@/store';

const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = store.state.token;
        if (token) {
            config.headers['Authentication-Token'] = token;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle 401/403
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && (error.response.status === 401 || error.response.status === 403)) {
            store.dispatch('logout');
            // Optional: redirect to login
        }
        return Promise.reject(error);
    }
);

export default api;
