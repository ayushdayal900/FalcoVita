<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">Find a Doctor</h2>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          
          <!-- Search/Filter -->
          <div class="flex flex-col md:flex-row gap-4 mb-6">
            <SearchBar 
              v-model="search" 
              placeholder="Search by name or specialization..."
              @clear="search = ''"
              class="flex-1"
            />
            
            <div v-if="activeDepartmentId" class="flex items-center gap-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-lg border border-blue-200">
              <span class="text-sm font-medium">Filtered by Department</span>
              <button @click="clearDepartmentFilter" class="hover:text-blue-900">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>

          <div v-if="loading" class="text-center py-10">
            <p class="text-muted">Loading doctors...</p>
          </div>

          <div v-else-if="filteredDoctors.length === 0" class="text-center py-10">
            <p class="text-muted">No doctors found.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="doctor in filteredDoctors" :key="doctor.id" class="card p-6 flex flex-col">
              <div class="flex items-center gap-4 mb-4">
                <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-lg">
                  Dr
                </div>
                <div>
                  <h3 class="font-bold text-lg">{{ doctor.user?.name || 'Doctor' }}</h3>
                  <p class="text-sm text-primary">{{ doctor.specialization }}</p>
                </div>
              </div>
              
              <div class="space-y-2 mb-6 flex-1">
                <p class="text-sm text-muted">
                  <span class="font-medium text-main">Department:</span> {{ doctor.department?.name || 'General' }}
                </p>
                <p class="text-sm text-muted">
                  <span class="font-medium text-main">Experience:</span> {{ doctor.experience }} years
                </p>
                <p class="text-sm text-muted">
                  <span class="font-medium text-main">Qualifications:</span> {{ doctor.qualifications }}
                </p>
              </div>

              <div class="mt-auto">
                <button v-if="userRole === 'admin'" @click="openManageModal(doctor)" class="btn btn-primary w-full text-center">
                  Manage Doctor
                </button>
                <router-link v-else :to="`/doctors/${doctor.id}`" class="btn btn-primary w-full text-center">
                  View Profile & Book
                </router-link>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Manage Doctor Modal -->
    <div v-if="showManageModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="card bg-white w-full max-w-sm p-6">
        <h3 class="text-lg font-bold mb-4">Manage Dr. {{ selectedDoctor?.user?.name }}</h3>
        <div class="space-y-3">
          <button @click="editDoctor" class="btn btn-outline w-full justify-start">
            Edit Details
          </button>
          <button @click="toggleBlock" class="btn btn-outline w-full justify-start text-orange-600 border-orange-200 hover:bg-orange-50 hover:border-orange-600">
            {{ selectedDoctor?.user?.blacklisted ? 'Unblock' : 'Block' }} Doctor
          </button>
          <button @click="deleteDoctor" class="btn btn-outline w-full justify-start text-red-600 border-red-200 hover:bg-red-50 hover:border-red-600">
            Delete Doctor
          </button>
        </div>
        <div class="mt-6 flex justify-end">
          <button @click="closeManageModal" class="btn btn-ghost">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';
import Sidebar from '@/components/Sidebar.vue';
import SearchBar from '@/components/SearchBar.vue';
import api from '@/services/api';

const store = useStore();
const userRole = computed(() => store.getters.userRole);
const currentUser = computed(() => store.getters.currentUser);

const route = useRoute();
const router = useRouter();

const doctors = ref([]);
const loading = ref(true);
const search = ref('');
const showManageModal = ref(false);
const selectedDoctor = ref(null);
const activeDepartmentId = ref(route.query.department_id || null);

const fetchDoctors = async () => {
  try {
    loading.value = true;
    // Admin sees all (including blocked), Patients see only active (default backend behavior)
    let url = userRole.value === 'admin' ? '/doctors/?include_blocked=true' : '/doctors/';
    
    if (activeDepartmentId.value) {
      const separator = url.includes('?') ? '&' : '?';
      url += `${separator}department_id=${activeDepartmentId.value}`;
    }

    const response = await api.get(url);
    doctors.value = response.data;
  } catch (err) {
    console.error('Failed to fetch doctors', err);
  } finally {
    loading.value = false;
  }
};

const clearDepartmentFilter = () => {
  activeDepartmentId.value = null;
  router.replace({ query: {} });
  fetchDoctors();
};

const openManageModal = (doctor) => {
  selectedDoctor.value = doctor;
  showManageModal.value = true;
};

const closeManageModal = () => {
  showManageModal.value = false;
  selectedDoctor.value = null;
};

const editDoctor = () => {
  // Redirect to admin edit page or open edit modal
  // For now, let's just alert or redirect
  alert('Edit functionality is available in "Manage Doctors" page');
  closeManageModal();
};

const toggleBlock = async () => {
  if (!selectedDoctor.value) return;
  const action = selectedDoctor.value.user?.blacklisted ? 'unblock' : 'block';
  if (!confirm(`Are you sure you want to ${action} this doctor?`)) return;
  
  try {
    if (selectedDoctor.value.user?.blacklisted) {
      await api.delete(`/admin/blacklist/${selectedDoctor.value.user.id}`);
    } else {
      await api.post(`/admin/blacklist/${selectedDoctor.value.user.id}`);
    }
    alert(`Doctor ${action}ed successfully`);
    closeManageModal();
    fetchDoctors();
  } catch (err) {
    alert(`Failed to ${action} doctor`);
  }
};

const deleteDoctor = async () => {
  if (!selectedDoctor.value) return;
  if (!confirm('Are you sure you want to delete this doctor?')) return;
  try {
    await api.delete(`/admin/doctors/${selectedDoctor.value.id}`);
    alert('Doctor deleted successfully');
    closeManageModal();
    fetchDoctors();
  } catch (err) {
    alert('Failed to delete doctor');
  }
};

const filteredDoctors = computed(() => {
  if (!search.value) return doctors.value;
  const term = search.value.toLowerCase();
  return doctors.value.filter(doc => 
    (doc.user?.name && doc.user.name.toLowerCase().includes(term)) ||
    (doc.specialization && doc.specialization.toLowerCase().includes(term))
  );
});

onMounted(() => {
  fetchDoctors();
});
</script>

<style scoped>
.text-main { color: #1e293b; }
.text-muted { color: #64748b; }
.card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  border: 1px solid #e2e8f0;
}
.input {
  width: 100%;
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  outline: none;
}
.input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}
</style>
