import { createStore } from 'vuex';
import api from '@/services/api';

export default createStore({
    state: {
        user: JSON.parse(localStorage.getItem('user')) || null,
        token: localStorage.getItem('token') || null,
        role: localStorage.getItem('role') || null,
    },
    getters: {
        isAuthenticated: (state) => !!state.token,
        currentUser: (state) => state.user,
        userRole: (state) => state.role,
    },
    mutations: {
        SET_USER(state, user) {
            state.user = user;
            state.role = user.role;
            localStorage.setItem('user', JSON.stringify(user));
            localStorage.setItem('role', user.role);
        },
        SET_TOKEN(state, token) {
            state.token = token;
            localStorage.setItem('token', token);
        },
        CLEAR_AUTH(state) {
            state.user = null;
            state.token = null;
            state.role = null;
            localStorage.removeItem('user');
            localStorage.removeItem('token');
            localStorage.removeItem('role');
        },
    },
    actions: {
        async login({ commit }, credentials) {
            try {
                const response = await api.post('/auth/login', credentials);
                const { token, ...user } = response.data;

                commit('SET_TOKEN', token);
                commit('SET_USER', user);
                return response.data;
            } catch (error) {
                throw error;
            }
        },
        async register({ commit }, userData) {
            try {
                const response = await api.post('/auth/register', userData);
                // Note: Register usually doesn't return token immediately in some flows, 
                // but if it does, we can set it. Based on backend analysis, it returns user info.
                // We might need to login after register or if backend returns token, use it.
                // Backend register returns: { message, id, email, role } - No token.
                return response.data;
            } catch (error) {
                throw error;
            }
        },
        logout({ commit }) {
            commit('CLEAR_AUTH');
            window.location.href = '/login';
        },
    },
});
