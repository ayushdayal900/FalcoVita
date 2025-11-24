<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">All Appointments</h2>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          
          <!-- Filter Tabs -->
          <div class="card p-4 mb-6">
            <div class="flex gap-4">
              <button 
                @click="filterStatus = 'all'" 
                :class="['btn', filterStatus === 'all' ? 'btn-primary' : 'btn-outline', 'text-sm']">
                All ({{ appointments.length }})
              </button>
              <button 
                @click="filterStatus = 'scheduled'" 
                :class="['btn', filterStatus === 'scheduled' ? 'btn-primary' : 'btn-outline', 'text-sm']">
                Scheduled
              </button>
              <button 
                @click="filterStatus = 'completed'" 
                :class="['btn', filterStatus === 'completed' ? 'btn-primary' : 'btn-outline', 'text-sm']">
                Completed
              </button>
              <button 
                @click="filterStatus = 'cancelled'" 
                :class="['btn', filterStatus === 'cancelled' ? 'btn-primary' : 'btn-outline', 'text-sm']">
                Cancelled
              </button>
            </div>
          </div>

          <div v-if="loading" class="text-center py-10">
            <p class="text-muted">Loading appointments...</p>
          </div>

          <div v-else-if="filteredAppointments.length === 0" class="text-center py-10">
            <p class="text-muted">No appointments found.</p>
          </div>

          <div v-else class="card overflow-hidden">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-50 text-muted text-sm border-b border-slate-200">
                  <th class="p-4 font-medium">Date & Time</th>
                  <th class="p-4 font-medium">Patient</th>
                  <th class="p-4 font-medium">Doctor</th>
                  <th class="p-4 font-medium">Department</th>
                  <th class="p-4 font-medium">Status</th>
                  <th class="p-4 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="appt in filteredAppointments" :key="appt.id" class="border-b border-slate-100 hover:bg-slate-50">
                  <td class="p-4 font-medium">{{ formatDateTime(appt.appointment_date) }}</td>
                  <td class="p-4 text-sm">{{ appt.patient?.user?.name || 'Unknown' }}</td>
                  <td class="p-4 text-sm">Dr. {{ appt.doctor?.user?.name || 'Unknown' }}</td>
                  <td class="p-4 text-sm">{{ appt.department?.name || 'N/A' }}</td>
                  <td class="p-4">
                    <span :class="getStatusClass(appt.status)" class="text-xs px-2 py-1 rounded">
                      {{ appt.status }}
                    </span>
                  </td>
                  <td class="p-4">
                    <div class="flex gap-2">
                      <button @click="editAppointment(appt)" class="text-primary hover:underline text-sm font-medium">Edit</button>
                      <button @click="deleteAppointment(appt.id)" class="text-red-500 hover:underline text-sm font-medium">Delete</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>
      </div>
    </main>

    <!-- Edit Appointment Modal -->
    <div v-if="showEditModal" class="modal-overlay">
      <div class="card bg-white w-full max-w-md p-6">
        <h3 class="text-lg font-bold mb-4">Edit Appointment</h3>
        
        <form @submit.prevent="saveAppointment" class="space-y-4">
          <div class="form-group">
            <label class="label">Patient</label>
            <input :value="editForm.patient_name" class="input" disabled />
          </div>
          
          <div class="form-group">
            <label class="label">Doctor</label>
            <input :value="editForm.doctor_name" class="input" disabled />
          </div>

          <div class="form-group">
            <label class="label">Date & Time</label>
            <input type="datetime-local" v-model="editForm.appointment_date" class="input" required />
          </div>

          <div class="form-group">
            <label class="label">Status</label>
            <select v-model="editForm.status" class="input" required>
              <option value="scheduled">Scheduled</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          
          <div class="flex gap-4 mt-6">
            <button type="button" @click="closeEditModal" class="btn btn-outline flex-1">Cancel</button>
            <button type="submit" class="btn btn-primary flex-1">Update</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Sidebar from '@/components/Sidebar.vue';
import api from '@/services/api';

const appointments = ref([]);
const loading = ref(true);
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
  if (filterStatus.value === 'all') return appointments.value;
  return appointments.value.filter(appt => appt.status === filterStatus.value);
});

const formatDateTime = (dateStr) => {
  return new Date(dateStr).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const getStatusClass = (status) => {
  const classes = {
    'scheduled': 'bg-blue-100 text-blue-600',
    'completed': 'bg-green-100 text-green-600',
    'cancelled': 'bg-red-100 text-red-600'
  };
  return classes[status] || 'bg-gray-100 text-gray-600';
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
