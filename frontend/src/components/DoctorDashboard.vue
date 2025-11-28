<template>
  <div>
    <!-- Stats Grid -->
    <div class="row g-4 mb-4">
      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body p-4">
            <h6 class="text-muted text-uppercase small fw-bold mb-2">Today's Appointments</h6>
            <h2 class="display-6 fw-bold text-primary mb-0">{{ todayAppointments }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body p-4">
            <h6 class="text-muted text-uppercase small fw-bold mb-2">Total Patients</h6>
            <h2 class="display-6 fw-bold text-indigo mb-0" style="color: var(--bs-indigo);">{{ totalPatients }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body p-4">
            <h6 class="text-muted text-uppercase small fw-bold mb-2">Completed This Week</h6>
            <h2 class="display-6 fw-bold text-success mb-0">{{ weekCompleted }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-6 col-lg-3">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-body p-4">
            <h6 class="text-muted text-uppercase small fw-bold mb-2">Pending Requests</h6>
            <h2 class="display-6 fw-bold text-warning mb-0">0</h2>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-4">
      <!-- Upcoming Appointments -->
      <div class="col-lg-6">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0 pt-4 px-4 pb-0 d-flex justify-content-between align-items-center">
            <h5 class="fw-bold mb-0 text-dark">Upcoming Appointments</h5>
            <div class="btn-group btn-group-sm" role="group">
              <button 
                type="button" 
                :class="['btn', timeRange === 'today' ? 'btn-primary' : 'btn-outline-primary']"
                @click="changeTimeRange('today')"
              >
                Today
              </button>
              <button 
                type="button" 
                :class="['btn', timeRange === 'week' ? 'btn-primary' : 'btn-outline-primary']"
                @click="changeTimeRange('week')"
              >
                This Week
              </button>
            </div>
          </div>
          <div class="card-body p-4">
            <div v-if="upcomingAppointments.length > 0" class="list-group list-group-flush">
              <div v-for="apt in upcomingAppointments.slice(0, 5)" :key="apt.id" 
                   class="list-group-item border-0 px-0 py-3 d-flex align-items-center justify-content-between">
                <div>
                  <p class="fw-bold mb-0 text-dark">{{ apt.patient?.user?.name || 'Unknown Patient' }}</p>
                  <small class="text-muted">{{ formatDateTime(apt.appointment_date) }}</small>
                </div>
                <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill px-3 py-2">
                  {{ apt.status }}
                </span>
              </div>
            </div>
            <div v-else class="text-center py-5 text-muted">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" class="bi bi-calendar-x mb-3 opacity-50" viewBox="0 0 16 16">
                <path d="M6.146 7.146a.5.5 0 0 1 .708 0L8 8.293l1.146-1.147a.5.5 0 1 1 .708.708L8.707 9l1.147 1.146a.5.5 0 0 1-.708.708L8 9.707l-1.146 1.147a.5.5 0 0 1-.708-.708L7.293 9 6.146 7.854a.5.5 0 0 1 0-.708z"/>
                <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
              </svg>
              <p class="mb-0">No upcoming appointments {{ timeRange === 'today' ? 'today' : 'this week' }}.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Assigned Patients -->
      <div class="col-lg-6">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white border-0 pt-4 px-4 pb-0">
            <h5 class="fw-bold mb-0 text-dark">Assigned Patients</h5>
          </div>
          <div class="card-body p-4">
            <div v-if="patients.length > 0" class="list-group list-group-flush overflow-auto custom-scrollbar" style="max-height: 400px;">
              <div v-for="p in patients" :key="p.id" 
                   class="list-group-item border-0 px-0 py-3 d-flex align-items-center justify-content-between">
                <div>
                  <p class="fw-bold mb-0 text-dark">{{ p.patient?.user?.name || 'Unknown' }}</p>
                  <small class="text-muted">DOB: {{ p.patient?.date_of_birth || 'N/A' }}</small>
                </div>
                <button @click="openHistoryModal(p)" class="btn btn-sm btn-outline-primary rounded-pill px-3">
                  Update History
                </button>
              </div>
            </div>
            <div v-else class="text-center py-5 text-muted">
              <p class="mb-0">No patients assigned yet.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Update History Modal -->
    <div v-if="showHistoryModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-bottom-0 pb-0">
            <h5 class="modal-title fw-bold">Update Patient History</h5>
            <button type="button" class="btn-close" @click="closeHistoryModal"></button>
          </div>
          <div class="modal-body p-4">
            <p class="text-muted small mb-4">Adding record for: <span class="fw-bold text-dark">{{ selectedPatient?.patient?.user?.name }}</span></p>
            
            <form @submit.prevent="submitHistory">
              <div class="mb-3">
                <label class="form-label fw-bold small">Visit Type</label>
                <select v-model="historyForm.visit_type" class="form-select" required>
                  <option value="Checkup">Checkup</option>
                  <option value="Follow-up">Follow-up</option>
                  <option value="Emergency">Emergency</option>
                  <option value="Consultation">Consultation</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold small">Diagnosis</label>
                <input v-model="historyForm.diagnosis" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold small">Treatment Plan</label>
                <textarea v-model="historyForm.treatment" class="form-control" rows="3" required></textarea>
              </div>
              <div class="mb-4">
                <label class="form-label fw-bold small">Notes</label>
                <textarea v-model="historyForm.notes" class="form-control" rows="3"></textarea>
              </div>
              
              <div class="d-flex justify-content-end gap-2">
                <button type="button" @click="closeHistoryModal" class="btn btn-light">Cancel</button>
                <button type="submit" class="btn btn-primary fw-bold px-4">Save Record</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';
import { useStore } from 'vuex';
import api from '@/services/api';

const props = defineProps({
  todayAppointments: Number,
  totalPatients: Number,
  weekCompleted: Number,
  upcomingAppointments: Array,
  patients: {
    type: Array,
    default: () => []
  },
  departmentId: Number
});

const emit = defineEmits(['refresh-appointments']);

const store = useStore();
const showHistoryModal = ref(false);
const selectedPatient = ref(null);
const timeRange = ref('week');
const historyForm = ref({
  visit_type: 'Checkup',
  diagnosis: '',
  treatment: '',
  notes: ''
});

const changeTimeRange = (range) => {
  timeRange.value = range;
  emit('refresh-appointments', range);
};

const formatDateTime = (dateString) => {
  const date = new Date(dateString);
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  
  const dateStr = date.toLocaleDateString();
  const timeStr = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  if (date.toDateString() === today.toDateString()) {
    return `Today at ${timeStr}`;
  } else if (date.toDateString() === tomorrow.toDateString()) {
    return `Tomorrow at ${timeStr}`;
  } else {
    return `${dateStr} at ${timeStr}`;
  }
};

const openHistoryModal = (patient) => {
  selectedPatient.value = patient;
  historyForm.value = { visit_type: 'Checkup', diagnosis: '', treatment: '', notes: '' };
  showHistoryModal.value = true;
};

const closeHistoryModal = () => {
  showHistoryModal.value = false;
  selectedPatient.value = null;
};

const submitHistory = async () => {
  if (!selectedPatient.value) return;

  try {
    const doctorId = store.getters.currentUser?.id;
    
    if (!props.departmentId) {
        alert("Error: Doctor department not found. Please refresh.");
        return;
    }

    const combinedDiagnosis = `${historyForm.value.diagnosis}\n\nTreatment: ${historyForm.value.treatment}\n\nNotes: ${historyForm.value.notes}`;

    await api.post('/history/', {
      patient_id: selectedPatient.value.patient_id,
      doctor_id: doctorId,
      department_id: props.departmentId,
      visit_type: historyForm.value.visit_type,
      visit_date: new Date().toISOString(),
      diagnosis: combinedDiagnosis
    });

    alert('History updated successfully');
    closeHistoryModal();
  } catch (err) {
    console.error('Failed to update history', err);
    alert('Failed to update history: ' + (err.response?.data?.message || err.message));
  }
};
</script>

<style scoped>
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
