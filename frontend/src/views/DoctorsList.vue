<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <!-- Sidebar (Reused or Component) - For now, I'll copy the sidebar structure or better, I should have made a layout. 
         To save time and complexity, I will assume the Dashboard Layout is used as a wrapper or I'll just duplicate the sidebar for now 
         since I didn't create a Layout component yet. 
         Actually, I'll create a Layout component now to avoid duplication. -->
    
    <!-- I'll use the Dashboard.vue as the layout and use nested routes, but I defined routes as flat.
         I'll just duplicate the sidebar code for this task to ensure it works standalone, 
         or better, I'll refactor Dashboard to be a layout. 
         
         Let's stick to the plan: I'll create a Layout component first. -->
         
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

              <button class="btn btn-primary w-full mt-auto">
                Book Appointment
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
import Sidebar from '@/components/Sidebar.vue'; // I need to create this
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
    (doc.user?.name?.toLowerCase().includes(term)) || 
    (doc.specialization?.toLowerCase().includes(term))
  );
});

onMounted(() => {
  fetchDoctors();
});
</script>

<style scoped>
.bg-primary\/10 { background-color: rgba(99, 102, 241, 0.1); }
</style>
