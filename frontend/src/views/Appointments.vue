<template>
  <div class="dashboard-layout flex h-screen overflow-hidden bg-slate-50">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden relative">
      <!-- Header -->
      <header class="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200/60 flex items-center justify-between px-8 z-10 sticky top-0">
        <div>
          <h2 class="text-2xl font-bold text-slate-800 tracking-tight">Appointments</h2>
          <p class="text-sm text-slate-500 mt-0.5">Manage your schedule and bookings</p>
        </div>
        
        <div class="flex items-center gap-4">
          <button 
            v-if="userRole === 'patient'" 
            @click="showBookModal = true" 
            class="btn-primary flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Book Appointment
          </button>
          <button 
            v-if="userRole === 'doctor'" 
            @click="showAddSlotModal = true" 
            class="btn-primary flex items-center gap-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Slot
          </button>
        </div>
      </header>

      <div class="flex-1 overflow-auto p-8">
        <div class="max-w-7xl mx-auto space-y-8">
          
          <!-- Search Section -->
          <div class="bg-white rounded-2xl p-1.5 shadow-sm border border-slate-100 max-w-2xl">
            <SearchBar 
              v-model="search" 
              placeholder="Search appointments by patient or doctor name..."
              @clear="search = ''"
            />
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="flex flex-col items-center justify-center py-20">
            <div class="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p class="text-slate-500 font-medium">Loading appointments...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="combinedItems.length === 0" class="flex flex-col items-center justify-center py-20 bg-white rounded-3xl border border-dashed border-slate-200">
            <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-lg font-bold text-slate-800 mb-1">No Appointments Found</h3>
            <p class="text-slate-500 text-center max-w-xs">
              {{ search ? 'Try adjusting your search terms.' : 'You don\'t have any scheduled appointments yet.' }}
            </p>
          </div>

          <!-- Grid Layout -->
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div 
              v-for="(item, index) in combinedItems" 
              :key="item.type + item.data.id" 
              class="group bg-white rounded-2xl border border-slate-100 shadow-sm hover:shadow-xl hover:shadow-blue-500/5 hover:-translate-y-1 transition-all duration-300 overflow-hidden flex flex-col"
            >
              
              <!-- Appointment Card -->
              <template v-if="item.type === 'appointment'">
                <div class="h-1.5 w-full transition-colors duration-300" :class="{
                  'bg-emerald-500': item.data.status === 'completed',
                  'bg-blue-500': item.data.status === 'scheduled',
                  'bg-rose-500': item.data.status === 'canceled'
                }"></div>

                <div class="p-6 flex-1 flex flex-col">
                  <div class="flex justify-between items-start mb-6">
                    <div>
                      <div class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide mb-3" :class="{
                        'bg-emerald-50 text-emerald-700': item.data.status === 'completed',
                        'bg-blue-50 text-blue-700': item.data.status === 'scheduled',
                        'bg-rose-50 text-rose-700': item.data.status === 'canceled'
                      }">
                        <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="{
                          'bg-emerald-500': item.data.status === 'completed',
                          'bg-blue-500': item.data.status === 'scheduled',
                          'bg-rose-500': item.data.status === 'canceled'
                        }"></span>
                        {{ item.data.status }}
                      </div>
                      <h3 class="font-bold text-lg text-slate-800 group-hover:text-blue-600 transition-colors">
                        {{ userRole === 'doctor' ? item.data.patient?.user?.name : 'Dr. ' + (item.data.doctor?.user?.name || 'Unknown') }}
                      </h3>
                      <p class="text-sm text-slate-500 font-medium mt-1" v-if="userRole === 'patient' && item.data.doctor?.specialization">
                        {{ item.data.doctor.specialization }}
                      </p>
                    </div>
                  </div>

                  <div class="space-y-4 mb-8">
                    <div class="flex items-center gap-3.5 text-sm text-slate-600">
                      <div class="w-8 h-8 rounded-lg bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-blue-50 group-hover:text-blue-500 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                      </div>
                      <span class="font-medium">
                        {{ new Date(item.data.appointment_date).toLocaleDateString(undefined, { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }) }}
                      </span>
                    </div>
                    <div class="flex items-center gap-3.5 text-sm text-slate-600">
                      <div class="w-8 h-8 rounded-lg bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-blue-50 group-hover:text-blue-500 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <span class="font-medium">
                        {{ new Date(item.data.appointment_date).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' }) }}
                      </span>
                    </div>
                    <div class="flex items-center gap-3.5 text-sm text-slate-600">
                      <div class="w-8 h-8 rounded-lg bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-blue-50 group-hover:text-blue-500 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                      </div>
                      <span class="font-medium">{{ item.data.department?.name || 'General' }}</span>
                    </div>
                  </div>

                  <div class="mt-auto pt-6 border-t border-slate-100 flex gap-3">
                    <template v-if="item.data.status === 'scheduled'">
                      <button @click="cancelAppointment(item.data.id)" class="flex-1 py-2.5 px-4 rounded-xl text-xs font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 transition-colors">
                        Cancel
                      </button>
                      <button @click="rescheduleAppointment(item.data)" class="flex-1 py-2.5 px-4 rounded-xl text-xs font-bold text-blue-600 bg-blue-50 hover:bg-blue-100 transition-colors">
                        Reschedule
                      </button>
                      <button v-if="userRole === 'doctor'" @click="completeAppointment(item.data.id)" class="flex-1 py-2.5 px-4 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-500/20 transition-all">
                        Complete
                      </button>
                    </template>
                    <div v-else class="w-full text-center py-2 text-xs text-slate-400 font-medium italic">
                      No actions available
                    </div>
                  </div>
                </div>
              </template>

              <!-- Slot Card -->
              <template v-else>
                <div class="h-1.5 w-full bg-slate-200"></div>
                <div class="p-6 flex-1 flex flex-col">
                  <div class="flex justify-between items-start mb-6">
                    <div>
                      <div class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide bg-slate-100 text-slate-500 mb-3">
                        Available Slot
                      </div>
                      <h3 class="font-bold text-lg text-slate-800">
                        {{ new Date(item.data.available_date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) }}
                      </h3>
                    </div>
                  </div>

                  <div class="space-y-4 mb-8">
                    <div class="flex items-center gap-3.5 text-sm text-slate-600">
                      <div class="w-8 h-8 rounded-lg bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-blue-50 group-hover:text-blue-500 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <span class="font-bold text-lg text-blue-600">{{ item.data.time_slot }}</span>
                    </div>
                  </div>

                  <div class="mt-auto pt-6 border-t border-slate-100">
                    <button @click="deleteSlot(item.data.id)" class="w-full py-2.5 px-4 rounded-xl text-xs font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 transition-colors flex items-center justify-center gap-2">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
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

    <!-- Book Appointment Modal -->
    <Transition name="modal">
      <div v-if="showBookModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
        <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity" @click="showBookModal = false"></div>
        
        <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-[550px] overflow-hidden transform transition-all flex flex-col max-h-[90vh]">
          
          <div class="px-8 py-6 bg-gradient-to-r from-blue-600 to-blue-700 flex justify-between items-start">
            <div>
              <h3 class="text-xl font-bold text-white">Book Appointment</h3>
              <p class="text-blue-100 text-sm mt-1">Schedule a visit with our specialists</p>
            </div>
            <button @click="showBookModal = false" class="text-white/70 hover:text-white transition-colors bg-white/10 hover:bg-white/20 rounded-full p-2 backdrop-blur-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div class="p-8 overflow-y-auto">
            <form @submit.prevent="bookAppointment" class="space-y-6">
              
              <div class="form-group">
                <label class="block text-sm font-bold text-slate-700 mb-2">Select Specialist</label>
                <div class="relative group">
                  <select 
                    v-model="newAppt.doctor_id" 
                    @change="handleDoctorChange" 
                    class="block w-full pl-4 pr-10 py-3.5 text-sm font-medium text-slate-700 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-slate-50 hover:bg-white transition-all appearance-none cursor-pointer" 
                    required
                  >
                    <option value="" disabled>Choose a doctor...</option>
                    <option v-for="doc in doctors" :key="doc.id" :value="doc.id">
                      Dr. {{ doc.user?.name }} — {{ doc.specialization }}
                    </option>
                  </select>
                  <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-slate-400 group-hover:text-blue-500 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>
              
              <div class="form-group">
                <label class="block text-sm font-bold text-slate-700 mb-2">Available Time Slots</label>
                <div class="relative group">
                  <select 
                    v-model="newAppt.slot_id" 
                    class="block w-full pl-4 pr-10 py-3.5 text-sm font-medium text-slate-700 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-slate-50 hover:bg-white transition-all appearance-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-slate-100" 
                    required 
                    :disabled="!newAppt.doctor_id"
                  >
                    <option value="" disabled>Select a time slot...</option>
                    <option v-for="slot in availableSlots" :key="slot.id" :value="slot.id">
                      {{ new Date(slot.available_date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) }} — {{ slot.time_slot }}
                    </option>
                  </select>
                  <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none text-slate-400 group-hover:text-blue-500 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
                
                <div v-if="newAppt.doctor_id" class="mt-2 min-h-[20px]">
                  <p v-if="availableSlots.length === 0" class="text-xs font-medium text-rose-500 flex items-center gap-1.5 animate-pulse">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    No slots available for this doctor.
                  </p>
                  <p v-else class="text-xs font-medium text-emerald-600 flex items-center gap-1.5">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {{ availableSlots.length }} slots available
                  </p>
                </div>
              </div>
              
              <div class="flex items-center justify-end gap-3 pt-6 border-t border-slate-100">
                <button type="button" @click="showBookModal = false" class="px-6 py-3 text-sm font-bold text-slate-600 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 hover:text-slate-800 transition-all focus:ring-2 focus:ring-offset-2 focus:ring-slate-200">
                  Cancel
                </button>
                <button type="submit" class="px-8 py-3 text-sm font-bold text-white bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl hover:from-blue-700 hover:to-blue-800 shadow-lg shadow-blue-500/30 transform active:scale-95 transition-all focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                  Confirm Booking
                </button>
              </div>

            </form>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Add Slot Modal -->
    <Transition name="modal">
      <div v-if="showAddSlotModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
        <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm transition-opacity" @click="showAddSlotModal = false"></div>
        
        <div class="relative bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden transform transition-all">
          <div class="px-8 py-6 bg-gradient-to-r from-blue-600 to-blue-700 flex justify-between items-start">
            <div>
              <h3 class="text-xl font-bold text-white">Add Availability</h3>
              <p class="text-blue-100 text-sm mt-1">Set your available hours</p>
            </div>
            <button @click="showAddSlotModal = false" class="text-white/70 hover:text-white transition-colors bg-white/10 hover:bg-white/20 rounded-full p-2 backdrop-blur-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="p-8">
            <form @submit.prevent="addSlot" class="space-y-5">
              <div class="form-group">
                <label class="block text-sm font-bold text-slate-700 mb-2">Date</label>
                <input 
                  type="date" 
                  v-model="newSlot.date" 
                  class="block w-full px-4 py-3 text-sm font-medium text-slate-700 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-slate-50 hover:bg-white transition-all" 
                  required 
                  :min="new Date().toISOString().split('T')[0]"
                >
              </div>
              <div class="form-group">
                <label class="block text-sm font-bold text-slate-700 mb-2">Time Slot</label>
                <div class="flex gap-3 items-center">
                  <input 
                    type="time" 
                    v-model="newSlot.startTime" 
                    class="flex-1 px-4 py-3 text-sm font-medium text-slate-700 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-slate-50 hover:bg-white transition-all" 
                    required
                  >
                  <span class="text-slate-400 font-medium">to</span>
                  <input 
                    type="time" 
                    v-model="newSlot.endTime" 
                    class="flex-1 px-4 py-3 text-sm font-medium text-slate-700 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-slate-50 hover:bg-white transition-all" 
                    required
                  >
                </div>
              </div>
              <div class="flex justify-end gap-3 pt-4">
                <button type="button" @click="showAddSlotModal = false" class="px-6 py-2.5 text-sm font-bold text-slate-600 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 hover:text-slate-800 transition-all">Cancel</button>
                <button type="submit" class="px-8 py-2.5 text-sm font-bold text-white bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl hover:from-blue-700 hover:to-blue-800 shadow-lg shadow-blue-500/30 transform active:scale-95 transition-all">Add Slot</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </Transition>

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

const bookAppointment = async () => {
  try {
    console.log('Booking appointment...');
    
    const selectedDoc = doctors.value.find(d => d.id === newAppt.value.doctor_id);
    const selectedSlot = slots.value.find(s => s.id === newAppt.value.slot_id);
    
    if (!selectedDoc || !selectedSlot) {
      console.error('Doctor or Slot not selected');
      return;
    }

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
  items = displayedAppointments.value.map(appt => ({
    type: 'appointment',
    date: new Date(appt.appointment_date),
    data: appt
  }));

  // 2. Add Available Slots (Only for Doctors)
  if (userRole.value === 'doctor') {
    const relevantSlots = slots.value.filter(s => s.status === 'available');
    
    relevantSlots.forEach(slot => {
      const dateStr = slot.available_date.split('T')[0];
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
.btn-primary {
  @apply px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium shadow-sm shadow-blue-500/30;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .transform,
.modal-leave-active .transform {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-enter-from .transform,
.modal-leave-to .transform {
  opacity: 0;
  transform: scale(0.95) translateY(20px);
}
</style>