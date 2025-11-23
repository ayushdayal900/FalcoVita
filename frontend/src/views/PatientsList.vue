<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">My Patients</h2>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          
          <div class="mb-6">
            <input 
              type="text" 
              v-model="search" 
              placeholder="Search patients..." 
              class="input max-w-md"
            />
          </div>

          <div v-if="loading" class="text-center py-10">
            <p class="text-muted">Loading patients...</p>
          </div>

          <div v-else-if="filteredPatients.length === 0" class="text-center py-10">
            <p class="text-muted">No patients found.</p>
          </div>

          <div v-else class="card overflow-hidden">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-50 text-muted text-sm border-b border-slate-200">
                  <th class="p-4 font-medium">Name</th>
                  <th class="p-4 font-medium">Contact</th>
                  <th class="p-4 font-medium">Medical Record #</th>
                  <th class="p-4 font-medium">DOB</th>
                  <th class="p-4 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="patient in filteredPatients" :key="patient.id" class="border-b border-slate-100 hover:bg-slate-50">
                  <td class="p-4 font-medium">{{ patient.user?.name || 'Patient' }}</td>
                  <td class="p-4 text-sm">{{ patient.contact }}</td>
                  <td class="p-4 text-sm">{{ patient.medical_record_number }}</td>
                  <td class="p-4 text-sm">{{ patient.dob ? new Date(patient.dob).toLocaleDateString() : '-' }}</td>
                  <td class="p-4">
                    <button class="text-primary hover:underline text-sm font-medium">View History</button>
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
import Sidebar from '@/components/Sidebar.vue';
import api from '@/services/api';

const patients = ref([]);
const loading = ref(true);
const search = ref('');

const fetchPatients = async () => {
  try {
    // Ideally fetch only my patients, but for now fetch all
    const response = await api.get('/patients/');
    patients.value = response.data;
  } catch (err) {
    console.error('Failed to fetch patients', err);
  } finally {
    loading.value = false;
  }
};

const filteredPatients = computed(() => {
  if (!search.value) return patients.value;
  const term = search.value.toLowerCase();
  return patients.value.filter(p => 
    (p.user?.name?.toLowerCase().includes(term)) || 
    (p.medical_record_number?.toLowerCase().includes(term))
  );
});

onMounted(() => {
  fetchPatients();
});
</script>

<style scoped>
.bg-slate-50 { background-color: #f8fafc; }
.border-slate-200 { border-color: #e2e8f0; }
.border-slate-100 { border-color: #f1f5f9; }
.hover\:bg-slate-50:hover { background-color: #f8fafc; }
</style>
