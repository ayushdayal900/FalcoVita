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

      <div class="p-6 overflow-y-auto">
        <div class="max-w-7xl mx-auto">

          
          <!-- Departments Section -->
          <div class="mb-10">
            <h3 class="text-xl font-bold text-slate-800 mb-6">Departments</h3>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="dept in departments" :key="dept.id" class="group bg-white rounded-2xl p-6 border border-slate-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col h-full">
                <div class="mb-4">
                  <h4 class="text-lg font-bold text-slate-800 group-hover:text-blue-600 transition-colors">{{ dept.name }}</h4>
                  <div class="h-1 w-12 bg-blue-100 rounded-full mt-2 group-hover:bg-blue-500 transition-colors"></div>
                </div>
                
                <p class="text-slate-500 text-sm mb-6 line-clamp-2 flex-1 leading-relaxed">
                  {{ dept.overview || 'Specialized medical care and treatment provided by our expert team.' }}
                </p>
                
                <router-link 
                  :to="`/doctors?department_id=${dept.id}`" 
                  class="mt-auto w-full py-2.5 px-4 rounded-xl text-sm font-medium text-blue-600 bg-blue-50 hover:bg-blue-600 hover:text-white transition-all duration-300 flex items-center justify-center gap-2 group/btn"
                >
                  View Doctors
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transform group-hover/btn:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </router-link>
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