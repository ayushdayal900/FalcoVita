<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">Manage Patients</h2>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          
          <!-- Enhanced Search -->
          <div class="card p-4 mb-6">
            <div class="flex gap-4">
              <input 
                type="text" 
                v-model="search" 
                placeholder="Search patients by name, email or medical record number..." 
                class="input"
                style="min-width: 400px; flex: 1;"
                @keyup.enter="performSearch"
              />
              <button @click="performSearch" class="btn btn-primary">Search</button>
              <button @click="clearSearch" class="btn btn-outline">Clear</button>
            </div>
          </div>

          <div v-if="loading" class="text-center py-10">
            <p class="text-muted">Loading patients...</p>
          </div>

          <div v-else-if="displayedPatients.length === 0" class="text-center py-10">
            <p class="text-muted">No patients found.</p>
          </div>

          <div v-else class="card overflow-hidden">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-50 text-muted text-sm border-b border-slate-200">
                  <th class="p-4 font-medium">Name</th>
                  <th class="p-4 font-medium">Email</th>
                  <th class="p-4 font-medium">Medical Record #</th>
                  <th class="p-4 font-medium">DOB</th>
                  <th class="p-4 font-medium">Contact</th>
                  <th class="p-4 font-medium">Status</th>
                  <th class="p-4 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="patient in displayedPatients" :key="patient.id" class="border-b border-slate-100 hover:bg-slate-50">
                  <td class="p-4 font-medium">{{ patient.user?.name || 'Patient' }}</td>
                  <td class="p-4 text-sm">{{ patient.user?.email }}</td>
                  <td class="p-4 text-sm">{{ patient.medical_record_number }}</td>
                  <td class="p-4 text-sm">{{ patient.dob ? new Date(patient.dob).toLocaleDateString() : '-' }}</td>
                  <td class="p-4 text-sm">{{ patient.contact }}</td>
                  <td class="p-4">
                    <span v-if="patient.user?.blacklisted" class="text-xs px-2 py-1 bg-red-100 text-red-600 rounded">Blocked</span>
                    <span v-else class="text-xs px-2 py-1 bg-green-100 text-green-600 rounded">Active</span>
                  </td>
                  <td class="p-4">
                    <div class="flex gap-2">
                      <button @click="viewHistory(patient)" class="text-primary hover:underline text-sm font-medium">View History</button>
                      <button @click="toggleBlock(patient)" class="text-orange-500 hover:underline text-sm font-medium">
                        {{ patient.user?.blacklisted ? 'Unblock' : 'Block' }}
                      </button>
                      <button @click="deletePatient(patient.id)" class="text-red-500 hover:underline text-sm font-medium">Delete</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>
      </div>
    </main>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Sidebar from '@/components/Sidebar.vue';
import api from '@/services/api';

const router = useRouter();
const patients = ref([]);
const loading = ref(true);
const search = ref('');
const searchActive = ref(false);

const fetchPatients = async () => {
  try {
    const response = await api.get('/patients/');
    patients.value = response.data;
  } catch (err) {
    console.error('Failed to fetch patients', err);
  } finally {
    loading.value = false;
  }
};

const displayedPatients = computed(() => {
  if (!search.value || !searchActive.value) return patients.value;
  const term = search.value.toLowerCase();
  return patients.value.filter(p => 
    (p.user?.name?.toLowerCase().includes(term)) ||
    (p.medical_record_number?.toLowerCase().includes(term)) ||
    (p.user?.email?.toLowerCase().includes(term))
  );
});

const performSearch = () => {
  if (search.value.trim()) {
    searchActive.value = true;
  }
};

const clearSearch = () => {
  search.value = '';
  searchActive.value = false;
};

const viewHistory = (patient) => {
  // Navigate to patient history view
  router.push(`/history?patient_id=${patient.id}`);
};

const toggleBlock = async (patient) => {
  const action = patient.user?.blacklisted ? 'unblock' : 'block';
  if (!confirm(`Are you sure you want to ${action} this patient?`)) return;
  
  try {
    if (patient.user?.blacklisted) {
      await api.delete(`/admin/blacklist/${patient.user.id}`);
    } else {
      await api.post(`/admin/blacklist/${patient.user.id}`);
    }
    alert(`Patient ${action}ed successfully`);
    fetchPatients();
  } catch (err) {
    alert(`Failed to ${action} patient`);
  }
};

const deletePatient = async (id) => {
  if (!confirm('Are you sure you want to delete this patient?')) return;
  try {
    await api.delete(`/admin/patients/${id}`);
    alert('Patient deleted successfully');
    fetchPatients();
  } catch (err) {
    alert('Failed to delete patient');
  }
};

onMounted(() => {
  fetchPatients();
});
</script>
