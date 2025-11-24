<template>
  <aside class="sidebar flex flex-col border-r border-slate-200 bg-white">
    <div class="p-6 border-b border-slate-100">
      <h1 class="text-xl font-bold text-primary">FalcoVita</h1>
      <p class="text-xs text-muted mt-1">Hospital Management</p>
    </div>

    <nav class="flex-1 p-4 space-y-2 overflow-y-auto">
      <!-- Admin Navigation -->
      <template v-if="userRole === 'admin'">
        <router-link to="/admin/dashboard" class="nav-item" active-class="active">
          <span>📊</span> Admin Dashboard
        </router-link>
        <router-link to="/doctors" class="nav-item" active-class="active">
          <span>👨‍⚕️</span> Manage Doctors
        </router-link>
        <router-link to="/patients" class="nav-item" active-class="active">
          <span>👥</span> Manage Patients
        </router-link>
        <router-link to="/appointments" class="nav-item" active-class="active">
          <span>📅</span> All Appointments
        </router-link>
      </template>
      
      <!-- Doctor Navigation -->
      <template v-if="userRole === 'doctor'">
        <router-link to="/dashboard" class="nav-item" active-class="active">
          <span>📊</span> Dashboard
        </router-link>
        <router-link to="/appointments" class="nav-item" active-class="active">
          <span>📅</span> My Appointments
        </router-link>
        <router-link to="/patients" class="nav-item" active-class="active">
          <span>👥</span> My Patients
        </router-link>
      </template>

      <!-- Patient Navigation -->
      <template v-if="userRole === 'patient'">
        <router-link to="/dashboard" class="nav-item" active-class="active">
          <span>🏠</span> Dashboard
        </router-link>
        <router-link to="/doctors" class="nav-item" active-class="active">
          <span>🔍</span> Find Doctors
        </router-link>
        <router-link to="/appointments" class="nav-item" active-class="active">
          <span>📅</span> My Appointments
        </router-link>
        <router-link to="/history" class="nav-item" active-class="active">
          <span>📋</span> Medical History
        </router-link>
      </template>
    </nav>

    <div class="p-4 border-t border-slate-100">
      <div class="flex items-center gap-3 mb-4">
        <div class="avatar bg-primary text-white rounded-full w-10 h-10 flex items-center justify-center font-bold">
          {{ userInitials }}
        </div>
        <div class="overflow-hidden flex-1">
          <p class="text-sm font-medium truncate">{{ userName }}</p>
          <p class="text-xs text-muted capitalize">{{ userRole }}</p>
        </div>
      </div>
      <button @click="logout" class="btn btn-outline w-full text-sm">
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
  background-color: var(--bg-card);
  box-shadow: var(--shadow-sm);
  z-index: 20;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem 1.25rem;
  border-radius: var(--radius-lg);
  color: var(--text-muted);
  font-weight: 500;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.nav-item span {
  font-size: 1.25rem;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.nav-item:hover {
  background-color: var(--slate-50);
  color: var(--slate-900);
}

.nav-item:hover span {
  opacity: 1;
}

.nav-item.active {
  background-color: var(--primary-50);
  color: var(--primary-700);
  font-weight: 600;
}

.nav-item.active span {
  opacity: 1;
}

.avatar {
  background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-800) 100%);
  box-shadow: var(--shadow-md);
}

.space-y-2 > * + * {
  margin-top: 0.25rem;
}

.border-r { border-right-width: 1px; }
.border-b { border-bottom-width: 1px; }
.border-t { border-top-width: 1px; }
.border-slate-200 { border-color: var(--slate-200); }
.border-slate-100 { border-color: var(--slate-100); }
.bg-white { background-color: var(--bg-card); }
.truncate { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.capitalize { text-transform: capitalize; }
.overflow-y-auto { overflow-y: auto; }
</style>