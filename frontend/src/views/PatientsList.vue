<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />
    
    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <!-- Header -->
      <header class="bg-white border-bottom py-3 px-4 d-flex align-items-center justify-content-between sticky-top z-2 shadow-sm">
        <div>
          <h2 class="h4 fw-bold text-dark mb-0">My Patients</h2>
          <p class="text-muted small mb-0">View and manage your patient records</p>
        </div>
      </header>

      <div class="flex-grow-1 overflow-auto p-4 custom-scrollbar">
        <div class="container-fluid p-0" style="max-width: 1400px;">
          
          <!-- Search Bar -->
          <div class="card border-0 shadow-sm mb-4" style="max-width: 600px;">
            <div class="card-body p-2">
              <SearchBar 
                v-model="search" 
                placeholder="Search patients by name or medical record number..."
                @clear="search = ''"
              />
            </div>
          </div>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary mb-3" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted fw-medium">Loading patients...</p>
          </div>

          <div v-else-if="filteredPatients.length === 0" class="text-center py-5 bg-white rounded-4 border border-dashed">
            <div class="bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 64px; height: 64px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-muted">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="h5 fw-bold text-dark mb-1">No patients found</h3>
            <p class="text-muted small">Try adjusting your search criteria.</p>
          </div>

          <div v-else class="row g-4">
            <div v-for="patient in filteredPatients" :key="patient.id" class="col-md-6 col-lg-4">
              <div class="card h-100 border-0 shadow-sm hover-lift overflow-hidden">
                <div class="card-body p-4 d-flex flex-column">
                  <div class="d-flex align-items-center gap-3 mb-4">
                    <div class="rounded-circle bg-primary bg-opacity-10 text-primary d-flex align-items-center justify-content-center fw-bold fs-4" style="width: 64px; height: 64px;">
                      {{ patient.user?.name?.charAt(0) }}
                    </div>
                    <div>
                      <h3 class="h5 fw-bold text-dark mb-1">{{ patient.user?.name || 'Patient' }}</h3>
                      <span class="badge bg-light text-primary border border-primary border-opacity-25 rounded-pill fw-normal px-3">
                        MRN: {{ patient.medical_record_number }}
                      </span>
                    </div>
                  </div>
                  
                  <div class="mb-4 flex-grow-1">
                    <div class="d-flex align-items-center gap-2 mb-2 text-muted small">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span class="fw-bold text-dark">DOB:</span> {{ patient.dob ? new Date(patient.dob).toLocaleDateString() : '-' }}
                    </div>
                    <div class="d-flex align-items-center gap-2 mb-2 text-muted small">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                      </svg>
                      <span class="fw-bold text-dark">Contact:</span> {{ patient.contact }}
                    </div>
                    <div class="d-flex align-items-center gap-2 text-muted small">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                      <span class="fw-bold text-dark">Email:</span> {{ patient.user?.email }}
                    </div>
                  </div>

                  <button @click="$router.push(`/history/${patient.id}`)" class="btn btn-primary w-full fw-bold shadow-sm mt-auto">
                    View History
                  </button>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import Sidebar from '@/components/Sidebar.vue';
import SearchBar from '@/components/SearchBar.vue';
import api from '@/services/api';

const patients = ref([]);
const loading = ref(true);
const search = ref('');

const store = useStore();
const userRole = computed(() => store.getters.userRole);
const currentUser = computed(() => store.getters.currentUser);

const fetchPatients = async () => {
  try {
    let url = '/patients/';
    if (userRole.value === 'doctor' && currentUser.value) {
      url += `?doctor_id=${currentUser.value.id}`;
    }
    const response = await api.get(url);
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
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-5px);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.175)!important;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.1);
  border-radius: 10px;
}

.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: rgba(0,0,0,0.2);
}
</style>
