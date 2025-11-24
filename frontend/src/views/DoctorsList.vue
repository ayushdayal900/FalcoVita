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
          <div class="mb-6 flex gap-4">
            <input 
              type="text" 
              v-model="search" 
              placeholder="Search by name or specialization..." 
              class="input max-w-md"
            />
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

              <router-link :to="`/doctors/${doctor.id}`" class="btn btn-primary w-full mt-auto text-center">
                View Profile & Book
              </router-link>
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
import api from '@/services/api';

const doctors = ref([]);
const loading = ref(true);
const search = ref('');

const fetchDoctors = async () => {
  try {
    const response = await api.get('/doctors/');
    doctors.value = response.data;
  } catch (err) {
    console.error('Failed to fetch doctors', err);
  } finally {
    loading.value = false;
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
