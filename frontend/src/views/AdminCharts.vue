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

            <!-- 1. Patient Analytics Dashboard -->
            <div class="mb-5">
              <h2 class="h4 mb-3 ps-2 border-start border-4 border-primary">1. Patient Analytics Dashboard</h2>
              <div class="row g-4">
                <div class="col-md-3">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-primary">Doctors vs Patients Ratio</h6></div>
                    <div class="card-body"><div class="chart-container"><Pie :data="doctorsVsPatientsData" :options="pieOptions" /></div></div>
                  </div>
                </div>
                <!-- New Charts for Section 1 -->
                 <div class="col-md-3">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-primary">Patient Gender Ratio</h6></div>
                    <div class="card-body"><div class="chart-container"><Doughnut :data="patientGenderData" :options="pieOptions" /></div></div>
                  </div>
                </div>
                 <div class="col-md-3">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-primary">New Registrations (Weekly)</h6></div>
                    <div class="card-body"><div class="chart-container"><Line :data="patientRegistrationsData" :options="lineOptions" /></div></div>
                  </div>
                </div>
                 <div class="col-md-3">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-primary">Age Distribution</h6></div>
                    <div class="card-body"><div class="chart-container"><Line :data="patientAgeTrendData" :options="lineOptions" /></div></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 2. Doctor / Staff Analytics Dashboard -->
            <div class="mb-5">
              <h2 class="h4 mb-3 ps-2 border-start border-4 border-success">2. Doctor / Staff Analytics Dashboard</h2>
              <div class="row g-4">
                <div class="col-md-4">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-success">Doctors per Department</h6></div>
                    <div class="card-body"><div class="chart-container"><Bar :data="doctorsPerDepartmentData" :options="barOptions" /></div></div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-success">Doctor Workload Trend</h6></div>
                    <div class="card-body"><div class="chart-container"><Line :data="doctorTrendData" :options="lineOptions" /></div></div>
                  </div>
                </div>
                  <div class="col-md-4">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-success">Doctor Average Ratings (Real Data)</h6></div>
                    <div class="card-body"><div class="chart-container"><Bar :data="doctorRatingData" :options="ratingBarOptions" /></div></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 3. Appointment Analytics -->
            <div class="mb-5">
              <h2 class="h4 mb-3 ps-2 border-start border-4 border-info">3. Appointment Analytics</h2>
              <div class="row g-4">
                 <div class="col-md-4">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-info">Appointment Status</h6></div>
                    <div class="card-body"><div class="chart-container"><Doughnut :data="appointmentsByStatusData" :options="pieOptions" /></div></div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-info">Booked vs Cancelled (Stacked)</h6></div>
                    <div class="card-body"><div class="chart-container"><Bar :data="appointmentStackedData" :options="barWithLegendOptions" /></div></div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-info">Trend vs Available Slots</h6></div>
                    <div class="card-body"><div class="chart-container"><Bar :data="appointmentTrendData" :options="barWithLegendOptions" /></div></div>
                  </div>
                </div>
                 <div class="col-md-12">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-info">Calendar Heatmap (Mock)</h6></div>
                    <div class="card-body">
                         <!-- Simple Heatmap Table Proxy -->
                         <div class="table-responsive">
                            <table class="table table-bordered text-center table-sm">
                                <thead><tr><th>Time</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th></tr></thead>
                                <tbody>
                                    <tr><td>9-11 AM</td><td class="bg-danger text-white">High</td><td class="bg-warning">Med</td><td class="bg-success text-white">Low</td><td class="bg-danger text-white">High</td><td class="bg-warning">Med</td></tr>
                                    <tr><td>11-1 PM</td><td class="bg-warning">Med</td><td class="bg-danger text-white">High</td><td class="bg-warning">Med</td><td class="bg-warning">Med</td><td class="bg-success text-white">Low</td></tr>
                                    <tr><td>2-4 PM</td><td class="bg-success text-white">Low</td><td class="bg-success text-white">Low</td><td class="bg-danger text-white">High</td><td class="bg-success text-white">Low</td><td class="bg-danger text-white">High</td></tr>
                                </tbody>
                            </table>
                         </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 4. Revenue / Billing Analytics -->
            <div class="mb-5">
              <h2 class="h4 mb-3 ps-2 border-start border-4 border-warning">4. Revenue / Billing Analytics</h2>
              <div class="row g-4">
                <div class="col-md-8">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-warning">Patient Unpaid Appointments Balance</h6></div>
                    <div class="card-body"><div class="chart-container"><Bar :data="patientBillingStatusData" :options="unpaidBarOptions" /></div></div>
                  </div>
                </div>
                 <div class="col-md-4">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-warning">Revenue Growth</h6></div>
                    <div class="card-body"><div class="chart-container"><Line :data="revenueGrowthData" :options="lineOptions" /></div></div>
                  </div>
                </div>
                 <div class="col-md-6">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-warning">Revenue by Department</h6></div>
                    <div class="card-body"><div class="chart-container"><Doughnut :data="revenueByDeptData" :options="pieOptions" /></div></div>
                  </div>
                </div>
                 <div class="col-md-6">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-warning">Monthly Target Completion</h6></div>
                    <div class="card-body"><div class="chart-container"><Doughnut :data="monthlyTargetData" :options="pieOptions" /></div></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 5. Medical Data Analytics -->
            <div class="mb-5">
              <h2 class="h4 mb-3 ps-2 border-start border-4 border-danger">5. Medical Data Analytics</h2>
               <div class="row g-4">
                <div class="col-md-6">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-danger">Disease Severity vs Age (Bubble)</h6></div>
                    <div class="card-body"><div class="chart-container"><Bubble :data="medicalBubbleData" :options="lineOptions" /></div></div>
                  </div>
                </div>
                 <div class="col-md-6">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-danger">Medication Dosage vs Recovery (Scatter)</h6></div>
                    <div class="card-body"><div class="chart-container"><Scatter :data="medicalScatterData" :options="lineOptions" /></div></div>
                  </div>
                </div>
                 <div class="col-md-12">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-danger">Resource Allocation (Treemap Proxy)</h6></div>
                    <div class="card-body">
                         <div class="d-flex flex-wrap h-100">
                             <div class="bg-primary text-white p-4 m-1 flex-grow-1" style="width: 40%">ICU Beds (40%)</div>
                             <div class="bg-success text-white p-4 m-1 flex-grow-1" style="width: 30%">OPD Rooms (30%)</div>
                             <div class="bg-warning text-dark p-4 m-1 flex-grow-1" style="width: 15%">Labs (15%)</div>
                             <div class="bg-info text-white p-4 m-1 flex-grow-1" style="width: 10%">Wards (10%)</div>
                         </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 6. Inventory / Pharmacy Dashboard -->
            <div class="mb-5">
              <h2 class="h4 mb-3 ps-2 border-start border-4 border-secondary">6. Inventory / Pharmacy Dashboard</h2>
               <div class="row g-4">
                <div class="col-md-6">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-secondary">Stock Levels</h6></div>
                    <div class="card-body"><div class="chart-container"><Bar :data="inventoryStockData" :options="barOptions" /></div></div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-secondary">Pareto Chart (Demand vs Cumulative %)</h6></div>
                    <div class="card-body"><div class="chart-container"><Bar :data="inventoryParetoData" :options="barWithLegendOptions" /></div></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 7. Patient History Dashboard -->
            <div class="mb-5">
              <h2 class="h4 mb-3 ps-2 border-start border-4 border-dark">7. Patient History Dashboard</h2>
              <div class="row g-4">
                <div class="col-md-4">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-dark">Patient Visits by Type</h6></div>
                    <div class="card-body"><div class="chart-container"><Pie :data="patientHistoryData" :options="pieOptions" /></div></div>
                  </div>
                </div>
                 <div class="col-md-4">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-dark">Vitals Tracking (Multi-line)</h6></div>
                    <div class="card-body"><div class="chart-container"><Line :data="historyVitalsData" :options="lineOptions" /></div></div>
                  </div>
                </div>
                 <div class="col-md-4">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-dark">Diagnosis Distribution</h6></div>
                    <div class="card-body"><div class="chart-container"><Doughnut :data="historyDiagnosisData" :options="pieOptions" /></div></div>
                  </div>
                </div>
                 <div class="col-md-12">
                  <div class="card shadow mb-4 h-100">
                    <div class="card-header py-3"><h6 class="m-0 fw-bold text-dark">Vitals Risk Heatmap (Mock)</h6></div>
                    <div class="card-body">
                         <div class="table-responsive">
                            <table class="table table-bordered text-center table-sm">
                                <thead><tr><th>Param</th><th>Visit 1</th><th>Visit 2</th><th>Visit 3</th><th>Visit 4</th></tr></thead>
                                <tbody>
                                    <tr><td>BP</td><td class="bg-success text-white">Normal</td><td class="bg-warning">Elevated</td><td class="bg-success text-white">Normal</td><td class="bg-danger text-white">High</td></tr>
                                    <tr><td>HR</td><td class="bg-success text-white">Normal</td><td class="bg-success text-white">Normal</td><td class="bg-warning">High</td><td class="bg-success text-white">Normal</td></tr>
                                    <tr><td>Temp</td><td class="bg-success text-white">Normal</td><td class="bg-danger text-white">Fever</td><td class="bg-success text-white">Normal</td><td class="bg-success text-white">Normal</td></tr>
                                </tbody>
                            </table>
                         </div>
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
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  RadialLinearScale,
  Filler
} from 'chart.js';
import { Bar, Pie, Doughnut, Line, Radar, Bubble, Scatter } from 'vue-chartjs';
import ChartDataLabels from 'chartjs-plugin-datalabels';

