<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />
    
    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <!-- Header -->
      <header class="bg-white border-bottom py-3 px-4 d-flex align-items-center justify-content-between sticky-top z-2 shadow-sm">
        <div>
          <h2 class="h4 fw-bold text-dark mb-0">Appointments</h2>
          <p class="text-muted small mb-0">Manage your schedule and bookings</p>
        </div>
        
        <div class="d-flex gap-2">
          <button 
            v-if="userRole === 'patient'" 
            @click="showBookModal = true" 
            class="btn btn-primary d-flex align-items-center gap-2 shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Book Appointment
          </button>
          <button 
            v-if="userRole === 'doctor'" 
            @click="showAddSlotModal = true" 
            class="btn btn-primary d-flex align-items-center gap-2 shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Slot
          </button>
        </div>
      </header>

      <div class="flex-grow-1 overflow-auto p-4 custom-scrollbar">
        <div class="container-fluid p-0" style="max-width: 1400px;">
          
          <!-- Search Section -->
          <div class="card border-0 shadow-sm mb-4" style="max-width: 600px;">
            <div class="card-body p-2">
              <SearchBar 
                v-model="search" 
                placeholder="Search appointments by name..."
                @clear="search = ''"
              />
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary mb-3" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted fw-medium">Loading appointments...</p>
          </div>

          <div v-else-if="combinedItems.length === 0" class="text-center py-5 bg-white rounded-4 border border-dashed">
            <!-- Empty State -->
            <div class="bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 64px; height: 64px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-muted">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="h5 fw-bold text-dark mb-1">No Appointments Found</h3>
            <p class="text-muted small">
              {{ search ? 'Try adjusting your search terms.' : 'You don\'t have any scheduled appointments yet.' }}
            </p>
          </div>

          <div v-else class="row g-4">
            <!-- Grid Layout -->
            <div 
              v-for="(item, index) in combinedItems" 
              :key="item.type + item.data.id" 
              class="col-md-6 col-lg-4"
            >
              <div class="card h-100 border-0 shadow-sm hover-lift overflow-hidden">
                
                <!-- Appointment Card -->
                <template v-if="item.type === 'appointment'">
                  <div class="card-header border-0 p-0" style="height: 6px;" :class="{
                    'bg-success': item.data.status === 'completed',
                    'bg-primary': item.data.status === 'scheduled',
                    'bg-danger': item.data.status === 'cancelled' || item.data.status === 'canceled'
                  }"></div>

                  <div class="card-body p-4 d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-start mb-4">
                      <div>
                        <!-- Fixed status badge block -->
                        <span
                          class="badge rounded-pill mb-2 px-3 py-2"
                          :class="{
                            'bg-success bg-opacity-10 text-success': item.data.status === 'completed',
                            'bg-primary bg-opacity-10 text-primary': item.data.status === 'scheduled',
                            'bg-danger bg-opacity-10 text-danger': item.data.status === 'cancelled' || item.data.status === 'canceled'
                          }"
                        >
                          <span
                            class="d-inline-block rounded-circle me-2"
                            style="width: 8px; height: 8px;"
                            :class="{
                              'bg-success': item.data.status === 'completed',
                              'bg-primary': item.data.status === 'scheduled',
                              'bg-danger': item.data.status === 'cancelled' || item.data.status === 'canceled'
                            }"
                          ></span>
                          {{ item.data.status }}
                        </span>
                        <h3 class="h5 fw-bold text-dark mb-1">
                          {{ userRole === 'doctor' ? item.data.patient?.user?.name : 'Dr. ' + (item.data.doctor?.user?.name || 'Unknown') }}
                        </h3>
                        <p class="text-primary small fw-bold mb-0" v-if="userRole === 'admin'">
                          Patient: {{ item.data.patient?.user?.name }}
                        </p>
                        <p class="text-muted small fw-medium mb-0" v-if="userRole === 'patient' && item.data.doctor?.specialization">
                          {{ item.data.doctor.specialization }}
                        </p>
                      </div>
                    </div>

                        <div class="d-flex align-items-center gap-3 mb-2 text-muted small">
                          <div class="bg-light rounded p-1 text-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                          </div>
                          <span class="fw-medium text-dark">
                            {{ new Date(item.data.appointment_date).toLocaleDateString(undefined, { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }) }}
                          </span>
                        </div>

                        <div class="d-flex align-items-center gap-3 mb-2 text-muted small">
                          <div class="bg-light rounded p-1 text-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                          </div>
                          <span class="fw-medium text-dark">
                            {{ new Date(item.data.appointment_date).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' }) }}
                          </span>
                        </div>

                        <div class="d-flex align-items-center gap-3 text-muted small">
                          <div class="bg-light rounded p-1 text-primary">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                            </svg>
                          </div>
                          <span class="fw-medium text-dark">{{ item.data.department?.name || 'General' }}</span>
                        </div>

                    <div class="mt-auto pt-3 border-top d-flex gap-2">
                      <template v-if="item.data.status === 'scheduled'">
                        <button @click="cancelAppointment(item.data.id)" class="btn btn-sm btn-outline-danger flex-grow-1 fw-bold">
                          Cancel
                        </button>
                        <button @click="rescheduleAppointment(item.data)" class="btn btn-sm btn-outline-primary flex-grow-1 fw-bold">
                          Reschedule
                        </button>
                        <button v-if="userRole === 'doctor'" @click="completeAppointment(item.data.id)" class="btn btn-sm btn-primary flex-grow-1 fw-bold">
                          Complete
                        </button>
                      </template>
                      <div v-else class="w-100 text-center py-1 text-muted small fst-italic">
                        No actions available
                      </div>
                    </div>
                  </div>
                </template>

                <template v-if="item.type === 'slot'">
                  <!-- Slot Card -->
                  <div class="card-header border-0 p-0 bg-secondary" style="height: 6px;"></div>
                  <div class="card-body p-4 d-flex flex-column">
                    <div class="mb-4">
                      <span class="badge bg-light text-secondary border mb-2">Available Slot</span>
                      <h3 class="h5 fw-bold text-dark mb-0">
                        {{ new Date(item.data.available_date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) }}
                      </h3>
                    </div>

                    <div class="mb-4">
                      <div class="d-flex align-items-center gap-3 text-muted small">
                        <div class="bg-light rounded p-1 text-primary">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                        </div>
                        <span class="fw-bold fs-5 text-primary">{{ item.data.time_slot }}</span>
                      </div>
                    </div>

                    <div class="mt-auto pt-3 border-top">
                      <button @click="deleteSlot(item.data.id)" class="btn btn-sm btn-outline-danger w-100 fw-bold d-flex align-items-center justify-content-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
      </div>
    </main>

    <!-- Book Appointment Modal -->
    <div v-if="showBookModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header bg-primary text-white border-bottom-0 rounded-top-4">
            <h5 class="modal-title fw-bold">Book Appointment</h5>
            <button type="button" class="btn-close btn-close-white" @click="showBookModal = false"></button>
          </div>
          
          <div class="modal-body p-4">
            <form @submit.prevent="bookAppointment">
              
              <div class="mb-3">
                <label class="form-label fw-bold small">Select Specialist</label>
                <select 
                  v-model="newAppt.doctor_id" 
                  @change="handleDoctorChange" 
                  class="form-select" 
                  required
                >
                  <option value="" disabled>Choose a doctor...</option>
                  <option v-for="doc in doctors" :key="doc.id" :value="doc.id">
                    Dr. {{ doc.user?.name }} — {{ doc.specialization }}
                  </option>
                </select>
              </div>
              
              <div class="mb-4">
                <label class="form-label fw-bold small">Available Time Slots</label>
                <select 
                  v-model="newAppt.slot_id" 
                  class="form-select" 
                  required 
                  :disabled="!newAppt.doctor_id"
                >
                  <option value="" disabled>Select a time slot...</option>
                  <option v-for="slot in availableSlots" :key="slot.id" :value="slot.id">
                    {{ new Date(slot.available_date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) }} — {{ slot.time_slot }}
                  </option>
                </select>
                
                <div v-if="newAppt.doctor_id" class="mt-2">
                  <p v-if="availableSlots.length === 0" class="text-danger small fw-bold mb-0">
                    No slots available for this doctor.
                  </p>
                  <p v-else class="text-success small fw-bold mb-0">
                    {{ availableSlots.length }} slots available
                  </p>
                </div>
              </div>
              
              <div class="d-flex justify-content-end gap-2 pt-3 border-top">
                <button type="button" @click="showBookModal = false" class="btn btn-light">Cancel</button>
                <button type="submit" class="btn btn-primary fw-bold px-4">Confirm Booking</button>
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Payment Confirmation Modal -->
    <div v-if="showPaymentModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header bg-success text-white border-bottom-0 rounded-top-4">
            <h5 class="modal-title fw-bold">Complete Payment</h5>
            <button type="button" class="btn-close btn-close-white" @click="showPaymentModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <div class="text-center mb-4">
              <div class="bg-success bg-opacity-10 text-success rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 64px; height: 64px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h4 class="h5 fw-bold text-dark">Payment Required</h4>
              <p class="text-muted small">Please pay the consultation fee to confirm your booking.</p>
              <h2 class="display-6 fw-bold text-success mb-0">₹100</h2>
            </div>
            
            <form @submit.prevent="confirmPayment">
              <div class="mb-3">
                <label class="form-label fw-bold small">Card Number</label>
                <input type="text" class="form-control" placeholder="0000 0000 0000 0000" required>
              </div>
              <div class="row g-3">
                <div class="col-6">
                  <label class="form-label fw-bold small">Expiry</label>
                  <input type="text" class="form-control" placeholder="MM/YY" required>
                </div>
                <div class="col-6">
                  <label class="form-label fw-bold small">CVV</label>
                  <input type="text" class="form-control" placeholder="123" required>
                </div>
              </div>
              
              <div class="d-flex justify-content-end gap-2 pt-4 mt-2 border-top">
                <button type="button" @click="showPaymentModal = false" class="btn btn-light">Cancel</button>
                <button type="button" @click="confirmPayment('Pay Later')" class="btn btn-outline-primary fw-bold">Pay Later</button>
                <button type="submit" class="btn btn-success fw-bold px-4">Pay & Confirm</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Slot Modal -->
    <div v-if="showAddSlotModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header bg-primary text-white border-bottom-0 rounded-top-4">
            <h5 class="modal-title fw-bold">Add Availability</h5>
            <button type="button" class="btn-close btn-close-white" @click="showAddSlotModal = false"></button>
          </div>

          <div class="modal-body p-4">
            <form @submit.prevent="addSlot">
              <div class="mb-3">
                <label class="form-label fw-bold small">Dates</label>
                <div class="d-flex gap-2 mb-2">
                  <input 
                    type="date" 
                    v-model="currentDateInput" 
                    class="form-control" 
                    :min="new Date().toISOString().split('T')[0]"
                  >
                  <button type="button" @click="addDateToSlot" class="btn btn-outline-primary fw-bold text-nowrap">
                    Add Date
                  </button>
                </div>
                
                <!-- Selected Dates List -->
                <div v-if="newSlot.dates.length > 0" class="d-flex flex-wrap gap-2 mb-2">
                  <span 
                    v-for="(date, index) in newSlot.dates" 
                    :key="index"
                    class="badge bg-light text-primary border d-flex align-items-center gap-2 px-3 py-2"
                  >
                    {{ new Date(date).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) }}
                    <button 
                      type="button" 
                      @click="removeDateFromSlot(index)"
                      class="btn-close btn-close-dark" 
                      style="width: 0.5em; height: 0.5em;"
                    ></button>
                  </span>
                </div>
                <div v-if="newSlot.dates.length === 0 && !currentDateInput" class="text-muted small fst-italic">
                  Select a date and click "Add Date" or just fill the date input.
                </div>
              </div>

              <div class="mb-4">
                <label class="form-label fw-bold small">Time Slot</label>
                <div class="input-group">
                  <input 
                    type="time" 
                    v-model="newSlot.startTime" 
                    class="form-control" 
                    required
                  >
                  <span class="input-group-text bg-light">to</span>
                  <input 
                    type="time" 
                    v-model="newSlot.endTime" 
                    class="form-control" 
                    required
                  >
                </div>
              </div>
              <div class="d-flex justify-content-end gap-2 pt-3 border-top">
                <button type="button" @click="showAddSlotModal = false" class="btn btn-light">Cancel</button>
                <button type="submit" class="btn btn-primary fw-bold px-4">Add Slot</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Complete Appointment Modal -->
    <div v-if="showCompleteModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header bg-primary text-white border-bottom-0 rounded-top-4">
            <h5 class="modal-title fw-bold">Complete Appointment & Write Prescription</h5>
            <button type="button" class="btn-close btn-close-white" @click="showCompleteModal = false"></button>
          </div>
          
          <div class="modal-body p-4">
            <form @submit.prevent="submitCompletion">
              
              <div class="mb-4">
                <label class="form-label fw-bold small text-uppercase text-muted">Diagnosis</label>
                <textarea 
                  v-model="completeForm.diagnosis" 
                  class="form-control" 
                  rows="2" 
                  placeholder="Enter patient diagnosis..."
                  required
                ></textarea>
              </div>

              <div class="card bg-light border-0 mb-4">
                <div class="card-body">
                  <h6 class="fw-bold text-primary mb-3">Prescription Details</h6>
                  
                  <div class="mb-3">
                    <label class="form-label fw-bold small">Medicines</label>
                    <input 
                      type="text" 
                      v-model="completeForm.medicines" 
                      class="form-control" 
                      placeholder="e.g., Amoxicillin 500mg, Paracetamol"
                      required
                    >
                  </div>

                  <div class="row g-3">
                    <div class="col-md-6">
                      <label class="form-label fw-bold small">Dosage</label>
                      <input 
                        type="text" 
                        v-model="completeForm.dosage" 
                        class="form-control" 
                        placeholder="e.g., 1 tablet 3 times a day"
                        required
                      >
                    </div>
                    <div class="col-md-6">
                      <label class="form-label fw-bold small">Instructions</label>
                      <input 
                        type="text" 
                        v-model="completeForm.instructions" 
                        class="form-control" 
                        placeholder="e.g., Take after food"
                      >
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="d-flex justify-content-end gap-2 pt-3 border-top">
                <button type="button" @click="showCompleteModal = false" class="btn btn-light">Cancel</button>
                <button type="submit" class="btn btn-primary fw-bold px-4">Complete & Save</button>
              </div>

            </form>
          </div>
        </div>
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
const showPaymentModal = ref(false);
const showAddSlotModal = ref(false);
const search = ref('');
const pendingBookingPayload = ref(null);
const pendingSlotId = ref(null);

const newAppt = ref({
  doctor_id: '',
  slot_id: ''
});

const currentDateInput = ref('');
const newSlot = ref({
  dates: [],
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

    // Store payload and open payment modal
    pendingBookingPayload.value = payload;
    pendingSlotId.value = selectedSlot.id;
    showBookModal.value = false;
    showPaymentModal.value = true;

  } catch (err) {
    console.error(err);
    alert('Failed to initiate booking');
  }
};

const confirmPayment = async (method = 'Credit Card') => {
  if (!pendingBookingPayload.value) return;

  try {
    const isPayLater = method === 'Pay Later';
    const finalPayDetails = isPayLater 
       ? { amount: 100, method: 'Pay Later' }
       : { amount: 100, method: "Credit Card" };

    const finalPayload = {
        ...pendingBookingPayload.value,
        payment_details: finalPayDetails
    };

    await api.post('/appointments/', finalPayload);
    
    // Mark slot as booked
    if (pendingSlotId.value) {
        await api.put(`/availability/${pendingSlotId.value}`, { status: 'booked' });
    }
    
    showPaymentModal.value = false;
    pendingBookingPayload.value = null;
    pendingSlotId.value = null;
    fetchAppointments();
    alert(method === 'Pay Later' ? "Booking Confirmed! Please pay from your dashboard." : "Payment successful! Your appointment has been booked.");
  } catch (err) {
    console.error(err);
    alert('Failed to complete booking/payment');
  }
};

const cancelAppointment = async (id) => {
  if (!confirm('Are you sure?')) return;
  try {
    await api.put(`/appointments/${id}`, { status: 'cancelled' });
    fetchAppointments();
  } catch (err) {
    console.error(err);
  }
};

const showCompleteModal = ref(false);
const selectedAppointmentId = ref(null);
const completeForm = ref({
  diagnosis: '',
  medicines: '',
  dosage: '',
  instructions: ''
});

const completeAppointment = (id) => {
  selectedAppointmentId.value = id;
  completeForm.value = {
    diagnosis: '',
    medicines: '',
    dosage: '',
    instructions: ''
  };
  showCompleteModal.value = true;
};

const submitCompletion = async () => {
  if (!selectedAppointmentId.value) return;
  
  try {
    const payload = {
      status: 'completed',
      diagnosis: completeForm.value.diagnosis,
      prescription: {
        medicines: completeForm.value.medicines,
        dosage: completeForm.value.dosage,
        instructions: completeForm.value.instructions
      }
    };

    await api.put(`/appointments/${selectedAppointmentId.value}`, payload);
    
    showCompleteModal.value = false;
    fetchAppointments();
    alert('Appointment completed and prescription saved successfully!');
  } catch (err) {
    console.error('Failed to complete appointment', err);
    alert('Failed to complete appointment.');
  }
};

const rescheduleAppointment = async (appt) => {
  if (!confirm('To reschedule, we will cancel this appointment and redirect you to the doctor\'s page to book a new slot. Proceed?')) return;
  
  try {
    // 1. Cancel current appointment
    await api.put(`/appointments/${appt.id}`, { status: 'cancelled' });
    
    // 2. Redirect to doctor's page
    router.push(`/doctors/${appt.doctor_id}`);
  } catch (err) {
    console.error("Reschedule failed", err);
    alert("Failed to initiate reschedule.");
  }
};

const addDateToSlot = () => {
  if (!currentDateInput.value) return;
  if (!newSlot.value.dates.includes(currentDateInput.value)) {
    newSlot.value.dates.push(currentDateInput.value);
  }
  currentDateInput.value = '';
};

const removeDateFromSlot = (index) => {
  newSlot.value.dates.splice(index, 1);
};

const addSlot = async () => {
  // Combine dates: those in the list + the one currently in the input (if any)
  const datesToProcess = [...newSlot.value.dates];
  if (currentDateInput.value && !datesToProcess.includes(currentDateInput.value)) {
    datesToProcess.push(currentDateInput.value);
  }

  if (datesToProcess.length === 0) {
    alert("Please select at least one date.");
    return;
  }

  if (!newSlot.value.startTime || !newSlot.value.endTime) {
    alert("Please select start and end time.");
    return;
  }

  try {
    let successCount = 0;
    let failCount = 0;

    for (const dateStr of datesToProcess) {
      try {
        const payload = {
          doctor_id: currentUser.value.id,
          available_date: new Date(dateStr).toISOString(),
          time_slot: `${newSlot.value.startTime}-${newSlot.value.endTime}`,
          status: 'available'
        };
        await api.post('/availability/', payload);
        successCount++;
      } catch (err) {
        console.error(`Failed to add slot for ${dateStr}`, err);
        failCount++;
      }
    }

    if (successCount > 0) {
      alert(`${successCount} slot(s) added successfully!${failCount > 0 ? ` (${failCount} failed)` : ''}`);
      showAddSlotModal.value = false;
      if (currentUser.value) {
        fetchSlots(currentUser.value.id);
      }
      // Reset form
      newSlot.value = { dates: [], startTime: '', endTime: '' };
      currentDateInput.value = '';
    } else {
      alert("Failed to add slots. Please try again.");
    }

  } catch (err) {
    console.error("Unexpected error in addSlot", err);
    alert("An unexpected error occurred.");
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