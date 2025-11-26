<template>
  <div class="dashboard-layout flex h-screen overflow-hidden bg-slate-50">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden relative">
      <!-- Top Header -->
      <header class="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10">
        <div>
          <h2 class="text-2xl font-bold text-slate-800">All Appointments</h2>
          <p class="text-sm text-slate-500">Monitor and manage hospital appointments</p>
        </div>
      </header>

      <div class="flex-1 overflow-y-auto p-8 custom-scrollbar">
        <div class="max-w-7xl mx-auto">
          
          <!-- Search Bar -->
          <SearchBar 
            v-model="search" 
            placeholder="Search by patient or doctor name..." 
            @clear="search = ''"
            class="mb-6"
          />

          <!-- Filter Tabs -->
          <div class="bg-white rounded-2xl p-2 shadow-sm border border-slate-100 mb-6 inline-flex">
            <button 
              v-for="status in ['all', 'scheduled', 'completed', 'cancelled']" 
              :key="status"
              @click="filterStatus = status" 
              :class="[
                'px-6 py-2.5 rounded-xl text-sm font-medium transition-all',
                filterStatus === status 
                  ? 'bg-primary-600 text-white shadow-lg shadow-primary-500/30' 
                  : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'
              ]">
              {{ status.charAt(0).toUpperCase() + status.slice(1) }}
              <span v-if="status === 'all'" class="ml-2 bg-white/20 px-1.5 py-0.5 rounded-full text-xs">{{ appointments.length }}</span>
            </button>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="flex flex-col items-center justify-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mb-4"></div>
            <p class="text-slate-500 font-medium">Loading appointments...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="filteredAppointments.length === 0" class="flex flex-col items-center justify-center py-20 bg-white rounded-3xl border border-dashed border-slate-300">
            <div class="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mb-4 text-slate-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-lg font-bold text-slate-800 mb-1">No appointments found</h3>
            <p class="text-slate-500">There are no appointments with this status.</p>
          </div>

          <!-- Appointments Table -->
          <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="bg-slate-50/50 border-b border-slate-200">
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Date & Time</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Patient</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Doctor</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Department</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                    <th class="p-5 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">Actions</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-for="appt in filteredAppointments" :key="appt.id" class="hover:bg-slate-50/80 transition-colors group">
                    <td class="p-5">
                      <div class="flex flex-col">
                        <span class="font-bold text-slate-800">{{ new Date(appt.appointment_date).toLocaleDateString() }}</span>
                        <span class="text-xs text-slate-500">{{ new Date(appt.appointment_date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}</span>
                      </div>
                    </td>
                    <td class="p-5">
                      <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center text-xs font-bold">
                          {{ appt.patient?.user?.name?.charAt(0) }}
                        </div>
                        <span class="font-medium text-slate-700">{{ appt.patient?.user?.name || 'Unknown' }}</span>
                      </div>
                    </td>
                    <td class="p-5">
                      <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold">
                          {{ appt.doctor?.user?.name?.charAt(0) }}
                        </div>
                        <span class="font-medium text-slate-700">Dr. {{ appt.doctor?.user?.name || 'Unknown' }}</span>
                      </div>
                    </td>
                    <td class="p-5 text-sm text-slate-600">{{ appt.department?.name || 'N/A' }}</td>
                    <td class="p-5">
                      <span :class="getStatusClass(appt.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize">
                        <span class="w-1.5 h-1.5 rounded-full mr-1.5" :class="getStatusDotClass(appt.status)"></span>
                        {{ appt.status }}
                      </span>
                    </td>
                    <td class="p-5 text-right">
                      <div class="flex items-center justify-end gap-2">
                        <button @click="editAppointment(appt)" class="p-2 text-slate-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-all" title="Edit">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button @click="deleteAppointment(appt.id)" class="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all" title="Delete">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
    <div v-if="showEditModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-bold text-slate-800">Edit Appointment</h3>
          <button @click="closeEditModal" class="text-slate-400 hover:text-slate-600 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="saveAppointment" class="space-y-5">
          <div class="form-group">
            <label class="label">Patient</label>
            <input :value="editForm.patient_name" class="input bg-slate-50 text-slate-500" disabled />
          </div>
          
          <div class="form-group">
            <label class="label">Doctor</label>
            <input :value="editForm.doctor_name" class="input bg-slate-50 text-slate-500" disabled />
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
          
          <div class="flex gap-4 pt-4 border-t border-slate-100 mt-4">
            <button type="button" @click="closeEditModal" class="btn btn-outline flex-1 rounded-xl">Cancel</button>
            <button type="submit" class="btn btn-primary flex-1 rounded-xl shadow-lg shadow-primary-500/20">Update Appointment</button>
          </div>
        </form>
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
    'scheduled': 'bg-blue-50 text-blue-700',
    'completed': 'bg-emerald-50 text-emerald-700',
    'cancelled': 'bg-red-50 text-red-700',
    'canceled': 'bg-red-50 text-red-700'
  };
  return classes[status] || 'bg-slate-50 text-slate-700';
};

const getStatusDotClass = (status) => {
  const classes = {
    'scheduled': 'bg-blue-500',
    'completed': 'bg-emerald-500',
    'cancelled': 'bg-red-500',
    'canceled': 'bg-red-500'
  };
  return classes[status] || 'bg-slate-500';
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
