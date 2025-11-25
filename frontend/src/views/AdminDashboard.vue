<template>
  <div class="dashboard-layout flex h-screen overflow-hidden bg-slate-50">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden relative">
      <!-- Top Header -->
      <header class="h-20 bg-white/80 backdrop-blur-md border-b border-slate-200 flex items-center justify-between px-8 sticky top-0 z-10">
        <div>
          <h2 class="text-2xl font-bold text-slate-800">Admin Dashboard</h2>
          <p class="text-sm text-slate-500">Overview of hospital operations</p>
        </div>
        <div class="flex gap-3">
          <button @click="showDoctorModal = true" class="btn bg-primary-600 hover:bg-primary-700 text-white shadow-lg shadow-primary-500/30 flex items-center gap-2 px-4 py-2.5 rounded-xl transition-all hover:-translate-y-0.5">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Doctor
          </button>
          <button @click="showDepartmentModal = true" class="btn bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 flex items-center gap-2 px-4 py-2.5 rounded-xl transition-all">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            Departments
          </button>
        </div>
      </header>

      <div class="flex-1 overflow-y-auto p-8 custom-scrollbar">
        <div class="max-w-7xl mx-auto space-y-8">
          
          <!-- Statistics Cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <!-- Total Doctors -->
            <div class="relative overflow-hidden rounded-2xl p-6 bg-gradient-to-br from-blue-500 to-blue-600 text-white shadow-xl shadow-blue-500/20 cursor-pointer hover:scale-[1.02] transition-transform" @click="showDoctorsList">
              <div class="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-white/20 rounded-full blur-2xl"></div>
              <div class="relative z-10">
                <div class="flex justify-between items-start mb-4">
                  <div class="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                  <span class="text-xs font-medium bg-white/20 px-2 py-1 rounded-full">Active</span>
                </div>
                <h3 class="text-3xl font-bold mb-1">{{ stats.total_doctors }}</h3>
                <p class="text-blue-100 text-sm font-medium">Total Doctors</p>
              </div>
            </div>

            <!-- Total Patients -->
            <div class="relative overflow-hidden rounded-2xl p-6 bg-gradient-to-br from-emerald-500 to-emerald-600 text-white shadow-xl shadow-emerald-500/20 cursor-pointer hover:scale-[1.02] transition-transform" @click="showPatientsList">
              <div class="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-white/20 rounded-full blur-2xl"></div>
              <div class="relative z-10">
                <div class="flex justify-between items-start mb-4">
                  <div class="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </div>
                  <span class="text-xs font-medium bg-white/20 px-2 py-1 rounded-full">+12%</span>
                </div>
                <h3 class="text-3xl font-bold mb-1">{{ stats.total_patients }}</h3>
                <p class="text-emerald-100 text-sm font-medium">Total Patients</p>
              </div>
            </div>

            <!-- Total Appointments -->
            <div class="relative overflow-hidden rounded-2xl p-6 bg-gradient-to-br from-violet-500 to-violet-600 text-white shadow-xl shadow-violet-500/20 cursor-pointer hover:scale-[1.02] transition-transform" @click="showAllAppointments">
              <div class="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-white/20 rounded-full blur-2xl"></div>
              <div class="relative z-10">
                <div class="flex justify-between items-start mb-4">
                  <div class="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                <h3 class="text-3xl font-bold mb-1">{{ stats.total_appointments }}</h3>
                <p class="text-violet-100 text-sm font-medium">Total Appointments</p>
              </div>
            </div>

            <!-- Upcoming -->
            <div class="relative overflow-hidden rounded-2xl p-6 bg-gradient-to-br from-orange-500 to-orange-600 text-white shadow-xl shadow-orange-500/20 cursor-pointer hover:scale-[1.02] transition-transform" @click="showUpcomingAppointments">
              <div class="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-white/20 rounded-full blur-2xl"></div>
              <div class="relative z-10">
                <div class="flex justify-between items-start mb-4">
                  <div class="p-2 bg-white/20 rounded-lg backdrop-blur-sm">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <span class="text-xs font-medium bg-white/20 px-2 py-1 rounded-full">Next 24h</span>
                </div>
                <h3 class="text-3xl font-bold mb-1">{{ stats.upcoming_appointments }}</h3>
                <p class="text-orange-100 text-sm font-medium">Upcoming</p>
              </div>
            </div>
          </div>

          <!-- Search Section -->
          <div class="bg-white rounded-2xl p-6 shadow-sm border border-slate-100">
            <h3 class="text-lg font-bold text-slate-800 mb-4">Quick Search</h3>
            <SearchBar 
              v-model="searchQuery" 
              v-model:searchType="searchType"
              placeholder="Search by name, email or ID..."
              :showTypeSelector="true"
              :types="['doctor', 'patient']"
              @search="performSearch"
              @clear="searchQuery = ''; searchResults = null"
            />

            <!-- Search Results -->
            <div v-if="searchResults" class="mt-6 space-y-6 animate-fade-in">
              <div v-if="searchResults.doctors.length > 0">
                <h4 class="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-3">Doctors Found</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div v-for="doc in searchResults.doctors" :key="doc.id" 
                       class="flex justify-between items-center p-4 bg-slate-50 rounded-xl border border-slate-100 hover:border-primary-200 transition-colors">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center font-bold">
                        {{ doc.name.charAt(0) }}
                      </div>
                      <div>
                        <p class="font-bold text-slate-800">{{ doc.name }}</p>
                        <p class="text-xs text-slate-500">{{ doc.email }}</p>
                      </div>
                    </div>
                    <div class="flex gap-2">
                      <button @click="editDoctor(doc)" class="p-2 text-slate-400 hover:text-primary-600 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button @click="deleteDoctor(doc.id)" class="p-2 text-slate-400 hover:text-red-600 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="searchResults.patients.length > 0">
                <h4 class="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-3">Patients Found</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div v-for="pat in searchResults.patients" :key="pat.id" 
                       class="flex justify-between items-center p-4 bg-slate-50 rounded-xl border border-slate-100 hover:border-emerald-200 transition-colors">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold">
                        {{ pat.name.charAt(0) }}
                      </div>
                      <div>
                        <p class="font-bold text-slate-800">{{ pat.name }}</p>
                        <p class="text-xs text-slate-500">{{ pat.email }}</p>
                      </div>
                    </div>
                    <div class="flex gap-2">
                      <button @click="editPatient(pat)" class="p-2 text-slate-400 hover:text-emerald-600 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button @click="deletePatient(pat.id)" class="p-2 text-slate-400 hover:text-red-600 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions Grid -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center text-center hover:shadow-md transition-shadow">
              <div class="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-4 text-blue-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 class="text-lg font-bold text-slate-800 mb-2">Manage Doctors</h3>
              <p class="text-sm text-slate-500 mb-6">View profiles, assign departments, and manage schedules.</p>
              <router-link to="/admin/doctors" class="btn btn-outline w-full rounded-xl">View All Doctors</router-link>
            </div>

            <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center text-center hover:shadow-md transition-shadow">
              <div class="w-16 h-16 bg-emerald-50 rounded-full flex items-center justify-center mb-4 text-emerald-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <h3 class="text-lg font-bold text-slate-800 mb-2">Manage Patients</h3>
              <p class="text-sm text-slate-500 mb-6">Access medical records, history, and patient details.</p>
              <router-link to="/admin/patients" class="btn btn-outline w-full rounded-xl">View All Patients</router-link>
            </div>

            <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col items-center text-center hover:shadow-md transition-shadow">
              <div class="w-16 h-16 bg-violet-50 rounded-full flex items-center justify-center mb-4 text-violet-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 class="text-lg font-bold text-slate-800 mb-2">Appointments</h3>
              <p class="text-sm text-slate-500 mb-6">Monitor scheduled visits and appointment history.</p>
              <router-link to="/admin/appointments" class="btn btn-outline w-full rounded-xl">View All Appointments</router-link>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Department Modal -->
    <div v-if="showDepartmentModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[85vh] flex flex-col overflow-hidden">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h3 class="text-xl font-bold text-slate-800">Manage Departments</h3>
          <button @click="showDepartmentModal = false" class="text-slate-400 hover:text-slate-600 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto custom-scrollbar">
          <!-- Add Department Form -->
          <form @submit.prevent="addDepartment" class="mb-8 p-5 bg-slate-50 rounded-xl border border-slate-100">
            <h4 class="text-sm font-bold text-slate-700 mb-3 uppercase tracking-wide">Add New Department</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input v-model="newDept.name" placeholder="Department Name" class="input bg-white" required />
              <input v-model="newDept.overview" placeholder="Overview (Optional)" class="input bg-white" />
            </div>
            <button type="submit" class="btn btn-primary w-full mt-4 rounded-xl">Add Department</button>
          </form>

          <!-- Departments List -->
          <div class="space-y-3">
            <h4 class="text-sm font-bold text-slate-700 uppercase tracking-wide mb-2">Existing Departments</h4>
            <div v-for="dept in departments" :key="dept.id" 
                 class="group border border-slate-100 rounded-xl p-4 hover:shadow-md transition-all bg-white">
              <div class="flex justify-between items-start mb-3">
                <div>
                  <p class="font-bold text-lg text-slate-800">{{ dept.name }}</p>
                  <p class="text-xs font-medium text-slate-500 bg-slate-100 inline-block px-2 py-1 rounded-full mt-1">
                    {{ dept.doctor_count }} Doctors Assigned
                  </p>
                </div>
                <button @click="deleteDepartment(dept.id)" 
                        class="text-slate-400 hover:text-red-500 transition-colors p-2 hover:bg-red-50 rounded-lg"
                        :disabled="dept.doctor_count > 0"
                        title="Delete Department">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
              
              <!-- Doctors List -->
              <div v-if="dept.doctors && dept.doctors.length > 0" class="pl-4 border-l-2 border-primary-100">
                <ul class="space-y-2 mt-2">
                  <li v-for="doc in dept.doctors" :key="doc.id" class="text-sm text-slate-600 flex items-center gap-2">
                    <div class="w-6 h-6 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center text-xs font-bold">
                      {{ doc.user?.name?.charAt(0) }}
                    </div>
                    {{ doc.user?.name || 'Unknown Doctor' }}
                  </li>
                </ul>
              </div>
              <div v-else class="text-sm text-slate-400 italic pl-4 border-l-2 border-slate-100 mt-2">
                No doctors currently assigned
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Doctor Modal -->
    <div v-if="showDoctorModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
          <h3 class="text-xl font-bold text-slate-800">Add New Doctor</h3>
          <button @click="showDoctorModal = false" class="text-slate-400 hover:text-slate-600 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto custom-scrollbar">
          <form @submit.prevent="createDoctor" class="space-y-5">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div class="form-group">
                <label class="label">Full Name</label>
                <input v-model="newDoctor.name" class="input" placeholder="Dr. John Doe" required />
              </div>
              <div class="form-group">
                <label class="label">Email Address</label>
                <input type="email" v-model="newDoctor.email" class="input" placeholder="doctor@hospital.com" required />
              </div>
              <div class="form-group">
                <label class="label">Password</label>
                <input type="password" v-model="newDoctor.password" class="input" placeholder="••••••••" required />
              </div>
              <div class="form-group">
                <label class="label">Contact Number</label>
                <input v-model="newDoctor.contact_number" class="input" placeholder="+1 234 567 890" required />
              </div>
              <div class="form-group md:col-span-2">
                <label class="label">Department</label>
                <select v-model="newDoctor.department_id" class="input" required>
                  <option value="">Select Department</option>
                  <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                    {{ dept.name }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label class="label">Specialization</label>
                <input v-model="newDoctor.specialization" class="input" placeholder="e.g. Cardiology" required />
              </div>
              <div class="form-group">
                <label class="label">Experience (Years)</label>
                <input type="number" v-model="newDoctor.experience" class="input" placeholder="e.g. 10" required />
              </div>
              <div class="form-group md:col-span-2">
                <label class="label">Qualifications</label>
                <input v-model="newDoctor.qualifications" class="input" placeholder="e.g. MBBS, MD, PhD" required />
              </div>
            </div>
            
            <div class="flex gap-4 pt-4 border-t border-slate-100 mt-4">
              <button type="button" @click="showDoctorModal = false" class="btn btn-outline flex-1 rounded-xl">Cancel</button>
              <button type="submit" class="btn btn-primary flex-1 rounded-xl shadow-lg shadow-primary-500/20">Create Doctor Account</button>
            </div>
          </form>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import Sidebar from '@/components/Sidebar.vue';
import SearchBar from '@/components/SearchBar.vue';
import api from '@/services/api';

const router = useRouter();

const stats = ref({
  total_doctors: 0,
  total_patients: 0,
  total_appointments: 0,
  upcoming_appointments: 0
});

const searchQuery = ref('');
const searchType = ref('all');
const searchResults = ref(null);

const showDepartmentModal = ref(false);
const showDoctorModal = ref(false);
const departments = ref([]);
const newDept = ref({ name: '', overview: '' });

const newDoctor = reactive({
  name: '',
  email: '',
  password: '',
  contact_number: '',
  department_id: '',
  specialization: '',
  qualifications: '',
  experience: ''
});

const fetchStats = async () => {
  try {
    const response = await api.get('/admin/dashboard');
    stats.value = response.data;
  } catch (err) {
    console.error('Failed to fetch stats', err);
  }
};

const performSearch = async () => {
  if (!searchQuery.value.trim()) return;
  
  try {
    const response = await api.get('/admin/search', {
      params: { q: searchQuery.value, type: searchType.value }
    });
    searchResults.value = response.data;
  } catch (err) {
    console.error('Search failed', err);
  }
};

const fetchDepartments = async () => {
  try {
    const response = await api.get('/departments/');
    departments.value = response.data;
  } catch (err) {
    console.error(err);
  }
};

const addDepartment = async () => {
  try {
    await api.post('/departments/', newDept.value);
    newDept.value = { name: '', overview: '' };
    fetchDepartments();
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to add department');
  }
};

const createDoctor = async () => {
  try {
    await api.post('/admin/doctors', newDoctor);
    alert('Doctor created successfully');
    showDoctorModal.value = false;
    // Reset form
    Object.keys(newDoctor).forEach(key => newDoctor[key] = '');
    fetchStats();
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to create doctor');
  }
};

const deleteDepartment = async (id) => {
  if (!confirm('Delete this department?')) return;
  try {
    await api.delete(`/departments/${id}`);
    fetchDepartments();
  } catch (err) {
    alert(err.response?.data?.message || 'Cannot delete department');
  }
};

const deleteDoctor = async (id) => {
  if (!confirm('Delete this doctor?')) return;
  try {
    await api.delete(`/admin/doctors/${id}`);
    performSearch();
    fetchStats();
  } catch (err) {
    alert('Failed to delete doctor');
  }
};

const deletePatient = async (id) => {
  if (!confirm('Delete this patient?')) return;
  try {
    await api.delete(`/admin/patients/${id}`);
    performSearch();
    fetchStats();
  } catch (err) {
    alert('Failed to delete patient');
  }
};

// Navigate to specific lists
const showDoctorsList = () => {
  router.push('/admin/doctors');
};

const showPatientsList = () => {
  router.push('/admin/patients');
};

const showAllAppointments = () => {
  router.push('/admin/appointments');
};

const showUpcomingAppointments = () => {
  router.push('/admin/appointments?filter=upcoming');
};

onMounted(() => {
  fetchStats();
  fetchDepartments();
});
</script>
