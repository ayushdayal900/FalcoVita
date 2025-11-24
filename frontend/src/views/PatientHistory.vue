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

          <div v-else class="space-y-6">
            <div v-for="record in history" :key="record.id" class="card p-6">
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
              
              <div class="mb-4">
                <h4 class="text-sm font-medium text-main mb-1">Diagnosis</h4>
                <p class="text-sm text-muted bg-slate-50 p-3 rounded border border-slate-100">
                  {{ record.diagnosis || 'No diagnosis recorded.' }}
                </p>
              </div>

              <!-- Prescriptions would go here if available in the record object or fetched separately -->
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
    await api.post(`/history/export/${currentUser.value.id}`);
    alert('Export started! You will receive an email shortly.');
  } catch (err) {
    console.error('Export failed', err);
    alert('Failed to start export.');
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
