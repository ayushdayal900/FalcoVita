<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">Appointments</h2>
        <button v-if="userRole === 'patient'" @click="showBookModal = true" class="btn btn-primary text-sm">
          Book Appointment
        </button>
        <button v-if="userRole === 'doctor'" @click="showAddSlotModal = true" class="btn btn-primary text-sm">
          Add Slot
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

          <div v-else-if="combinedItems.length === 0" class="text-center py-10">
            <p class="text-muted">No appointments or slots found.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="(item, index) in combinedItems" :key="item.type + item.data.id" class="group bg-white rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden flex flex-col">
              
              <!-- APPOINTMENT CARD -->
              <template v-if="item.type === 'appointment'">
                <!-- Status Bar -->
                <div class="h-1.5 w-full" :class="{
                  'bg-emerald-500': item.data.status === 'completed',
                  'bg-blue-500': item.data.status === 'scheduled',
                  'bg-red-500': item.data.status === 'canceled'
                }"></div>

                <div class="p-6 flex-1 flex flex-col">
                  <div class="flex justify-between items-start mb-4">
                    <div>
                      <p class="text-xs font-bold uppercase tracking-wider mb-1" :class="{
                        'text-emerald-600': item.data.status === 'completed',
                        'text-blue-600': item.data.status === 'scheduled',
                        'text-red-600': item.data.status === 'canceled'
                      }">
                        {{ item.data.status }}
                      </p>
                      <h3 class="font-bold text-lg text-slate-800">
                        {{ userRole === 'doctor' ? item.data.patient?.user?.name : 'Dr. ' + (item.data.doctor?.user?.name || 'Unknown') }}
                      </h3>
                      <p class="text-sm text-slate-500" v-if="userRole === 'patient' && item.data.doctor?.specialization">
                        {{ item.data.doctor.specialization }}
                      </p>
                    </div>
                    </div>

                  <div class="space-y-3 mb-6">
                    <div class="flex items-center gap-3 text-sm text-slate-600">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span class="font-medium">
                        {{ new Date(item.data.appointment_date).toLocaleDateString(undefined, { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }) }}
                      </span>
                    </div>
                    <div class="flex items-center gap-3 text-sm text-slate-600">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span class="font-medium">
                        {{ new Date(item.data.appointment_date).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' }) }}
                      </span>
                    </div>
                    <div class="flex items-center gap-3 text-sm text-slate-600">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                      <span>{{ item.data.department?.name || 'General' }}</span>
                    </div>
                  </div>

                  <div class="mt-auto pt-4 border-t border-slate-100 flex gap-2">
                    <template v-if="item.data.status === 'scheduled'">
                      <button @click="cancelAppointment(item.data.id)" class="flex-1 py-2 px-3 rounded-lg text-xs font-medium text-red-600 bg-red-50 hover:bg-red-100 transition-colors">
                        Cancel
                      </button>
                      <button @click="rescheduleAppointment(item.data)" class="flex-1 py-2 px-3 rounded-lg text-xs font-medium text-blue-600 bg-blue-50 hover:bg-blue-100 transition-colors">
                        Reschedule
                      </button>
                      <button v-if="userRole === 'doctor'" @click="completeAppointment(item.data.id)" class="flex-1 py-2 px-3 rounded-lg text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 transition-colors">
                        Complete
                      </button>
                    </template>
                    <div v-else class="w-full text-center py-2 text-xs text-slate-400 font-medium italic">
                      No actions available
                    </div>
                  </div>
                </div>
              </template>

              <!-- SLOT CARD -->
              <template v-else>
                <div class="h-1.5 w-full bg-slate-300"></div>
                <div class="p-6 flex-1 flex flex-col">
                  <div class="flex justify-between items-start mb-4">
                    <div>
                      <p class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Available Slot</p>
                      <h3 class="font-bold text-lg text-slate-800">
                        {{ new Date(item.data.available_date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) }}
                      </h3>
                    </div>
                    </div>

                  <div class="space-y-3 mb-6">
                    <div class="flex items-center gap-3 text-sm text-slate-600">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span class="font-medium text-lg text-blue-600">{{ item.data.time_slot }}</span>
                    </div>
                  </div>

                  <div class="mt-auto pt-4 border-t border-slate-100">
                    <button @click="deleteSlot(item.data.id)" class="w-full py-2 px-3 rounded-lg text-xs font-medium text-red-600 bg-red-50 hover:bg-red-100 transition-colors">
                      Delete Slot
                    </button>
                  </div>
                </div>
              </template>

            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Simple Booking Modal -->
    <div v-if="showBookModal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden transform transition-all">
        <div class="bg-slate-50 px-6 py-4 border-b border-slate-100 flex justify-between items-center">
          <h3 class="text-lg font-bold text-slate-800">Book Appointment</h3>
          <button @click="showBookModal = false" class="text-slate-400 hover:text-slate-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6">
          <form @submit.prevent="bookAppointment" class="space-y-5">
            <div class="form-group">
              <label class="block text-sm font-medium text-slate-700 mb-1">Select Doctor</label>
              <div class="relative">
                <select v-model="newAppt.doctor_id" @change="handleDoctorChange" class="block w-full pl-3 pr-10 py-2.5 text-base border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-xl bg-slate-50 transition-all" required>
                  <option value="" disabled>Choose a specialist</option>
                  <option v-for="doc in doctors" :key="doc.id" :value="doc.id">
                    Dr. {{ doc.user?.name }} ({{ doc.specialization }})
                  </option>
                </select>
              </div>
            </div>
            
            <div class="form-group">
              <label class="block text-sm font-medium text-slate-700 mb-1">Available Slots</label>
              <div class="relative">
                <select v-model="newAppt.slot_id" class="block w-full pl-3 pr-10 py-2.5 text-base border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-xl bg-slate-50 transition-all" required :disabled="!newAppt.doctor_id">
                  <option value="" disabled>Select a time slot</option>
                  <option v-for="slot in availableSlots" :key="slot.id" :value="slot.id">
                    {{ new Date(slot.available_date).toLocaleDateString() }} - {{ slot.time_slot }}
                  </option>
                </select>
              </div>
              <p v-if="newAppt.doctor_id && availableSlots.length === 0" class="text-xs text-orange-500 mt-2 flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                No available slots for this doctor.
              </p>
            </div>
            
            <div class="flex justify-end gap-3 pt-4">
              <button type="button" @click="showBookModal = false" class="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-xl hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">Cancel</button>
              <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 shadow-lg shadow-blue-500/30 transition-all">Book Appointment</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Add Slot Modal -->
    <div v-if="showAddSlotModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="card bg-white w-full max-w-md p-6">
        <h3 class="text-lg font-bold mb-4">Add Availability Slot</h3>
        <form @submit.prevent="addSlot">
          <div class="form-group mb-4">
            <label class="label">Date</label>
            <input type="date" v-model="newSlot.date" class="input" required :min="new Date().toISOString().split('T')[0]">
          </div>
          <div class="form-group mb-4">
            <label class="label">Time Slot</label>
            <div class="flex gap-2 items-center">
              <input type="time" v-model="newSlot.startTime" class="input" required>
              <span>to</span>
              <input type="time" v-model="newSlot.endTime" class="input" required>
            </div>
          </div>
          <div class="flex justify-end gap-2">
            <button type="button" @click="showAddSlotModal = false" class="btn btn-outline">Cancel</button>
            <button type="submit" class="btn btn-primary">Add Slot</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import Sidebar from '@/components/Sidebar.vue';
import SearchBar from '@/components/SearchBar.vue';
import api from '@/services/api';

const store = useStore();
const userRole = computed(() => store.getters.userRole);
const currentUser = computed(() => store.getters.currentUser);
const router = useRouter();

const appointments = ref([]);
const doctors = ref([]); // For booking dropdown
const loading = ref(true);
const showBookModal = ref(false);
const showAddSlotModal = ref(false);
const search = ref('');

const newAppt = ref({
  doctor_id: '',
  slot_id: ''
});

const newSlot = ref({
  date: '',
  startTime: '',
  endTime: ''
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

const rescheduleAppointment = async (appt) => {
  if (!confirm('To reschedule, we will cancel this appointment and redirect you to the doctor\'s page to book a new slot. Proceed?')) return;
  
  try {
    // 1. Cancel current appointment
    await api.put(`/appointments/${appt.id}`, { status: 'canceled' });
    
    // 2. Redirect to doctor's page
    router.push(`/doctors/${appt.doctor_id}`);
  } catch (err) {
    console.error("Reschedule failed", err);
    alert("Failed to initiate reschedule.");
  }
};

const addSlot = async () => {
  try {
    const payload = {
      doctor_id: currentUser.value.id,
      available_date: new Date(newSlot.value.date).toISOString(),
      time_slot: `${newSlot.value.startTime}-${newSlot.value.endTime}`,
      status: 'available'
    };
    
    await api.post('/availability/', payload);
    alert('Slot added successfully!');
    showAddSlotModal.value = false;
    if (currentUser.value) {
      fetchSlots(currentUser.value.id);
    }
    
    // Reset form
    newSlot.value = { date: '', startTime: '', endTime: '' };
  } catch (err) {
    console.error("Failed to add slot", err);
    alert("Failed to add slot.");
  }
};

const deleteSlot = async (id) => {
  if (!confirm('Are you sure you want to delete this slot?')) return;
  try {
    await api.delete(`/availability/${id}`);
    if (currentUser.value) {
      fetchSlots(currentUser.value.id);
    }
  } catch (err) {
    console.error("Failed to delete slot", err);
    alert("Failed to delete slot.");
  }
};

const combinedItems = computed(() => {
  let items = [];

  // 1. Add Appointments
  // We use displayedAppointments which already handles search & role filtering
  items = displayedAppointments.value.map(appt => ({
    type: 'appointment',
    date: new Date(appt.appointment_date),
    data: appt
  }));

  // 2. Add Available Slots (Only for Doctors)
  if (userRole.value === 'doctor') {
    // Filter slots based on search term if needed, or just show all available
    // If search is active, maybe we only show slots if they match something? 
    // But slots don't have patient names. Let's just show them if search is empty 
    // OR if we want to be fancy, maybe filter by date? 
    // For now, let's include them if they are available.
    
    const relevantSlots = slots.value.filter(s => s.status === 'available');
    
    relevantSlots.forEach(slot => {
      // Create a date object for sorting. 
      // Assuming available_date is "YYYY-MM-DD" and time_slot is "HH:MM-..."
      const dateStr = slot.available_date.split('T')[0]; // ensure we get YYYY-MM-DD
      const timeStart = slot.time_slot.split('-')[0];
      const dateTime = new Date(`${dateStr}T${timeStart}`);
      
      items.push({
        type: 'slot',
        date: dateTime,
        data: slot
      });
    });
  }

  // 3. Sort by date
  return items.sort((a, b) => a.date - b.date);
});

onMounted(() => {
  fetchAppointments();
  fetchDoctors();
  if (userRole.value === 'doctor' && currentUser.value) {
    fetchSlots(currentUser.value.id);
  }
});
</script>

<style scoped>
.bg-black\/50 { background-color: rgba(0, 0, 0, 0.5); }
.text-red-500 { color: #ef4444; }
.border-red-200 { border-color: #fecaca; }
.hover\:bg-red-50:hover { background-color: #fef2f2; }
.hover\:border-red-500:hover { border-color: #ef4444; }
</style>
