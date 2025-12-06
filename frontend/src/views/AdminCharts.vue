<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />
    
    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <div class="flex-grow-1 overflow-auto p-4 custom-scrollbar">
        <div class="container-fluid py-4">
          <h1 class="h3 mb-4 text-gray-800">Hospital Analytics</h1>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>

          <div v-else class="row g-4">
            <!-- Chart 1: Doctors vs Patients -->
            <div class="col-md-4">
              <div class="card shadow mb-4 h-100">
                <div class="card-header py-3">
                  <h6 class="m-0 fw-bold text-primary">Doctors vs Patients</h6>
                </div>
                <div class="card-body">
                  <div class="chart-container" style="position: relative; height: 300px;">
                    <Pie :data="doctorsVsPatientsData" :options="pieOptions" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Chart 2: Appointments per Doctor -->
            <div class="col-md-4">
              <div class="card shadow mb-4 h-100">
                <div class="card-header py-3">
                  <h6 class="m-0 fw-bold text-primary">Appointments per Doctor</h6>
                </div>
                <div class="card-body">
                  <div class="chart-container" style="position: relative; height: 300px;">
                    <Bar :data="appointmentsPerDoctorData" :options="barOptions" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Chart 3: Doctor Experience -->
            <div class="col-md-4">
              <div class="card shadow mb-4 h-100">
                <div class="card-header py-3">
                  <h6 class="m-0 fw-bold text-primary">Doctor Experience (Years)</h6>
                </div>
                <div class="card-body">
                  <div class="chart-container" style="position: relative; height: 300px;">
                    <Bar :data="doctorExperienceData" :options="barOptions" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Chart 4: Appointments by Status -->
            <div class="col-md-4">
              <div class="card shadow mb-4 h-100">
                <div class="card-header py-3">
                  <h6 class="m-0 fw-bold text-primary">Appointments by Status</h6>
                </div>
                <div class="card-body">
                  <div class="chart-container" style="position: relative; height: 300px;">
                    <Doughnut :data="appointmentsByStatusData" :options="pieOptions" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Chart 5: Patients per Doctor -->
            <div class="col-md-4">
              <div class="card shadow mb-4 h-100">
                <div class="card-header py-3">
                  <h6 class="m-0 fw-bold text-primary">Patients per Doctor</h6>
                </div>
                <div class="card-body">
                  <div class="chart-container" style="position: relative; height: 300px;">
                    <Bar :data="patientsPerDoctorData" :options="barOptions" />
                  </div>
                </div>
              </div>
            </div>

            <!-- Chart 6: Doctors per Department -->
            <div class="col-md-4">
              <div class="card shadow mb-4 h-100">
                <div class="card-header py-3">
                  <h6 class="m-0 fw-bold text-primary">Doctors per Department</h6>
                </div>
                <div class="card-body">
                  <div class="chart-container" style="position: relative; height: 300px;">
                    <Pie :data="doctorsPerDepartmentData" :options="pieOptions" />
                  </div>
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
import { ref, onMounted, computed } from 'vue';
import Sidebar from '@/components/Sidebar.vue';
import api from '@/services/api';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement
} from 'chart.js';
import { Bar, Pie, Doughnut } from 'vue-chartjs';

// Register ChartJS components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

const loading = ref(true);
const doctors = ref([]);
const patients = ref([]);
const appointments = ref([]);
const departments = ref([]);

// Chart Options
const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom'
    }
  }
};

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 1
      }
    }
  }
};

// Data Processing
const doctorsVsPatientsData = computed(() => {
  return {
    labels: ['Doctors', 'Patients'],
    datasets: [
      {
        backgroundColor: ['#4e73df', '#1cc88a'],
        data: [doctors.value.length, patients.value.length]
      }
    ]
  };
});

const appointmentsPerDoctorData = computed(() => {
  // Count appointments per doctor
  const counts = {};
  appointments.value.forEach(appt => {
    const docName = appt.doctor?.user?.name || 'Unknown';
    counts[docName] = (counts[docName] || 0) + 1;
  });

  return {
    labels: Object.keys(counts),
    datasets: [
      {
        label: 'Appointments',
        backgroundColor: '#36b9cc',
        data: Object.values(counts)
      }
    ]
  };
});

const doctorExperienceData = computed(() => {
  const labels = doctors.value.map(d => d.user?.name || 'Unknown');
  const data = doctors.value.map(d => d.experience || 0);

  return {
    labels: labels,
    datasets: [
      {
        label: 'Years of Experience',
        backgroundColor: '#f6c23e',
        data: data
      }
    ]
  };
});

const appointmentsByStatusData = computed(() => {
  const counts = {};
  appointments.value.forEach(appt => {
    const status = appt.status || 'Unknown';
    counts[status] = (counts[status] || 0) + 1;
  });

  return {
    labels: Object.keys(counts),
    datasets: [
      {
        backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b'],
        data: Object.values(counts)
      }
    ]
  };
});

const patientsPerDoctorData = computed(() => {
  // This is an approximation based on appointments, as we don't have a direct patient-doctor assignment table loaded here
  // Or we can count unique patients per doctor from appointments
  const doctorPatients = {};
  
  appointments.value.forEach(appt => {
    const docName = appt.doctor?.user?.name || 'Unknown';
    const patientId = appt.patient_id;
    
    if (!doctorPatients[docName]) {
      doctorPatients[docName] = new Set();
    }
    doctorPatients[docName].add(patientId);
  });

  const labels = Object.keys(doctorPatients);
  const data = Object.values(doctorPatients).map(set => set.size);

  return {
    labels: labels,
    datasets: [
      {
        label: 'Unique Patients',
        backgroundColor: '#858796',
        data: data
      }
    ]
  };
});

const doctorsPerDepartmentData = computed(() => {
  const counts = {};
  departments.value.forEach(dept => {
    counts[dept.name] = dept.doctor_count || 0;
  });

  return {
    labels: Object.keys(counts),
    datasets: [
      {
        backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796'],
        data: Object.values(counts)
      }
    ]
  };
});

const fetchData = async () => {
  try {
    const [docsRes, patientsRes, apptsRes, deptsRes] = await Promise.all([
      api.get('/doctors/'),
      api.get('/patients/'),
      api.get('/appointments/'),
      api.get('/departments/')
    ]);

    doctors.value = docsRes.data;
    patients.value = patientsRes.data;
    appointments.value = apptsRes.data;
    departments.value = deptsRes.data;
  } catch (err) {
    console.error("Failed to fetch chart data", err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.chart-container {
  position: relative;
  margin: auto;
  height: 300px;
  width: 100%;
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
