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
          <div class="card-header bg-white border-0 pt-4 px-4 pb-0">
            <h5 class="fw-bold mb-0 text-dark">Upcoming Appointments</h5>
          </div>
          <div class="card-body p-4">
            <div v-if="upcomingAppointments.length > 0" class="list-group list-group-flush">
              <div v-for="apt in upcomingAppointments.slice(0, 5)" :key="apt.id" 
                   class="list-group-item border-0 px-0 py-3 d-flex align-items-center justify-content-between">
                <div>
                  <p class="fw-bold mb-0 text-dark">{{ apt.patient?.user?.name || 'Unknown Patient' }}</p>
                  <small class="text-muted">{{ new Date(apt.appointment_date).toLocaleString() }}</small>
                </div>
                <span class="badge bg-primary bg-opacity-10 text-primary rounded-pill px-3 py-2">
                  {{ apt.status }}
                </span>
              </div>
            </div>
            <div v-else class="text-center py-5 text-muted">
              <p class="mb-0">No upcoming appointments found.</p>
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
import { ref, defineProps } from 'vue';
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

const store = useStore();
const showHistoryModal = ref(false);
const selectedPatient = ref(null);
const historyForm = ref({
  visit_type: 'Checkup',
  diagnosis: '',
  treatment: '',
  notes: ''
});

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
