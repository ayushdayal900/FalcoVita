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
        isAdmin: (state) => state.role === 'admin',
        isDoctor: (state) => state.role === 'doctor',
        isPatient: (state) => state.role === 'patient',
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
                const data = response.data;
                
                // Backend returns: { message, id, email, name, role, token }
                if (data.token) {
                    commit('SET_TOKEN', data.token);
                    commit('SET_USER', {
                        id: data.id,
                        email: data.email,
                        name: data.name,
                        role: data.role
                    });
                }
                
                return data;
            } catch (error) {
                throw error;
            }
        },
        async register({ commit }, userData) {
            try {
                const response = await api.post('/auth/register', userData);
                // Backend register returns: { message, id, email, role }
                // User needs to login after registration
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