<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">My Patients</h2>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          
          <SearchBar 
            v-model="search" 
            placeholder="Search patients by name or medical record number..."
            @clear="search = ''"
          />

          <div v-if="loading" class="text-center py-10">
            <p class="text-muted">Loading patients...</p>
          </div>

          <div v-else-if="filteredPatients.length === 0" class="text-center py-10">
            <p class="text-muted">No patients found.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="patient in filteredPatients" :key="patient.id" class="card p-6 flex flex-col">
              <div class="flex items-center gap-4 mb-4">
                <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold text-lg">
                  Pt
                </div>
                <div>
                  <h3 class="font-bold text-lg">{{ patient.user?.name || 'Patient' }}</h3>
                  <p class="text-sm text-primary">MRN: {{ patient.medical_record_number }}</p>
                </div>
              </div>
              
              <div class="space-y-2 mb-6 flex-1">
                <p class="text-sm text-muted">
                  <span class="font-medium text-main">DOB:</span> {{ patient.dob ? new Date(patient.dob).toLocaleDateString() : '-' }}
                </p>
                <p class="text-sm text-muted">
                  <span class="font-medium text-main">Contact:</span> {{ patient.contact }}
                </p>
                <p class="text-sm text-muted">
                  <span class="font-medium text-main">Email:</span> {{ patient.user?.email }}
                </p>
              </div>

              <button class="btn btn-primary w-full mt-auto text-center">
                View History
              </button>
            </div>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Sidebar from '@/components/Sidebar.vue';
import SearchBar from '@/components/SearchBar.vue';
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
.text-main { color: #1e293b; }
.text-muted { color: #64748b; }
.card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  border: 1px solid #e2e8f0;
}
</style>
