<template>
  <aside class="sidebar flex flex-col border-r border-slate-200 bg-white h-screen sticky top-0">
    <div class="p-6 border-b border-slate-100 flex items-center gap-3">
      <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-600 to-primary-800 flex items-center justify-center shadow-lg shadow-primary-500/30">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
        </svg>
      </div>
      <div>
        <h1 class="text-xl font-bold text-slate-900 tracking-tight">FalcoVita</h1>
        <p class="text-[10px] uppercase tracking-wider font-semibold text-primary-600">Hospital System</p>
      </div>
    </div>

    <nav class="flex-1 p-4 space-y-1 overflow-y-auto custom-scrollbar">
      <!-- Admin Navigation -->
      <template v-if="userRole === 'admin'">
        <div class="px-3 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">Administration</div>
        <router-link to="/admin/dashboard" class="nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
          </svg>
          Dashboard
        </router-link>
        <router-link to="/doctors" class="nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          Manage Doctors
        </router-link>
        <router-link to="/patients" class="nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          Manage Patients
        </router-link>
        <router-link to="/appointments" class="nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          All Appointments
        </router-link>
      </template>
      
      <!-- Doctor Navigation -->
      <template v-if="userRole === 'doctor'">
        <div class="px-3 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">Practice</div>
        <router-link to="/dashboard" class="nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Dashboard
        </router-link>
        <router-link to="/appointments" class="nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          My Schedule
        </router-link>
        <router-link to="/patients" class="nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          My Patients
        </router-link>
      </template>

      <!-- Patient Navigation -->
      <template v-if="userRole === 'patient'">
        <div class="px-3 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">Menu</div>
        <router-link to="/dashboard" class="nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Dashboard
        </router-link>
        <router-link to="/doctors" class="nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          Find Doctors
        </router-link>
        <router-link to="/appointments" class="nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          My Appointments
        </router-link>
        <router-link to="/history" class="nav-item" active-class="active">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
          Medical History
        </router-link>
      </template>
    </nav>

    <div class="p-4 border-t border-slate-100 bg-slate-50/50">
      <div class="flex items-center gap-3 mb-4 p-2 rounded-lg hover:bg-white transition-colors">
        <div class="avatar bg-gradient-to-br from-primary-500 to-primary-700 text-white rounded-full w-10 h-10 flex items-center justify-center font-bold shadow-md text-sm">
          {{ userInitials }}
        </div>
        <div class="overflow-hidden flex-1">
          <p class="text-sm font-bold text-slate-800 truncate">{{ userName }}</p>
          <p class="text-xs text-slate-500 capitalize flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            {{ userRole }}
          </p>
        </div>
      </div>
      <button @click="logout" class="btn btn-outline w-full text-sm hover:bg-red-50 hover:text-red-600 hover:border-red-200 group transition-all">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 group-hover:text-red-600 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
.sidebar {
  width: 280px;
  background-color: #ffffff;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.02);
  z-index: 20;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  color: var(--slate-500);
  font-weight: 500;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  position: relative;
}

.icon {
  width: 1.25rem;
  height: 1.25rem;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background-color: var(--slate-50);
  color: var(--slate-900);
}

.nav-item:hover .icon {
  color: var(--primary-600);
  transform: scale(1.1);
}

.nav-item.active {
  background-color: var(--primary-50);
  color: var(--primary-700);
  font-weight: 600;
}

.nav-item.active .icon {
  color: var(--primary-600);
}

/* Active indicator line */
.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  height: 1.5rem;
  width: 3px;
  background-color: var(--primary-600);
  border-radius: 0 4px 4px 0;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: var(--slate-200);
  border-radius: 4px;
}

.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background: var(--slate-300);
}
</style>