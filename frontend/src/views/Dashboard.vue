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

          <!-- Quick Actions and Next Appointment -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Quick Actions Section -->
            <div class="lg:col-span-2">
              <div class="bg-white rounded-2xl p-8 shadow-lg border border-slate-100">
                <h3 class="text-2xl font-bold text-slate-800 mb-6">Quick Actions</h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <!-- Find a Doctor Card -->
                  <router-link 
                    to="/doctors" 
                    class="group relative overflow-hidden rounded-xl p-6 bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
                  >
                    <div class="relative z-10">
                      <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                      </div>
                      <h4 class="text-white font-bold text-lg mb-1">Find a Doctor</h4>
                      <p class="text-blue-100 text-sm">Browse specialists</p>
                    </div>
                    <div class="absolute top-0 right-0 w-24 h-24 bg-white/10 rounded-full -mr-12 -mt-12"></div>
                  </router-link>

                  <!-- My Appointments Card -->
                  <router-link 
                    to="/appointments" 
                    class="group relative overflow-hidden rounded-xl p-6 bg-gradient-to-br from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
                  >
                    <div class="relative z-10">
                      <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                      </div>
                      <h4 class="text-white font-bold text-lg mb-1">My Appointments</h4>
                      <p class="text-purple-100 text-sm">View schedule</p>
                    </div>
                    <div class="absolute top-0 right-0 w-24 h-24 bg-white/10 rounded-full -mr-12 -mt-12"></div>
                  </router-link>

                  <!-- Medical History Card -->
                  <router-link 
                    to="/history" 
                    class="group relative overflow-hidden rounded-xl p-6 bg-gradient-to-br from-emerald-500 to-emerald-600 hover:from-emerald-600 hover:to-emerald-700 transition-all duration-300 hover:shadow-xl hover:-translate-y-1"
                  >
                    <div class="relative z-10">
                      <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                      </div>
                      <h4 class="text-white font-bold text-lg mb-1">Medical History</h4>
                      <p class="text-emerald-100 text-sm">View records</p>
                    </div>
                    <div class="absolute top-0 right-0 w-24 h-24 bg-white/10 rounded-full -mr-12 -mt-12"></div>
                  </router-link>
                </div>
              </div>
            </div>

            <!-- Next Appointment Section -->
            <div class="lg:col-span-1">
              <div class="bg-white rounded-2xl p-8 shadow-lg border border-slate-100 h-full">
                <div class="flex items-center gap-2 mb-6">
                  <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 class="text-2xl font-bold text-slate-800">Next Appointment</h3>
                </div>
                
                <div v-if="upcomingAppointments.length > 0" class="space-y-4">
                  <div class="relative overflow-hidden rounded-xl p-6 bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-100">
                    <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-200/30 to-purple-200/30 rounded-full -mr-16 -mt-16"></div>
                    <div class="relative z-10">
                      <div class="flex items-start justify-between mb-4">
                        <div class="flex-1">
                          <p class="text-sm text-slate-500 mb-1">Doctor</p>
                          <p class="font-bold text-lg text-slate-800">
                            Dr. {{ upcomingAppointments[0].doctor?.user?.name }}
                          </p>
                        </div>
                        <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                        </div>
                      </div>
                      
                      <div class="space-y-3">
                        <div class="flex items-center gap-2">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                          </svg>
                          <span class="text-sm text-slate-600">{{ upcomingAppointments[0].department?.name }}</span>
                        </div>
                        
                        <div class="flex items-center gap-2">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          <span class="text-sm font-semibold text-slate-700">
                            {{ new Date(upcomingAppointments[0].appointment_date).toLocaleString('en-US', { 
                              month: 'short', 
                              day: 'numeric', 
                              year: 'numeric',
                              hour: 'numeric',
                              minute: '2-digit',
                              hour12: true 
                            }) }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <router-link 
                    to="/appointments" 
                    class="block w-full py-3 px-6 rounded-xl text-center font-medium text-white bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-md hover:shadow-lg"
                  >
                    Book Appointment
                  </router-link>
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