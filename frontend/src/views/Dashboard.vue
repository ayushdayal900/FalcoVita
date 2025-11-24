<template>
  <div class="dashboard-layout flex h-screen overflow-hidden">
    <Sidebar />

    <main class="flex-1 flex flex-col overflow-hidden bg-slate-50">
      <header class="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-6 shadow-sm">
        <h2 class="text-xl font-semibold">Dashboard</h2>

        <div class="px-4 py-2 rounded-xl bg-gradient-to-r from-blue-100 to-blue-200 border border-blue-300 shadow-sm">
          <p class="text-sm">
            <span class="text-slate-600">Welcome back,</span>
            <span class="text-blue-700 font-semibold ml-1">{{ userName }}</span>
          </p>
        </div>
      </header>

      <div class="flex-1 overflow-auto p-6">
        <div class="container mx-auto">
          
          <!-- Doctor Dashboard -->
          <div v-if="userRole === 'doctor'" class="space-y-6">
            <DoctorDashboard
              :todayAppointments="todayAppointments"
              :totalPatients="totalPatients"
              :weekCompleted="weekCompleted"
              :upcomingAppointments="upcomingAppointments"
              :patients="patientsList"
              :departmentId="doctorDepartmentId"
            />
          </div>

          <!-- Patient Dashboard -->
          <div v-if="userRole === 'patient'" class="space-y-6">
            
            <!-- Departments List (New) -->
            <div class="card p-6 mb-6">
              <h3 class="text-lg font-bold mb-4">Departments</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div v-for="dept in departments" :key="dept.id" class="p-4 border rounded hover:shadow-md transition-shadow">
                  <h4 class="font-bold text-primary">{{ dept.name }}</h4>
                  <p class="text-sm text-muted mt-1">{{ dept.overview || 'No description' }}</p>
                  <router-link to="/doctors" class="btn btn-outline btn-sm mt-3 w-full text-center block">
                    View Doctors
                  </router-link>
                </div>
                <div v-if="departments.length === 0" class="col-span-3 text-center text-muted">
                  No departments found.
                </div>
              </div>
            </div>

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
                  <router-link to="/doctors" class="block btn btn-primary text-center">
                    Find a Doctor
                  </router-link>
                  <router-link to="/appointments" class="block btn btn-outline text-center">
                    My Appointments
                  </router-link>
                  <router-link to="/history" class="block btn btn-outline text-center">
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
import DoctorDashboard from "@/components/DoctorDashboard.vue";

const store = useStore();
const userRole = computed(() => store.getters.userRole);
const userName = computed(() => store.getters.currentUser?.name || 'User');

const todayAppointments = ref(0);
const totalPatients = ref(0);
const weekCompleted = ref(0);
const upcomingAppointments = ref([]);
const totalVisits = ref(0);
const lastVisitDate = ref('N/A');
const departments = ref([]);
const patientsList = ref([]);
const doctorDepartmentId = ref(null);

const fetchDoctorStats = async () => {
  try {
    const doctorId = store.getters.currentUser?.id;

    // Fetch doctor details to get department_id
    const doctorRes = await api.get(`/doctors/${doctorId}`);
    if (doctorRes.data) {
        doctorDepartmentId.value = doctorRes.data.department_id;
    }

    const appointmentsRes = await api.get('/appointments/');
    const allAppointments = appointmentsRes.data;

    // Filter only this doctor's appointments
    const appointments = allAppointments.filter(a => a.doctor_id === doctorId);

    const today = new Date().toDateString();

    todayAppointments.value = appointments.filter(a =>
      new Date(a.appointment_date).toDateString() === today &&
      a.status === 'scheduled'
    ).length;

    upcomingAppointments.value = appointments
      .filter(a => a.status === 'scheduled' && new Date(a.appointment_date) > new Date())
      .sort((a, b) => new Date(a.appointment_date) - new Date(b.appointment_date));

    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);

    weekCompleted.value = appointments.filter(a =>
      a.status === 'completed' && new Date(a.appointment_date) > weekAgo
    ).length;

    // Get unique patients managed by this doctor
    const patientsRes = await api.get('/patients/');
    const patients = patientsRes.data;

    patientsList.value = patients.filter(
      p => p.patient?.doctor_id === doctorId
    );
    totalPatients.value = patientsList.value.length;

  } catch (err) {
    console.error("Failed to fetch doctor stats", err);
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

    // Fetch Departments
    const deptRes = await api.get('/departments/');
    departments.value = deptRes.data;

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