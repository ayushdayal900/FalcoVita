<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />

    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <header class="bg-white border-bottom py-3 px-4 d-flex align-items-center justify-content-between shadow-sm sticky-top z-2">
        <h2 class="h4 fw-bold text-dark mb-0">Dashboard</h2>

        <div class="d-flex align-items-center bg-primary bg-opacity-10 border border-primary border-opacity-25 rounded-pill px-3 py-2">
          <span class="text-muted small me-1">Welcome back,</span>
          <span class="text-primary fw-bold small">{{ userName }}</span>
        </div>
      </header>

      <div class="flex-grow-1 overflow-auto p-4 custom-scrollbar">
        <div class="container-fluid p-0" style="max-width: 1400px;">

          <!-- Doctor Dashboard View -->
          <template v-if="userRole === 'doctor'">
            <DoctorDashboard 
              :todayAppointments="todayAppointments"
              :totalPatients="totalPatients"
              :weekCompleted="weekCompleted"
              :upcomingAppointments="upcomingAppointments"
              :patients="patientsList"
              :departmentId="doctorDepartmentId"
            />
          </template>

          <!-- Patient Dashboard View -->
          <template v-else>
            <div class="mb-5">
              <h3 class="h5 fw-bold text-dark mb-4">Our Departments</h3>

              <div class="row g-4">
                <div v-for="dept in departments" :key="dept.id" class="col-md-6 col-lg-4">
                  <div class="card h-100 border-0 shadow-sm hover-lift transition-all">
                    <div class="card-body p-4 d-flex flex-column">
                      <div class="mb-3">
                        <h4 class="h5 fw-bold text-dark mb-2">{{ dept.name }}</h4>
                        <div class="progress" style="height: 4px;">
                          <div class="progress-bar bg-primary" role="progressbar" style="width: 40px;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                      </div>
                      
                      <p class="text-muted small mb-4 flex-grow-1">
                        {{ dept.overview || 'Specialized medical care and treatment provided by our expert team.' }}
                      </p>
                      
                      <router-link 
                        :to="`/doctors?department_id=${dept.id}`" 
                        class="btn btn-light text-primary w-100 fw-bold d-flex align-items-center justify-content-center gap-2 mt-auto"
                      >
                        View Doctors
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                        </svg>
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>

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
  } else {
    // Default to patient stats/view if not doctor (e.g. patient or admin viewing dashboard route, though admin has separate dashboard)
    fetchPatientStats();
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