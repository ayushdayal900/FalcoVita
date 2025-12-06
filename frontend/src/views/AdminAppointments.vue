<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />
    
    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <!-- Top Header -->
      <header class="bg-white border-bottom py-3 px-4 d-flex align-items-center justify-content-between sticky-top z-2 shadow-sm">
        <div>
          <h2 class="h4 fw-bold text-dark mb-0">All Appointments</h2>
          <p class="text-muted small mb-0">Monitor and manage hospital appointments</p>
        </div>
      </header>

      <div class="flex-grow-1 overflow-auto p-4 custom-scrollbar">
        <div class="container-fluid p-0" style="max-width: 1400px;">
          
          <!-- Search Bar -->
          <div class="card border-0 shadow-sm mb-4" style="max-width: 600px;">
            <div class="card-body p-2">
              <SearchBar 
                v-model="search" 
                placeholder="Search by patient or doctor name..." 
                @clear="search = ''"
              />
            </div>
          </div>

          <!-- Filter Tabs -->
          <div class="mb-4">
            <div class="btn-group shadow-sm" role="group">
              <button 
                v-for="status in ['all', 'scheduled', 'completed', 'cancelled']" 
                :key="status"
                @click="filterStatus = status" 
                class="btn btn-sm fw-medium px-4 py-2"
                :class="filterStatus === status ? 'btn-primary' : 'btn-white bg-white text-secondary border-light'"
              >
                {{ status.charAt(0).toUpperCase() + status.slice(1) }}
                <span v-if="status === 'all'" class="badge bg-white text-primary ms-2 rounded-pill">{{ appointments.length }}</span>
              </button>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary mb-3" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted fw-medium">Loading appointments...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="filteredAppointments.length === 0" class="text-center py-5 bg-white rounded-4 border border-dashed">
            <div class="bg-light rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 64px; height: 64px;">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-muted">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="h5 fw-bold text-dark mb-1">No appointments found</h3>
            <p class="text-muted small">There are no appointments with this status.</p>
          </div>

          <!-- Appointments Table -->
          <div v-else class="card border-0 shadow-sm overflow-hidden">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="bg-light">
                  <tr>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Date & Time</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Patient</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Doctor</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Department</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0">Status</th>
                    <th class="px-4 py-3 text-secondary text-uppercase small fw-bold border-0 text-end">Actions</th>
                  </tr>
                </thead>
                <tbody class="border-top-0">
                  <tr v-for="appt in filteredAppointments" :key="appt.id">
                    <td class="px-4 py-3 border-bottom-0">
                      <div class="d-flex flex-column">
                        <span class="fw-bold text-dark">{{ new Date(appt.appointment_date).toLocaleDateString() }}</span>
                        <span class="text-muted small">{{ new Date(appt.appointment_date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}</span>
                      </div>
                    </td>
                    <td class="px-4 py-3 border-bottom-0">
                      <div class="d-flex align-items-center gap-3">
                        <div class="rounded-circle bg-success bg-opacity-10 text-success d-flex align-items-center justify-content-center fw-bold" style="width: 32px; height: 32px; font-size: 0.8rem;">
                          {{ appt.patient?.user?.name?.charAt(0) }}
                        </div>
                        <span class="fw-medium text-dark">{{ appt.patient?.user?.name || 'Unknown' }}</span>
                      </div>
                    </td>
                    <td class="px-4 py-3 border-bottom-0">
                      <div class="d-flex align-items-center gap-3">
                        <div class="rounded-circle bg-primary bg-opacity-10 text-primary d-flex align-items-center justify-content-center fw-bold" style="width: 32px; height: 32px; font-size: 0.8rem;">
                          {{ appt.doctor?.user?.name?.charAt(0) }}
                        </div>
                        <span class="fw-medium text-dark">Dr. {{ appt.doctor?.user?.name || 'Unknown' }}</span>
                      </div>
                    </td>
                    <td class="px-4 py-3 border-bottom-0 text-muted small">{{ appt.department?.name || 'N/A' }}</td>
                    <td class="px-4 py-3 border-bottom-0">
                      <span :class="getStatusClass(appt.status)" class="badge rounded-pill fw-normal px-3 d-inline-flex align-items-center gap-1">
                        <span class="d-inline-block rounded-circle" :class="getStatusDotClass(appt.status)" style="width: 6px; height: 6px;"></span>
                        {{ appt.status }}
                      </span>
                    </td>
                    <td class="px-4 py-3 border-bottom-0 text-end">
                      <div class="d-flex align-items-center justify-content-end gap-2">
                        <button @click="editAppointment(appt)" class="btn btn-sm btn-light text-primary" title="Edit">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button @click="deleteAppointment(appt.id)" class="btn btn-sm btn-light text-danger" title="Delete">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Edit Appointment Modal -->
    <div v-if="showEditModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-bottom-0 pb-0">
            <h5 class="modal-title fw-bold">Edit Appointment</h5>
            <button type="button" class="btn-close" @click="closeEditModal"></button>
          </div>
          
          <div class="modal-body p-4">
            <form @submit.prevent="saveAppointment">
              <div class="mb-3">
                <label class="form-label fw-bold small">Patient</label>
                <input :value="editForm.patient_name" class="form-control bg-light" disabled />
              </div>
              
              <div class="mb-3">
                <label class="form-label fw-bold small">Doctor</label>
                <input :value="editForm.doctor_name" class="form-control bg-light" disabled />
              </div>

              <div class="mb-3">
                <label class="form-label fw-bold small">Date & Time</label>
                <input type="datetime-local" v-model="editForm.appointment_date" class="form-control" required />
              </div>

              <div class="mb-4">
                <label class="form-label fw-bold small">Status</label>
                <select v-model="editForm.status" class="form-select" required>
                  <option value="scheduled">Scheduled</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
              
              <div class="d-flex justify-content-end gap-2 pt-3 border-top">
                <button type="button" @click="closeEditModal" class="btn btn-light">Cancel</button>
                <button type="submit" class="btn btn-primary fw-bold px-4">Update Appointment</button>
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
import Sidebar from '@/components/Sidebar.vue';
import SearchBar from '@/components/SearchBar.vue';
import api from '@/services/api';

const appointments = ref([]);
const loading = ref(true);
const search = ref('');
const filterStatus = ref('all');
const showEditModal = ref(false);
const editingAppointment = ref(null);

const editForm = ref({
  patient_name: '',
  doctor_name: '',
  appointment_date: '',
  status: ''
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

const filteredAppointments = computed(() => {
  let result = appointments.value;
  
  // Filter by status
  if (filterStatus.value !== 'all') {
    result = result.filter(appt => appt.status === filterStatus.value);
  }
  
  // Filter by search term
  if (search.value) {
    const term = search.value.toLowerCase();
    result = result.filter(appt => 
      (appt.patient?.user?.name?.toLowerCase().includes(term)) ||
      (appt.doctor?.user?.name?.toLowerCase().includes(term))
    );
  }
  
  return result;
});

const getStatusClass = (status) => {
  const classes = {
    'scheduled': 'bg-primary bg-opacity-10 text-primary',
    'completed': 'bg-success bg-opacity-10 text-success',
    'cancelled': 'bg-danger bg-opacity-10 text-danger',
    'canceled': 'bg-danger bg-opacity-10 text-danger'
  };
  return classes[status] || 'bg-secondary bg-opacity-10 text-secondary';
};

const getStatusDotClass = (status) => {
  const classes = {
    'scheduled': 'bg-primary',
    'completed': 'bg-success',
    'cancelled': 'bg-danger',
    'canceled': 'bg-danger'
  };
  return classes[status] || 'bg-secondary';
};

const editAppointment = (appt) => {
  editingAppointment.value = appt;
  
  // Convert ISO date to datetime-local format
  const date = new Date(appt.appointment_date);
  const localDate = new Date(date.getTime() - (date.getTimezoneOffset() * 60000));
  const dateTimeLocal = localDate.toISOString().slice(0, 16);
  
  editForm.value = {
    patient_name: appt.patient?.user?.name || 'Unknown',
    doctor_name: `Dr. ${appt.doctor?.user?.name || 'Unknown'}`,
    appointment_date: dateTimeLocal,
    status: appt.status
  };
  showEditModal.value = true;
};

const closeEditModal = () => {
  showEditModal.value = false;
  editingAppointment.value = null;
  editForm.value = {
    patient_name: '',
    doctor_name: '',
    appointment_date: '',
    status: ''
  };
};

const saveAppointment = async () => {
  try {
    await api.put(`/appointments/${editingAppointment.value.id}`, {
      appointment_date: new Date(editForm.value.appointment_date).toISOString(),
      status: editForm.value.status
    });
    alert('Appointment updated successfully');
    closeEditModal();
    fetchAppointments();
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to update appointment');
  }
};

const deleteAppointment = async (id) => {
  if (!confirm('Are you sure you want to delete this appointment?')) return;
  try {
    await api.delete(`/appointments/${id}`);
    alert('Appointment deleted successfully');
    fetchAppointments();
  } catch (err) {
    alert('Failed to delete appointment');
  }
};

onMounted(() => {
  fetchAppointments();
});
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
