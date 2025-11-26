<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />
    
    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <!-- Header -->
      <header class="bg-white border-bottom py-3 px-4 d-flex align-items-center justify-content-between sticky-top z-2 shadow-sm">
        <div>
          <h2 class="h4 fw-bold text-dark mb-0">Medical History</h2>
          <p class="text-muted small mb-0">View your past visits and records</p>
        </div>
        <button @click="exportHistory" class="btn btn-primary d-flex align-items-center gap-2 shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Export CSV
        </button>
      </header>

      <div class="flex-grow-1 overflow-auto p-4 custom-scrollbar">
        <div class="container-fluid p-0" style="max-width: 1400px;">
          
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary mb-3" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted fw-medium">Loading history...</p>
          </div>

          <div v-else-if="history.length === 0" class="text-center py-5 bg-white rounded-4 border border-dashed">
            <div class="bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 64px; height: 64px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-muted">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="h5 fw-bold text-dark mb-1">No medical history found</h3>
            <p class="text-muted small">You don't have any past medical records.</p>
          </div>

          <div v-else class="row g-4">
            <div v-for="record in history" :key="record.id" class="col-md-6 col-lg-4">
              <div class="card h-100 border-0 shadow-sm hover-lift">
                <div class="card-header bg-white border-bottom-0 pt-4 px-4 pb-0 d-flex justify-content-between align-items-start">
                  <div>
                    <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill mb-2 px-3">
                      {{ record.visit_type }}
                    </span>
                    <h3 class="h5 fw-bold text-dark mb-1">{{ new Date(record.visit_date).toLocaleDateString() }}</h3>
                  </div>
                  <div class="text-end">
                    <p class="fw-bold text-dark small mb-0">{{ record.doctor?.user?.name || 'Doctor' }}</p>
                    <p class="text-muted small mb-0">{{ record.department?.name }}</p>
                  </div>
                </div>
                
                <div class="card-body p-4 d-flex flex-column">
                  <div class="mb-4 flex-grow-1">
                    <h6 class="text-uppercase text-muted small fw-bold mb-2">Diagnosis</h6>
                    <div class="bg-light p-3 rounded-3 border border-light">
                      <p class="mb-0 text-dark small">{{ record.diagnosis || 'No diagnosis recorded.' }}</p>
                    </div>
                  </div>

                  <div class="pt-3 border-top">
                    <h6 class="text-uppercase text-muted small fw-bold mb-2">Prescription</h6>
                    <div v-if="record.prescriptions && record.prescriptions.length > 0">
                      <div v-for="rx in record.prescriptions" :key="rx.id" class="bg-primary bg-opacity-10 p-3 rounded-3 border border-primary border-opacity-10 mb-2 last:mb-0">
                        <div class="row g-2">
                          <div class="col-12">
                            <span class="text-uppercase text-primary small fw-bold d-block" style="font-size: 0.7rem;">Medicines</span>
                            <span class="fw-bold text-dark small">{{ rx.medicines }}</span>
                          </div>
                          <div class="col-12">
                            <span class="text-uppercase text-primary small fw-bold d-block" style="font-size: 0.7rem;">Dosage</span>
                            <span class="fw-bold text-dark small">{{ rx.dosage }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div v-else class="text-muted small fst-italic">
                      No prescription recorded.
                    </div>
                  </div>
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
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';
import Sidebar from '@/components/Sidebar.vue';
import api from '@/services/api';

const store = useStore();
const route = useRoute();
const history = ref([]);
const loading = ref(true);
const currentUser = computed(() => store.getters.currentUser);

const fetchHistory = async () => {
  try {
    const patientId = route.params.patientId || (currentUser.value ? currentUser.value.id : null);
    if (!patientId) return;

    // Fetch history for the specific patient
    const response = await api.get(`/history/patient/${patientId}`);
    history.value = response.data;
  } catch (err) {
    console.error('Failed to fetch history', err);
  } finally {
    loading.value = false;
  }
};

const exportHistory = async () => {
  try {
    const patientId = route.params.patientId || (currentUser.value ? currentUser.value.id : null);
    if (!patientId) return;
    
    // Make GET request with blob response type
    const response = await api.get(`/history/export/${patientId}`, {
      responseType: 'blob'
    });
    
    // Create blob URL and trigger download
    const blob = new Blob([response.data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `patient_${patientId}_history.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    alert('CSV file downloaded successfully!');
  } catch (err) {
    console.error('Export failed', err);
    alert('Failed to export CSV.');
  }
};

onMounted(() => {
  fetchHistory();
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
