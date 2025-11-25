<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">Medical History</h2>
        <button @click="exportHistory" class="btn btn-primary text-sm">
          Export CSV
        </button>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          
          <div v-if="loading" class="text-center py-10">
            <p class="text-muted">Loading history...</p>
          </div>

          <div v-else-if="history.length === 0" class="text-center py-10">
            <p class="text-muted">No medical history found.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="record in history" :key="record.id" class="card p-6 flex flex-col h-full hover:shadow-md transition-shadow">
              <div class="flex justify-between items-start mb-4">
                <div>
                  <h3 class="text-lg font-bold text-primary">{{ record.visit_type }}</h3>
                  <p class="text-sm text-muted">{{ new Date(record.visit_date).toLocaleDateString() }}</p>
                </div>
                <div class="text-right">
                  <p class="text-sm font-medium">{{ record.doctor?.user?.name || 'Doctor' }}</p>
                  <p class="text-xs text-muted">{{ record.department?.name }}</p>
                </div>
              </div>
              
              <div class="mb-4 flex-1">
                <h4 class="text-sm font-medium text-main mb-1">Diagnosis</h4>
                <p class="text-sm text-muted bg-slate-50 p-3 rounded border border-slate-100 h-full">
                  {{ record.diagnosis || 'No diagnosis recorded.' }}
                </p>
              </div>

              <div v-if="record.prescriptions && record.prescriptions.length > 0" class="mt-4 pt-4 border-t border-slate-100">
                <h4 class="text-sm font-medium text-main mb-2">Prescription</h4>
                <div v-for="rx in record.prescriptions" :key="rx.id" class="bg-blue-50 p-3 rounded border border-blue-100 text-sm">
                  <div class="grid grid-cols-1 gap-2">
                    <div>
                      <span class="text-xs text-muted block">Medicines</span>
                      <span class="font-medium text-slate-700">{{ rx.medicines }}</span>
                    </div>
                    <div>
                      <span class="text-xs text-muted block">Dosage</span>
                      <span class="font-medium text-slate-700">{{ rx.dosage }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="mt-4 pt-4 border-t border-slate-100 text-sm text-muted italic">
                No prescription recorded.
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
import Sidebar from '@/components/Sidebar.vue';
import api from '@/services/api';

const store = useStore();
const history = ref([]);
const loading = ref(true);
const currentUser = computed(() => store.getters.currentUser);

const fetchHistory = async () => {
  try {
    if (!currentUser.value) return;
    // Fetch history for the specific patient
    const response = await api.get(`/history/patient/${currentUser.value.id}`);
    history.value = response.data;
  } catch (err) {
    console.error('Failed to fetch history', err);
  } finally {
    loading.value = false;
  }
};

const exportHistory = async () => {
  try {
    if (!currentUser.value) return;
    
    // Make GET request with blob response type
    const response = await api.get(`/history/export/${currentUser.value.id}`, {
      responseType: 'blob'
    });
    
    // Create blob URL and trigger download
    const blob = new Blob([response.data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `patient_${currentUser.value.id}_history.csv`;
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
.text-main { color: #1e293b; }
.text-muted { color: #64748b; }
.card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  border: 1px solid #e2e8f0;
}
</style>
