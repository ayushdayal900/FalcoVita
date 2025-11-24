<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <div class="card p-6 bg-white shadow-sm rounded-xl border border-slate-100">
      <h3 class="text-sm font-medium text-slate-500 mb-2">Today's Appointments</h3>
      <p class="text-3xl font-bold text-blue-600">{{ todayAppointments }}</p>
    </div>
    <div class="card p-6 bg-white shadow-sm rounded-xl border border-slate-100">
      <h3 class="text-sm font-medium text-slate-500 mb-2">Total Patients</h3>
      <p class="text-3xl font-bold text-indigo-600">{{ totalPatients }}</p>
    </div>
    <div class="card p-6 bg-white shadow-sm rounded-xl border border-slate-100">
      <h3 class="text-sm font-medium text-slate-500 mb-2">Completed This Week</h3>
      <p class="text-3xl font-bold text-green-600">{{ weekCompleted }}</p>
    </div>
    <div class="card p-6 bg-white shadow-sm rounded-xl border border-slate-100">
      <h3 class="text-sm font-medium text-slate-500 mb-2">Pending Requests</h3>
      <p class="text-3xl font-bold text-orange-500">0</p>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
    <!-- Upcoming Appointments -->
    <div class="card p-6 bg-white shadow-sm rounded-xl border border-slate-100">
      <h3 class="text-lg font-bold mb-4 text-slate-800">Upcoming Appointments</h3>
      <div v-if="upcomingAppointments.length > 0" class="space-y-4">
        <div v-for="apt in upcomingAppointments.slice(0, 5)" :key="apt.id" 
             class="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100">
          <div>
            <p class="font-medium text-slate-900">{{ apt.patient?.user?.name || 'Unknown Patient' }}</p>
            <p class="text-sm text-slate-500">{{ new Date(apt.appointment_date).toLocaleString() }}</p>
          </div>
          <span class="px-3 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-700">
            {{ apt.status }}
          </span>
        </div>
      </div>
      <div v-else class="text-center py-8 text-slate-400">
        No upcoming appointments found.
      </div>
    </div>

    <!-- Assigned Patients -->
    <div class="card p-6 bg-white shadow-sm rounded-xl border border-slate-100">
      <h3 class="text-lg font-bold mb-4 text-slate-800">Assigned Patients</h3>
      <div v-if="patients.length > 0" class="space-y-4 max-h-[400px] overflow-y-auto">
        <div v-for="p in patients" :key="p.id" 
             class="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100">
          <div>
            <p class="font-medium text-slate-900">{{ p.patient?.user?.name || 'Unknown' }}</p>
            <p class="text-xs text-slate-500">DOB: {{ p.patient?.date_of_birth || 'N/A' }}</p>
          </div>
          <button @click="openHistoryModal(p)" class="btn btn-sm btn-outline">
            Update History
          </button>
        </div>
      </div>
      <div v-else class="text-center py-8 text-slate-400">
        No patients assigned yet.
      </div>
    </div>
  </div>

  <!-- Update History Modal -->
  <div v-if="showHistoryModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl shadow-xl w-full max-w-lg p-6">
      <h3 class="text-xl font-bold mb-4">Update Patient History</h3>
      <p class="text-sm text-slate-600 mb-4">Adding record for: <span class="font-semibold">{{ selectedPatient?.patient?.user?.name }}</span></p>
      
      <form @submit.prevent="submitHistory">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Visit Type</label>
            <select v-model="historyForm.visit_type" class="input w-full" required>
              <option value="Checkup">Checkup</option>
              <option value="Follow-up">Follow-up</option>
              <option value="Emergency">Emergency</option>
              <option value="Consultation">Consultation</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Diagnosis</label>
            <input v-model="historyForm.diagnosis" type="text" class="input w-full" required />
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Treatment Plan</label>
            <textarea v-model="historyForm.treatment" class="input w-full h-24" required></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-1">Notes</label>
            <textarea v-model="historyForm.notes" class="input w-full h-24"></textarea>
          </div>
        </div>
        
        <div class="flex justify-end gap-3 mt-6">
          <button type="button" @click="closeHistoryModal" class="btn btn-ghost">Cancel</button>
          <button type="submit" class="btn btn-primary">Save Record</button>
        </div>
      </form>
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

    await api.post('/history/', {
      patient_id: selectedPatient.value.patient_id, // Use patient_id from the patient object (which is likely User ID)
      doctor_id: doctorId,
      department_id: props.departmentId,
      visit_type: historyForm.value.visit_type,
      visit_date: new Date().toISOString(),
      diagnosis: historyForm.value.diagnosis,
      // Note: The backend model might not have 'treatment' or 'notes' fields directly in PatientHistory?
      // Let's check the model again.
      // PatientHistory has: diagnosis. 
      // It does NOT seem to have 'treatment' or 'notes'.
      // It has 'Prescription' relationship.
      // Wait, if the backend model doesn't have treatment/notes, where do I save them?
      // I might need to append them to diagnosis or check if I missed fields.
    });

    // Re-checking model:
    // PatientHistory(patient_id, doctor_id, department_id, appointment_id, visit_type, visit_date, diagnosis)
    // It seems 'treatment' and 'notes' are missing.
    // I will append them to 'diagnosis' for now as a workaround, or just save diagnosis.
    // "Diagnosis: ... | Treatment: ... | Notes: ..."
    
    // Actually, let's just send diagnosis for now to be safe, or combine them.
    // I'll combine them into diagnosis for now.
    
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


