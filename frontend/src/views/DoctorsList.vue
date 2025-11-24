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
          <SearchBar 
            v-model="search" 
            placeholder="Search by name or specialization..."
            @clear="search = ''"
          />

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
                <button v-if="userRole === 'admin'" @click="openManageModal(doctor)" class="btn btn-outline w-full text-center border-primary text-primary hover:bg-primary hover:text-white">
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
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import Sidebar from '@/components/Sidebar.vue';
import SearchBar from '@/components/SearchBar.vue';
import api from '@/services/api';

const store = useStore();
const userRole = computed(() => store.getters.userRole);
const currentUser = computed(() => store.getters.currentUser);

const doctors = ref([]);
const loading = ref(true);
const search = ref('');
const showManageModal = ref(false);
const selectedDoctor = ref(null);

const fetchDoctors = async () => {
  try {
    // Admin sees all (including blocked), Patients see only active (default backend behavior)
    const url = userRole.value === 'admin' ? '/doctors/?include_blocked=true' : '/doctors/';
    const response = await api.get(url);
    doctors.value = response.data;
  } catch (err) {
    console.error('Failed to fetch doctors', err);
  } finally {
    loading.value = false;
  }
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