// Register ChartJS components
ChartJS.register(
  CategoryScale, 
  LinearScale, 
  RadialLinearScale,
  BarElement, 
  LineElement,
  PointElement,
  Title, 
  Tooltip, 
  Legend, 
  ArcElement, 
  Filler,
  ChartDataLabels
);

const loading = ref(true);
const doctors = ref([]);
const patients = ref([]);
const appointments = ref([]);
const departments = ref([]);

const histories = ref([]);
const feedbackStats = ref([]);

// Chart Options
const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        fontSize: 10,
        boxWidth: 10
      }
    },
    datalabels: {
       display: false
    }
  }
};

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top'
    },
    datalabels: { display: false }
  },
  scales: {
    y: { beginAtZero: true }
  }
};

const radarOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
    datalabels: { display: false }
  },
  scales: {
    r: {
      angleLines: { display: true },
      suggestedMin: 0,
      suggestedMax: 5
    }
  }
};

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    datalabels: {
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

const barWithLegendOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    },
    datalabels: {
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

const unpaidBarOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    },
    tooltip: {
      mode: 'index',
      intersect: false
    },
    datalabels: {
        anchor: 'end',
        align: 'end',
        formatter: (value, context) => {
            // Retrieve the amount from the raw data mapping or separate array
            // context.dataIndex gives us the index
            const amount = context.chart.data.datasets[0].amountData[context.dataIndex];
            return  amount > 0 ? '$' + amount : '';
        },
        font: {
            weight: 'bold'
        },
        color: 'black'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
          display: true,
          text: 'Count of Unpaid Appointments'
      },
      ticks: {
          stepSize: 1
      }
    }
  }
};

const ratingBarOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
        callbacks: {
            label: (context) => {
                const count = context.chart.data.datasets[0].countData[context.dataIndex];
                return `${context.parsed.y} / 5 (${count} reviews)`;
            }
        }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 5,
      title: { display: true, text: 'Average Rating' }
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
        backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#858796'],
        data: Object.values(counts)
      }
    ]
  };
});

const patientsPerDoctorData = computed(() => {
  const labels = doctors.value.map(d => d.user?.name || 'Unknown');
  const data = doctors.value.map(d => d.patient_count || 0);

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

// --- 1. Patient Analytics Additional Data ---
const patientRegistrationsData = computed(() => {
    // Mocking weekly trend based on patient count
    const weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
    return {
        labels: weeks,
        datasets: [{
            label: 'New Registrations',
            backgroundColor: 'rgba(78, 115, 223, 0.2)',
            borderColor: '#4e73df',
            pointBackgroundColor: '#4e73df',
            data: [5, 10, 8, patients.value.length], // Dummy trend ending in total
            fill: true
        }]
    };
});

const patientAgeTrendData = computed(() => {
    // Calculate ages from DOB
    const ages = patients.value.map(p => {
        if (!p.dob) return 0;
        const dob = new Date(p.dob);
        const diff = Date.now() - dob.getTime();
        return Math.floor(diff / (1000 * 60 * 60 * 24 * 365.25));
    });
    
    // Binning ages 0-10, 11-20, etc.
    const bins = {'0-18':0, '19-30':0, '31-50':0, '51+':0};
    ages.forEach(age => {
        if (age <= 18) bins['0-18']++;
        else if (age <= 30) bins['19-30']++;
        else if (age <= 50) bins['31-50']++;
        else bins['51+']++;
    });

    return {
        labels: Object.keys(bins),
        datasets: [{
            label: 'Age Distribution',
            borderColor: '#1cc88a',
            backgroundColor: '#1cc88a',
            data: Object.values(bins),
            tension: 0.4
        }]
    };
});

const patientGenderData = computed(() => {
    // MOCK: Randomly assign gender since it's not in DB
    const male = Math.floor(patients.value.length * 0.55);
    const female = patients.value.length - male;
    return {
        labels: ['Male', 'Female'],
        datasets: [{
            backgroundColor: ['#36b9cc', '#e74a3b'],
            data: [male, female]
        }]
    };
});


// --- 2. Doctor Analytics Additional Data ---
const doctorTrendData = computed(() => {
    // Mocking appointment trend per doctor over a few months
    return {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [
            {
                label: 'Dr. John Doe',
                borderColor: '#4e73df',
                data: [10, 25, 30, 45, 50],
                fill: false
            },
            {
                label: 'Dr. Sarah Smith',
                borderColor: '#1cc88a',
                data: [5, 15, 10, 20, 30],
                fill: false
            }
        ]
    };
});

const doctorRatingData = computed(() => {
    const labels = feedbackStats.value.map(s => s.doctor_name);
    const data = feedbackStats.value.map(s => s.average_rating);
    const counts = feedbackStats.value.map(s => s.review_count);

    return {
        labels: labels,
        datasets: [
            {
                label: 'Average Rating',
                backgroundColor: '#36b9cc',
                data: data,
                countData: counts
            }
        ]
    };
});

// Analytics Data
const analyticsDashboard = ref({});
const analyticsDemographics = ref({});
const analyticsAppointments = ref({});
const analyticsFinancial = ref({});
const analyticsInventory = ref({});
const analyticsGoals = ref([]);

const inventoryStatusData = computed(() => {
    const cats = analyticsInventory.value.category_value || {};
    return {
        labels: Object.keys(cats),
        datasets: [{
            data: Object.values(cats),
            backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b']
        }]
    };
});

const appointmentTrendData = computed(() => {
    const weekly = analyticsAppointments.value.weekly_trend || {};
    return {
        labels: Object.keys(weekly),
        datasets: [{
            label: 'Appointments',
            data: Object.values(weekly),
            borderColor: '#4e73df',
            tension: 0.3,
            fill: true
        }]
    };
});

const revenueByDeptData = computed(() => {
    const depts = analyticsFinancial.value.department_revenue || {};
    return {
        labels: Object.keys(depts),
        datasets: [{
            label: 'Revenue',
            data: Object.values(depts),
            backgroundColor: '#1cc88a'
        }]
    };
});

const patientAgeData = computed(() => {
    const ages = analyticsDemographics.value.age_distribution || {};
    return {
        labels: Object.keys(ages),
        datasets: [{
             data: Object.values(ages),
             backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e']
        }]
    };
});

// Replace Chart Data sources in template with these computed properties
// e.g. <Bar :data="revenueByDeptData" ... />


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

const patientBillingStatusData = computed(() => {
  // Filter out patients with 0 unpaid amount
  const filteredPatients = patients.value.filter(p => p.total_unpaid_amount > 0);

  const labels = filteredPatients.map(p => p.user?.name || 'Unknown');
  const unpaidCount = filteredPatients.map(p => p.unpaid_billings_count || 0);
  const unpaidAmounts = filteredPatients.map(p => p.total_unpaid_amount || 0);

  return {
    labels: labels,
    datasets: [
      {
        label: 'Unpaid Appointments Count',
        backgroundColor: '#e74a3b',
        data: unpaidCount,
        // Custom property to access in formatter
        amountData: unpaidAmounts 
      }
    ]
  };
});

const patientHistoryData = computed(() => {
  const counts = {};
  histories.value.forEach(h => {
    const type = h.visit_type || 'Unknown';
    counts[type] = (counts[type] || 0) + 1;
  });

  return {
    labels: Object.keys(counts),
    datasets: [
      {
        backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e'],
        data: Object.values(counts)
      }
    ]
  };
});

// --- 3. Appointment Analytics ---
const appointmentStackedData = computed(() => {
  return {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    datasets: [
      { label: 'Completed', backgroundColor: '#1cc88a', data: [12, 19, 3, 5, 2] },
      { label: 'Booked', backgroundColor: '#36b9cc', data: [2, 3, 20, 5, 1] },
      { label: 'Cancelled', backgroundColor: '#e74a3b', data: [3, 10, 13, 15, 22] },
    ]
  };
});

// (Removed redundant appointmentTrendData)

// --- 4. Revenue Analytics ---
const revenueGrowthData = computed(() => {
    const totalPaid = patients.value.reduce((acc, p) => acc + (p.paid_billings_count * 100), 0) || 1000; // Mock 100 per billing
    // Mock trend
    return {
        labels: ['Jan', 'Feb', 'Mar', 'Apr'],
        datasets: [{
            label: 'Revenue ($)',
            borderColor: '#f6c23e',
            backgroundColor: 'rgba(246, 194, 62, 0.1)',
            data: [totalPaid*0.2, totalPaid*0.4, totalPaid*0.6, totalPaid],
            fill: true
        }]
    };
});

// (Removed redundant revenueByDeptData)

const monthlyTargetData = computed(() => {
    // Gauge chart proxy using Doughnut
    return {
        labels: ['Achieved', 'Remaining'],
        datasets: [{
            backgroundColor: ['#1cc88a', '#e3e6f0'],
            data: [75, 25],
            circumference: 180,
            rotation: 270
        }]
    };
});

// --- 5. Medical Analytics ---
const medicalBubbleData = computed(() => {
    return {
        datasets: [{
            label: 'Severity vs Age',
            backgroundColor: 'rgba(231, 74, 59, 0.6)',
            data: [
                { x: 20, y: 3, r: 10 },
                { x: 40, y: 7, r: 15 },
                { x: 60, y: 5, r: 8 },
                { x: 80, y: 9, r: 20 }
            ]
        }]
    };
});

const medicalScatterData = computed(() => {
    return {
        datasets: [{
            label: 'Dosage vs Recovery',
            backgroundColor: '#36b9cc',
            data: [
                { x: 10, y: 5 },
                { x: 20, y: 10 },
                { x: 50, y: 3 },
                { x: 100, y: 2 }
            ]
        }]
    };
});

// --- 6. Inventory Analytics ---
const inventoryStockData = computed(() => {
    return {
        labels: ['Paracetamol', 'Ibuprofen', 'Antibiotics', 'Syringes'],
        datasets: [{
            label: 'Stock Level',
            backgroundColor: ['#1cc88a', '#1cc88a', '#e74a3b', '#f6c23e'], // Red if low
            data: [500, 300, 20, 150]
        }]
    };
});

const inventoryParetoData = computed(() => {
    return {
        labels: ['Medicine A', 'Medicine B', 'Medicine C', 'Others'],
        datasets: [
            { type: 'line', label: 'Cumulative %', borderColor: '#4e73df', data: [40, 70, 85, 100], yAxisID: 'y1' },
            { type: 'bar', label: 'Demand', backgroundColor: '#858796', data: [400, 300, 150, 150], yAxisID: 'y' }
        ]
    };
});

// --- 7. History Analytics ---
const historyVitalsData = computed(() => {
    return {
        labels: ['Visit 1', 'Visit 2', 'Visit 3'],
        datasets: [
            { label: 'Systolic BP', borderColor: '#e74a3b', data: [120, 130, 125], fill: false },
            { label: 'Heart Rate', borderColor: '#4e73df', data: [72, 75, 78], fill: false }
        ]
    };
});

const historyDiagnosisData = computed(() => {
    const counts = {};
    if (histories.value && histories.value.length) {
        histories.value.forEach(h => {
             const d = h.diagnosis || 'Pending';
             counts[d] = (counts[d] || 0) + 1;
        });
    } else {
        counts['Flu'] = 10; counts['Fracture'] = 5; counts['Checkup'] = 20;
    }
    
    return {
        labels: Object.keys(counts),
        datasets: [{
            backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
            data: Object.values(counts)
        }]
    };
});

const fetchData = async () => {
  try {
    const [docsRes, patientsRes, apptsRes, deptsRes, historyRes, feedbackRes, dashRes, demoRes, apptTrendRes, finRes, invRes, goalRes] = await Promise.all([
      api.get('/doctors/'),
      api.get('/patients/'),
      api.get('/appointments/'),
      api.get('/departments/'),
      api.get('/history/'),
      api.get('/feedback/stats'),
      api.get('/analytics/dashboard'),
      api.get('/analytics/demographics'),
      api.get('/analytics/appointments'),
      api.get('/analytics/financial'),
      api.get('/analytics/inventory'),
      api.get('/analytics/goals')
    ]);

    doctors.value = docsRes.data;
    patients.value = patientsRes.data;
    appointments.value = apptsRes.data;
    departments.value = deptsRes.data;
    histories.value = historyRes.data;
    feedbackStats.value = feedbackRes.data;
    
    analyticsDashboard.value = dashRes.data;
    analyticsDemographics.value = demoRes.data;
    analyticsAppointments.value = apptTrendRes.data;
    analyticsFinancial.value = finRes.data;
    analyticsInventory.value = invRes.data;
    analyticsGoals.value = goalRes.data;
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
