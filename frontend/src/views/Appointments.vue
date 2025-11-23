<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">Appointments</h2>
        <button v-if="userRole === 'patient'" @click="showBookModal = true" class="btn btn-primary text-sm">
          Book Appointment
        </button>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          
          <div v-if="loading" class="text-center py-10">
            <p class="text-muted">Loading appointments...</p>
          </div>

          <div v-else-if="appointments.length === 0" class="text-center py-10">
            <p class="text-muted">No appointments found.</p>
          </div>

          <div v-else class="space-y-4">
            <div v-for="appt in appointments" :key="appt.id" class="card p-4 flex items-center justify-between">
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-muted font-bold">
                  {{ getInitials(appt) }}
                </div>
                <div>
                  <h3 class="font-bold text-main">
                    {{ userRole === 'doctor' ? appt.patient?.user?.name : appt.doctor?.user?.name }}
                  </h3>
                  <p class="text-sm text-muted">
                    {{ new Date(appt.appointment_date).toLocaleString() }}
                  </p>
                  <p class="text-xs text-primary font-medium mt-1 uppercase tracking-wide">{{ appt.status }}</p>
                </div>
              </div>
              
              <div class="flex gap-2">
                <button v-if="appt.status === 'scheduled'" @click="cancelAppointment(appt.id)" class="btn btn-outline text-red-500 border-red-200 hover:bg-red-50 hover:border-red-500 text-sm">
                  Cancel
                </button>
                <button v-if="userRole === 'doctor' && appt.status === 'scheduled'" @click="completeAppointment(appt.id)" class="btn btn-primary text-sm">
                  Complete
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Simple Booking Modal (Placeholder logic) -->
    <div v-if="showBookModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="card bg-white w-full max-w-md p-6">
        <h3 class="text-lg font-bold mb-4">Book Appointment</h3>
        <form @submit.prevent="bookAppointment">
          <div class="form-group mb-4">
            <label class="label">Select Doctor</label>
            <select v-model="newAppt.doctor_id" class="input" required>
              <option value="" disabled>Select a doctor</option>
              <option v-for="doc in doctors" :key="doc.id" :value="doc.id">
                {{ doc.user?.name }} ({{ doc.specialization }})
              </option>
            </select>
          </div>
          <div class="form-group mb-4">
            <label class="label">Date & Time</label>
            <input type="datetime-local" v-model="newAppt.date" class="input" required />
          </div>
          <div class="flex justify-end gap-2">
            <button type="button" @click="showBookModal = false" class="btn btn-outline">Cancel</button>
            <button type="submit" class="btn btn-primary">Book</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import Sidebar from '@/components/Sidebar.vue';
import api from '@/services/api';

const store = useStore();
const userRole = computed(() => store.getters.userRole);

const appointments = ref([]);
const doctors = ref([]); // For booking dropdown
const loading = ref(true);
const showBookModal = ref(false);

const newAppt = ref({
  doctor_id: '',
  date: ''
});

const fetchAppointments = async () => {
  try {
    const response = await api.get('/appointments/');
    appointments.value = response.data;
  } catch (err) {
    console.error('Failed to fetch appointments', err);
  } finally {
    loading.value = false;
  }
};

const fetchDoctors = async () => {
  if (userRole.value === 'patient') {
    try {
      const response = await api.get('/doctors/');
      doctors.value = response.data;
    } catch (err) {
      console.error(err);
    }
  }
};

const getInitials = (appt) => {
  const name = userRole.value === 'doctor' ? appt.patient?.user?.name : appt.doctor?.user?.name;
  return name ? name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase() : '?';
};

const bookAppointment = async () => {
  try {
    // Need department_id for appointment. Assuming doctor object has it.
    const selectedDoc = doctors.value.find(d => d.id === newAppt.doctor_id);
    if (!selectedDoc) return;

    await api.post('/appointments/', {
      doctor_id: newAppt.doctor_id,
      department_id: selectedDoc.department_id,
      patient_id: store.getters.currentUser.id, // Assuming user.id is patient.id (one-to-one)
      appointment_date: new Date(newAppt.date).toISOString(),
      status: 'scheduled'
    });
    showBookModal.value = false;
    fetchAppointments();
  } catch (err) {
    alert('Failed to book appointment');
  }
};

const cancelAppointment = async (id) => {
  if (!confirm('Are you sure?')) return;
  try {
    await api.put(`/appointments/${id}`, { status: 'canceled' });
    fetchAppointments();
  } catch (err) {
    console.error(err);
  }
};

const completeAppointment = async (id) => {
  try {
    await api.put(`/appointments/${id}`, { status: 'completed' });
    fetchAppointments();
  } catch (err) {
    console.error(err);
  }
};

onMounted(() => {
  fetchAppointments();
  fetchDoctors();
});
</script>

<style scoped>
.bg-black\/50 { background-color: rgba(0, 0, 0, 0.5); }
.text-red-500 { color: #ef4444; }
.border-red-200 { border-color: #fecaca; }
.hover\:bg-red-50:hover { background-color: #fef2f2; }
.hover\:border-red-500:hover { border-color: #ef4444; }
</style>
