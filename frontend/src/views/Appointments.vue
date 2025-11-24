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
          
          <!-- Search -->
          <SearchBar 
            v-model="search" 
            placeholder="Search appointments by patient or doctor name..."
            @clear="search = ''"
          />

          <div v-if="loading" class="text-center py-10">
            <p class="text-muted">Loading appointments...</p>
          </div>

          <div v-else-if="displayedAppointments.length === 0" class="text-center py-10">
            <p class="text-muted">No appointments found.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="appt in displayedAppointments" :key="appt.id" class="card p-6 flex flex-col">
              <div class="flex items-center gap-4 mb-4">
                <div class="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-muted font-bold text-lg">
                  {{ getInitials(appt) }}
                </div>
                <div>
                  <h3 class="font-bold text-lg text-main">
                    {{ userRole === 'doctor' ? appt.patient?.user?.name : appt.doctor?.user?.name }}
                  </h3>
                  <p class="text-sm text-muted">
                    {{ new Date(appt.appointment_date).toLocaleString() }}
                  </p>
                  <p class="text-xs font-bold mt-1 uppercase tracking-wide" 
                     :class="{
                       'text-green-600': appt.status === 'completed',
                       'text-blue-600': appt.status === 'scheduled',
                       'text-red-600': appt.status === 'canceled'
                     }">
                    {{ appt.status }}
                  </p>
                </div>
              </div>
              
              <div class="space-y-2 mb-6 flex-1">
                 <p class="text-sm text-muted">
                  <span class="font-medium text-main">Department:</span> {{ appt.department?.name || 'N/A' }}
                </p>
              </div>

              <div class="flex gap-2 mt-auto">
                <button v-if="appt.status === 'scheduled'" @click="cancelAppointment(appt.id)" class="btn btn-outline w-full text-red-500 border-red-200 hover:bg-red-50 hover:border-red-500 text-sm">
                  Cancel
                </button>
                <button v-if="userRole === 'doctor' && appt.status === 'scheduled'" @click="completeAppointment(appt.id)" class="btn btn-primary w-full text-sm">
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
            <select v-model="newAppt.doctor_id" @change="handleDoctorChange" class="input" required>
              <option value="" disabled>Select a doctor</option>
              <option v-for="doc in doctors" :key="doc.id" :value="doc.id">
                {{ doc.user?.name }} ({{ doc.specialization }})
              </option>
            </select>
          </div>
          <div class="form-group mb-4">
            <label class="label">Available Slots</label>
            <select v-model="newAppt.slot_id" class="input" required :disabled="!newAppt.doctor_id">
              <option value="" disabled>Select a time slot</option>
              <option v-for="slot in availableSlots" :key="slot.id" :value="slot.id">
                {{ new Date(slot.available_date).toLocaleDateString() }} - {{ slot.time_slot }}
              </option>
            </select>
            <p v-if="newAppt.doctor_id && availableSlots.length === 0" class="text-xs text-red-500 mt-1">
              No available slots for this doctor.
            </p>
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
import SearchBar from '@/components/SearchBar.vue';
import api from '@/services/api';

const store = useStore();
const userRole = computed(() => store.getters.userRole);
const currentUser = computed(() => store.getters.currentUser);

const appointments = ref([]);
const doctors = ref([]); // For booking dropdown
const loading = ref(true);
const showBookModal = ref(false);
const search = ref('');

const newAppt = ref({
  doctor_id: '',
  slot_id: ''
});

const slots = ref([]);
const availableSlots = computed(() => {
  return slots.value.filter(slot => slot.status === 'available');
});

const fetchSlots = async (doctorId) => {
  if (!doctorId) return;
  try {
    const response = await api.get(`/availability/doctor/${doctorId}`);
    slots.value = response.data;
  } catch (err) {
    console.error('Failed to fetch slots', err);
  }
};

const handleDoctorChange = () => {
  newAppt.value.slot_id = '';
  fetchSlots(newAppt.value.doctor_id);
};

const filteredAppointments = computed(() => {
  if (!currentUser.value) return [];
  return appointments.value.filter(appt => {
    if (userRole.value === 'admin') {
      return true; // Show all appointments for admin
    } else if (userRole.value === 'patient') {
      return appt.patient_id === currentUser.value.id;
    } else if (userRole.value === 'doctor') {
      return appt.doctor_id === currentUser.value.id;
    }
    return false;
  });
});

const displayedAppointments = computed(() => {
  if (!search.value) return filteredAppointments.value;
  const term = search.value.toLowerCase();
  return filteredAppointments.value.filter(appt => 
    (appt.patient?.user?.name?.toLowerCase().includes(term)) ||
    (appt.doctor?.user?.name?.toLowerCase().includes(term))
  );
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
    console.log('Booking appointment...');
    
    const selectedDoc = doctors.value.find(d => d.id === newAppt.value.doctor_id);
    const selectedSlot = slots.value.find(s => s.id === newAppt.value.slot_id);
    
    if (!selectedDoc || !selectedSlot) {
      console.error('Doctor or Slot not selected');
      return;
    }

    // Combine date and time from slot (assuming slot.available_date is a date string and time_slot is "HH:MM-HH:MM")
    // For simplicity, let's assume available_date is the date and we take the start time from time_slot
    // Format: "09:00-10:00" -> "09:00"
    const startTime = selectedSlot.time_slot.split('-')[0];
    const appointmentDate = new Date(selectedSlot.available_date);
    const [hours, minutes] = startTime.split(':');
    appointmentDate.setHours(parseInt(hours), parseInt(minutes));

    const payload = {
      doctor_id: newAppt.value.doctor_id,
      department_id: selectedDoc.department_id,
      patient_id: store.getters.currentUser.id, 
      appointment_date: appointmentDate.toISOString(),
      status: 'scheduled'
    };
    console.log('Payload:', payload);

    await api.post('/appointments/', payload);
    
    // Mark slot as booked
    await api.put(`/availability/${selectedSlot.id}`, { status: 'booked' });
    
    showBookModal.value = false;
    fetchAppointments();
  } catch (err) {
    console.error(err);
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
