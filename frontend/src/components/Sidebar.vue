<template>
  <aside class="d-flex flex-column flex-shrink-0 p-3 bg-white border-end" style="width: 280px; height: 100vh; position: sticky; top: 0; z-index: 1000;">
    <a href="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none border-bottom pb-3 w-100">
      <div class="lh-1">
        <span class="fs-5 fw-bold text-dark">FalcoVita</span>
        <span class="d-block text-uppercase text-primary fw-bold" style="font-size: 0.65rem; letter-spacing: 1px;">Hospital System</span>
      </div>
    </a>

    <div class="overflow-auto flex-grow-1 custom-scrollbar">
      <ul class="nav nav-pills flex-column mb-auto">
        
        <!-- Admin Navigation -->
        <template v-if="userRole === 'admin'">
          <li class="nav-header text-muted text-uppercase fw-bold mt-3 mb-2 ps-3" style="font-size: 0.75rem;">Administration</li>
          <li class="nav-item">
            <router-link to="/admin/dashboard" class="nav-link link-dark" active-class="active">
              <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
              Dashboard
            </router-link>
          </li>
          <li>
            <router-link to="/doctors" class="nav-link link-dark" active-class="active">
              <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              Manage Doctors
            </router-link>
          </li>
          <li>
            <router-link to="/patients" class="nav-link link-dark" active-class="active">
              <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              Manage Patients
            </router-link>
          </li>
          <li>
            <router-link to="/appointments" class="nav-link link-dark" active-class="active">
              <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              All Appointments
            </router-link>
          </li>
        </template>

        <!-- Doctor Navigation -->
        <template v-if="userRole === 'doctor'">
          <li class="nav-header text-muted text-uppercase fw-bold mt-3 mb-2 ps-3" style="font-size: 0.75rem;">Practice</li>
          <li class="nav-item">
            <router-link to="/dashboard" class="nav-link link-dark" active-class="active">
              <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Dashboard
            </router-link>
          </li>
          <li>
            <router-link to="/appointments" class="nav-link link-dark" active-class="active">
              <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              My Schedule
            </router-link>
          </li>
          <li>
            <router-link to="/patients" class="nav-link link-dark" active-class="active">
              <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              My Patients
            </router-link>
          </li>
        </template>

        <!-- Patient Navigation -->
        <template v-if="userRole === 'patient'">
          <li class="nav-header text-muted text-uppercase fw-bold mt-3 mb-2 ps-3" style="font-size: 0.75rem;">Menu</li>
          <li class="nav-item">
            <router-link to="/dashboard" class="nav-link link-dark" active-class="active">
              <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Dashboard
            </router-link>
          </li>
          <li>
            <router-link to="/doctors" class="nav-link link-dark" active-class="active">
              <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              Find Doctors
            </router-link>
          </li>
          <li>
            <router-link to="/appointments" class="nav-link link-dark" active-class="active">
              <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              My Appointments
            </router-link>
          </li>
          <li>
            <router-link to="/history" class="nav-link link-dark" active-class="active">
              <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
              Medical History
            </router-link>
          </li>
        </template>
      </ul>
    </div>

    <div class="border-top pt-3 mt-3">
      <div class="d-flex align-items-center mb-3 px-2">
        <div class="flex-shrink-0">
          <div class="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center fw-bold shadow-sm" style="width: 38px; height: 38px;">
            {{ userInitials }}
          </div>
        </div>
        <div class="flex-grow-1 ms-3 overflow-hidden">
          <h6 class="mb-0 text-truncate text-dark fw-bold" style="font-size: 0.9rem;">{{ userName }}</h6>
          <div class="d-flex align-items-center mt-1">
            <span class="rounded-circle bg-success me-1" style="width: 8px; height: 8px;"></span>
            <small class="text-muted text-capitalize" style="font-size: 0.75rem;">{{ userRole }}</small>
          </div>
        </div>
      </div>
      <button @click="logout" class="btn btn-outline-danger w-100 btn-sm d-flex align-items-center justify-content-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="bi me-2" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
        Sign Out
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

const user = computed(() => store.getters.currentUser);
const userRole = computed(() => store.getters.userRole);
const userName = computed(() => user.value?.name || 'User');

const userInitials = computed(() => {
  const name = userName.value;
  return name ? name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() : 'U';
});

const logout = () => {
  store.dispatch('logout');
};
</script>

<style scoped>
.nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background-color: var(--bs-gray-100);
  color: var(--bs-primary) !important;
}

.nav-link.active {
  background-color: var(--bs-primary) !important;
  color: white !important;
  box-shadow: 0 4px 6px rgba(13, 110, 253, 0.2);
}

.nav-link.active svg {
  color: white;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.1);
  border-radius: 10px;
}

.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.2);
}
</style>