<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">Admin Dashboard</h2>
        <div class="flex gap-2">
          <button @click="showDepartmentModal = true" class="btn btn-outline text-sm">
            Manage Departments
          </button>
        </div>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          
          <!-- Statistics Cards -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
            <div class="card p-6">
              <h3 class="text-sm font-medium text-muted mb-2">Total Doctors</h3>
              <p class="text-3xl font-bold text-primary">{{ stats.total_doctors }}</p>
            </div>
            <div class="card p-6">
              <h3 class="text-sm font-medium text-muted mb-2">Total Patients</h3>
              <p class="text-3xl font-bold text-secondary">{{ stats.total_patients }}</p>
            </div>
            <div class="card p-6">
              <h3 class="text-sm font-medium text-muted mb-2">Total Appointments</h3>
              <p class="text-3xl font-bold">{{ stats.total_appointments }}</p>
            </div>
            <div class="card p-6">
              <h3 class="text-sm font-medium text-muted mb-2">Upcoming</h3>
              <p class="text-3xl font-bold text-green-600">{{ stats.upcoming_appointments }}</p>
            </div>
          </div>

          <!-- Search -->
          <div class="card p-4 mb-6">
            <div class="flex gap-4">
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="Search doctors or patients..." 
                class="input flex-1"
                @keyup.enter="performSearch"
              />
              <select v-model="searchType" class="input w-40">
                <option value="all">All</option>
                <option value="doctor">Doctors</option>
                <option value="patient">Patients</option>
              </select>
              <button @click="performSearch" class="btn btn-primary">Search</button>
            </div>
          </div>

          <!-- Search Results -->
          <div v-if="searchResults" class="mb-6">
            <div v-if="searchResults.doctors.length > 0" class="card p-6 mb-4">
              <h3 class="text-lg font-bold mb-4">Doctors</h3>
              <div class="space-y-2">
                <div v-for="doc in searchResults.doctors" :key="doc.id" 
                     class="flex justify-between items-center p-3 bg-slate-50 rounded">
                  <div>
                    <p class="font-medium">{{ doc.name }}</p>
                    <p class="text-sm text-muted">{{ doc.email }}</p>
                  </div>
                  <div class="flex gap-2">
                    <button @click="editDoctor(doc)" class="btn btn-outline text-sm">Edit</button>
                    <button @click="deleteDoctor(doc.id)" class="btn btn-outline text-sm text-red-500">Delete</button>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="searchResults.patients.length > 0" class="card p-6">
              <h3 class="text-lg font-bold mb-4">Patients</h3>
              <div class="space-y-2">
                <div v-for="pat in searchResults.patients" :key="pat.id" 
                     class="flex justify-between items-center p-3 bg-slate-50 rounded">
                  <div>
                    <p class="font-medium">{{ pat.name }}</p>
                    <p class="text-sm text-muted">{{ pat.email }}</p>
                  </div>
                  <div class="flex gap-2">
                    <button @click="editPatient(pat)" class="btn btn-outline text-sm">Edit</button>
                    <button @click="deletePatient(pat.id)" class="btn btn-outline text-sm text-red-500">Delete</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="card p-6">
              <h3 class="text-lg font-bold mb-4">Doctors</h3>
              <p class="text-muted text-sm mb-4">Manage doctor accounts and profiles</p>
              <router-link to="/admin/doctors" class="btn btn-primary w-full text-sm">
                Manage Doctors
              </router-link>
            </div>

            <div class="card p-6">
              <h3 class="text-lg font-bold mb-4">Patients</h3>
              <p class="text-muted text-sm mb-4">View and manage patient records</p>
              <router-link to="/admin/patients" class="btn btn-primary w-full text-sm">
                Manage Patients
              </router-link>
            </div>

            <div class="card p-6">
              <h3 class="text-lg font-bold mb-4">Appointments</h3>
              <p class="text-muted text-sm mb-4">View all appointments system-wide</p>
              <router-link to="/appointments" class="btn btn-primary w-full text-sm">
                View All
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Department Modal -->
    <div v-if="showDepartmentModal" class="modal-overlay">
      <div class="card bg-white w-full max-w-2xl p-6 max-h-[80vh] overflow-y-auto">
        <h3 class="text-lg font-bold mb-4">Manage Departments</h3>
        
        <!-- Add Department Form -->
        <form @submit.prevent="addDepartment" class="mb-6 p-4 bg-slate-50 rounded">
          <div class="grid grid-cols-2 gap-4">
            <input v-model="newDept.name" placeholder="Department Name" class="input" required />
            <input v-model="newDept.overview" placeholder="Overview" class="input" />
          </div>
          <button type="submit" class="btn btn-primary text-sm mt-2">Add Department</button>
        </form>

        <!-- Departments List -->
        <div class="space-y-2">
          <div v-for="dept in departments" :key="dept.id" 
               class="flex justify-between items-center p-3 border rounded">
            <div>
              <p class="font-medium">{{ dept.name }}</p>
              <p class="text-sm text-muted">{{ dept.doctor_count }} doctors</p>
            </div>
            <button @click="deleteDepartment(dept.id)" 
                    class="text-red-500 hover:underline text-sm"
                    :disabled="dept.doctor_count > 0">
              Delete
            </button>
          </div>
        </div>

        <button @click="showDepartmentModal = false" class="btn btn-outline w-full mt-4">Close</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Sidebar from '@/components/Sidebar.vue';
import api from '@/services/api';

const stats = ref({
  total_doctors: 0,
  total_patients: 0,
  total_appointments: 0,
  upcoming_appointments: 0
});

const searchQuery = ref('');
const searchType = ref('all');
const searchResults = ref(null);

const showDepartmentModal = ref(false);
const departments = ref([]);
const newDept = ref({ name: '', overview: '' });

const fetchStats = async () => {
  try {
    const response = await api.get('/admin/dashboard');
    stats.value = response.data;
  } catch (err) {
    console.error('Failed to fetch stats', err);
  }
};

const performSearch = async () => {
  if (!searchQuery.value.trim()) return;
  
  try {
    const response = await api.get('/admin/search', {
      params: { q: searchQuery.value, type: searchType.value }
    });
    searchResults.value = response.data;
  } catch (err) {
    console.error('Search failed', err);
  }
};

const fetchDepartments = async () => {
  try {
    const response = await api.get('/departments/');
    departments.value = response.data;
  } catch (err) {
    console.error(err);
  }
};

const addDepartment = async () => {
  try {
    await api.post('/departments/', newDept.value);
    newDept.value = { name: '', overview: '' };
    fetchDepartments();
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to add department');
  }
};

const deleteDepartment = async (id) => {
  if (!confirm('Delete this department?')) return;
  try {
    await api.delete(`/departments/${id}`);
    fetchDepartments();
  } catch (err) {
    alert(err.response?.data?.message || 'Cannot delete department');
  }
};

const deleteDoctor = async (id) => {
  if (!confirm('Delete this doctor?')) return;
  try {
    await api.delete(`/admin/doctors/${id}`);
    performSearch();
    fetchStats();
  } catch (err) {
    alert('Failed to delete doctor');
  }
};

const deletePatient = async (id) => {
  if (!confirm('Delete this patient?')) return;
  try {
    await api.delete(`/admin/patients/${id}`);
    performSearch();
    fetchStats();
  } catch (err) {
    alert('Failed to delete patient');
  }
};

onMounted(() => {
  fetchStats();
  fetchDepartments();
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
}

.text-secondary { color: var(--secondary); }
.text-green-600 { color: #16a34a; }
.text-red-500 { color: #ef4444; }
.max-h-\[80vh\] { max-height: 80vh; }
</style>