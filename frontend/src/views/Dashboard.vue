<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />

    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">
        <h2 class="text-lg font-medium">Dashboard</h2>
        <div class="text-sm text-muted">
          Welcome back, <span class="font-medium text-main">{{ userName }}</span>
        </div>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          
          <!-- Doctor Dashboard -->
          <div v-if="userRole === 'doctor'" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="card p-6">
                <h3 class="text-sm font-medium text-muted mb-2">Today's Appointments</h3>
                <p class="text-3xl font-bold text-primary">{{ todayAppointments }}</p>
              </div>
              <div class="card p-6">
                <h3 class="text-sm font-medium text-muted mb-2">Total Patients</h3>
                <p class="text-3xl font-bold">{{ totalPatients }}</p>
              </div>
              <div class="card p-6">
                <h3 class="text-sm font-medium text-muted mb-2">Completed This Week</h3>
                <p class="text-3xl font-bold text-green-600">{{ weekCompleted }}</p>
              </div>
            </div>

            <div class="card p-6">
              <h3 class="text-lg font-bold mb-4">Upcoming Appointments</h3>
              <div v-if="upcomingAppointments.length === 0" class="text-center py-8 text-muted">
                No upcoming appointments
              </div>
              <div v-else class="space-y-3">
                <div v-for="appt in upcomingAppointments.slice(0, 5)" :key="appt.id" 
                     class="flex justify-between items-center p-3 bg-slate-50 rounded">
                  <div>
                    <p class="font-medium">{{ appt.patient?.user?.name || 'Patient' }}</p>
                    <p class="text-sm text-muted">
                      {{ new Date(appt.appointment_date).toLocaleString() }}
                    </p>
                  </div>
                  <router-link to="/appointments" class="text-primary hover:underline text-sm">
                    View Details
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- Patient Dashboard -->
          <div v-if="userRole === 'patient'" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div class="card p-6">
                <h3 class="text-sm font-medium text-muted mb-2">Upcoming Appointments</h3>
                <p class="text-3xl font-bold text-primary">{{ upcomingAppointments.length }}</p>
              </div>
              <div class="card p-6">
                <h3 class="text-sm font-medium text-muted mb-2">Total Visits</h3>
                <p class="text-3xl font-bold">{{ totalVisits }}</p>
              </div>
              <div class="card p-6">
                <h3 class="text-sm font-medium text-muted mb-2">Last Visit</h3>
                <p class="text-sm font-medium">{{ lastVisitDate }}</p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="card p-6">
                <h3 class="text-lg font-bold mb-4">Quick Actions</h3>
                <div class="space-y-3">
                  <router-link to="/doctors" class="block btn btn-primary">
                    Find a Doctor
                  </router-link>
                  <router-link to="/appointments" class="block btn btn-outline">
                    My Appointments
                  </router-link>
                  <router-link to="/history" class="block btn btn-outline">
                    Medical History
                  </router-link>
                </div>
              </div>

              <div class="card p-6">
                <h3 class="text-lg font-bold mb-4">Next Appointment</h3>
                <div v-if="upcomingAppointments.length > 0">
                  <div class="p-4 bg-blue-50 rounded border border-blue-200">
                    <p class="font-medium text-primary">
                      Dr. {{ upcomingAppointments[0].doctor?.user?.name }}
                    </p>
                    <p class="text-sm text-muted mt-1">
                      {{ upcomingAppointments[0].department?.name }}
                    </p>
                    <p class="text-sm font-medium mt-2">
                      {{ new Date(upcomingAppointments[0].appointment_date).toLocaleString() }}
                    </p>
                  </div>
                </div>
                <div v-else class="text-center py-8 text-muted">
                  No upcoming appointments
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import Sidebar from '@/components/Sidebar.vue';
import api from '@/services/api';

const store = useStore();
const userRole = computed(() => store.getters.userRole);
const userName = computed(() => store.getters.currentUser?.name || 'User');

const todayAppointments = ref(0);
const totalPatients = ref(0);
const weekCompleted = ref(0);
const upcomingAppointments = ref([]);
const totalVisits = ref(0);
const lastVisitDate = ref('N/A');

const fetchDoctorStats = async () => {
  try {
    const appointmentsRes = await api.get('/appointments/');
    const appointments = appointmentsRes.data;
    
    const today = new Date().toDateString();
    todayAppointments.value = appointments.filter(a => 
      new Date(a.appointment_date).toDateString() === today && a.status === 'scheduled'
    ).length;
    
    upcomingAppointments.value = appointments.filter(a => 
      a.status === 'scheduled' && new Date(a.appointment_date) > new Date()
    ).sort((a, b) => new Date(a.appointment_date) - new Date(b.appointment_date));
    
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    weekCompleted.value = appointments.filter(a => 
      a.status === 'completed' && new Date(a.appointment_date) > weekAgo
    ).length;
    
    const patientsRes = await api.get('/patients/');
    totalPatients.value = patientsRes.data.length;
  } catch (err) {
    console.error('Failed to fetch doctor stats', err);
  }
};

const fetchPatientStats = async () => {
  try {
    const appointmentsRes = await api.get('/appointments/');
    const appointments = appointmentsRes.data;
    
    upcomingAppointments.value = appointments.filter(a => 
      a.status === 'scheduled' && new Date(a.appointment_date) > new Date()
    ).sort((a, b) => new Date(a.appointment_date) - new Date(b.appointment_date));
    
    totalVisits.value = appointments.filter(a => a.status === 'completed').length;
    
    const completed = appointments.filter(a => a.status === 'completed')
      .sort((a, b) => new Date(b.appointment_date) - new Date(a.appointment_date));
    
    if (completed.length > 0) {
      lastVisitDate.value = new Date(completed[0].appointment_date).toLocaleDateString();
    }
  } catch (err) {
    console.error('Failed to fetch patient stats', err);
  }
};

onMounted(() => {
  if (userRole.value === 'doctor') {
    fetchDoctorStats();
  } else if (userRole.value === 'patient') {
    fetchPatientStats();
  }
});
</script>

<style scoped>
.bg-slate-50 { background-color: #f8fafc; }
.text-green-600 { color: #16a34a; }
.bg-blue-50 { background-color: #eff6ff; }
.border-blue-200 { border-color: #bfdbfe; }
.space-y-6 > * + * { margin-top: 1.5rem; }
.space-y-3 > * + * { margin-top: 0.75rem; }
</style>