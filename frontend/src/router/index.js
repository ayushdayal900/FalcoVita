import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';

import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import Dashboard from '@/views/Dashboard.vue';

const routes = [
    {
        path: '/',
        redirect: '/dashboard',
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { guest: true },
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        meta: { guest: true },
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard,
        meta: { requiresAuth: true },
    },
    {
        path: '/admin/dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/AdminDashboard.vue'),
        meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
        path: '/doctors',
        name: 'Doctors',
        component: () => import('@/views/DoctorsList.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/patients',
        name: 'Patients',
        component: () => import('@/views/PatientsList.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/appointments',
        name: 'Appointments',
        component: () => import('@/views/Appointments.vue'),
        meta: { requiresAuth: true },
    },
    {
        path: '/history',
        name: 'History',
        component: () => import('@/views/PatientHistory.vue'),
        meta: { requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

router.beforeEach((to, from, next) => {
    const isAuthenticated = store.getters.isAuthenticated;
    const userRole = store.getters.userRole;

    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (!isAuthenticated) {
            next('/login');
        } else if (to.matched.some((record) => record.meta.requiresAdmin)) {
            if (userRole === 'admin') {
                next();
            } else {
                next('/dashboard');
            }
        } else {
            next();
        }
    } else if (to.matched.some((record) => record.meta.guest)) {
        if (isAuthenticated) {
            // Redirect based on role
            if (userRole === 'admin') {
                next('/admin/dashboard');
            } else {
                next('/dashboard');
            }
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;