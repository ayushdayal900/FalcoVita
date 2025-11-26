<template>
  <div class="dashboard-layout flex h-screen overflow-hidden bg-slate-50 font-sans selection:bg-primary-500 selection:text-white">
    <Sidebar />
    
    <main class="flex-1 flex flex-col overflow-hidden relative">
      <!-- Top Header -->
      <header class="h-24 bg-white/80 backdrop-blur-xl border-b border-slate-200/60 flex items-center justify-between px-10 sticky top-0 z-20 transition-all duration-300">
        <div>
          <h2 class="text-3xl font-bold text-slate-800 tracking-tight">Admin Dashboard</h2>
          <p class="text-slate-500 font-medium mt-1">Overview of hospital operations</p>
        </div>
        <div class="flex gap-4">
          <button @click="showDoctorModal = true" class="btn bg-primary-600 hover:bg-primary-700 text-white shadow-lg shadow-primary-500/30 flex items-center gap-2.5 px-6 py-3 rounded-2xl transition-all hover:-translate-y-0.5 hover:shadow-primary-500/40 font-semibold tracking-wide">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
            </svg>
            Add Doctor
          </button>
          <button @click="showDepartmentModal = true" class="btn bg-white border border-slate-200 hover:bg-slate-50 hover:border-slate-300 text-slate-700 flex items-center gap-2.5 px-6 py-3 rounded-2xl transition-all shadow-sm hover:shadow-md font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            Departments
          </button>
        </div>
      </header>

      <div class="flex-1 overflow-y-auto p-10 custom-scrollbar scroll-smooth">
        <div class="max-w-[1600px] mx-auto space-y-10">
          
          <!-- Statistics Cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <!-- Total Doctors -->
            <div class="relative overflow-hidden rounded-3xl p-8 bg-gradient-to-br from-blue-600 to-blue-700 text-white shadow-2xl shadow-blue-500/30 cursor-pointer hover:-translate-y-1 transition-all duration-500 border border-white/10 group" @click="showDoctorsList">
              <div class="absolute top-0 right-0 -mt-8 -mr-8 w-48 h-48 bg-white/10 rounded-full blur-3xl group-hover:bg-white/20 transition-all duration-700"></div>
              <div class="absolute bottom-0 left-0 -mb-8 -ml-8 w-32 h-32 bg-blue-500/30 rounded-full blur-2xl"></div>
              
              <div class="relative z-10">
                <div class="flex justify-between items-start mb-8">
                  <div class="p-3.5 bg-white/15 rounded-2xl backdrop-blur-md border border-white/10 shadow-inner">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                  <span class="text-xs font-bold bg-white/20 px-3 py-1.5 rounded-full border border-white/10 backdrop-blur-sm shadow-sm">Active</span>
                </div>
                <div>
                  <h3 class="text-5xl font-bold mb-2 tracking-tight group-hover:scale-105 transition-transform origin-left">{{ stats.total_doctors }}</h3>
                  <p class="text-blue-100 text-base font-medium opacity-90">Total Doctors</p>
                </div>
              </div>
            </div>

            <!-- Total Patients -->
            <div class="relative overflow-hidden rounded-3xl p-8 bg-gradient-to-br from-emerald-500 to-emerald-600 text-white shadow-2xl shadow-emerald-500/30 cursor-pointer hover:-translate-y-1 transition-all duration-500 border border-white/10 group" @click="showPatientsList">
              <div class="absolute top-0 right-0 -mt-8 -mr-8 w-48 h-48 bg-white/10 rounded-full blur-3xl group-hover:bg-white/20 transition-all duration-700"></div>
              <div class="absolute bottom-0 left-0 -mb-8 -ml-8 w-32 h-32 bg-emerald-400/30 rounded-full blur-2xl"></div>

              <div class="relative z-10">
                <div class="flex justify-between items-start mb-8">
                  <div class="p-3.5 bg-white/15 rounded-2xl backdrop-blur-md border border-white/10 shadow-inner">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </div>
                  <span class="text-xs font-bold bg-white/20 px-3 py-1.5 rounded-full border border-white/10 backdrop-blur-sm shadow-sm">+12%</span>
                </div>
                <div>
                  <h3 class="text-5xl font-bold mb-2 tracking-tight group-hover:scale-105 transition-transform origin-left">{{ stats.total_patients }}</h3>
                  <p class="text-emerald-100 text-base font-medium opacity-90">Total Patients</p>
                </div>
              </div>
            </div>

            <!-- Total Appointments -->
            <div class="relative overflow-hidden rounded-3xl p-8 bg-gradient-to-br from-violet-600 to-violet-700 text-white shadow-2xl shadow-violet-500/30 cursor-pointer hover:-translate-y-1 transition-all duration-500 border border-white/10 group" @click="showAllAppointments">
              <div class="absolute top-0 right-0 -mt-8 -mr-8 w-48 h-48 bg-white/10 rounded-full blur-3xl group-hover:bg-white/20 transition-all duration-700"></div>
              <div class="absolute bottom-0 left-0 -mb-8 -ml-8 w-32 h-32 bg-violet-500/30 rounded-full blur-2xl"></div>

              <div class="relative z-10">
                <div class="flex justify-between items-start mb-8">
                  <div class="p-3.5 bg-white/15 rounded-2xl backdrop-blur-md border border-white/10 shadow-inner">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                </div>
                <div>
                  <h3 class="text-5xl font-bold mb-2 tracking-tight group-hover:scale-105 transition-transform origin-left">{{ stats.total_appointments }}</h3>
                  <p class="text-violet-100 text-base font-medium opacity-90">Total Appointments</p>
                </div>
              </div>
            </div>

            <!-- Upcoming -->
            <div class="relative overflow-hidden rounded-3xl p-8 bg-gradient-to-br from-orange-500 to-orange-600 text-white shadow-2xl shadow-orange-500/30 cursor-pointer hover:-translate-y-1 transition-all duration-500 border border-white/10 group" @click="showUpcomingAppointments">
              <div class="absolute top-0 right-0 -mt-8 -mr-8 w-48 h-48 bg-white/10 rounded-full blur-3xl group-hover:bg-white/20 transition-all duration-700"></div>
              <div class="absolute bottom-0 left-0 -mb-8 -ml-8 w-32 h-32 bg-orange-400/30 rounded-full blur-2xl"></div>

              <div class="relative z-10">
                <div class="flex justify-between items-start mb-8">
                  <div class="p-3.5 bg-white/15 rounded-2xl backdrop-blur-md border border-white/10 shadow-inner">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <span class="text-xs font-bold bg-white/20 px-3 py-1.5 rounded-full border border-white/10 backdrop-blur-sm shadow-sm">Next 24h</span>
                </div>
                <div>
                  <h3 class="text-5xl font-bold mb-2 tracking-tight group-hover:scale-105 transition-transform origin-left">{{ stats.upcoming_appointments }}</h3>
                  <p class="text-orange-100 text-base font-medium opacity-90">Upcoming</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Search Section -->
          <div class="bg-white/80 backdrop-blur-lg rounded-3xl p-8 shadow-lg shadow-slate-200/50 border border-white/50">
            <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              Quick Search
            </h3>
            <SearchBar 
              v-model="searchQuery" 
              v-model:searchType="searchType"
              placeholder="Search by name, email or ID..."
              :showTypeSelector="true"
              :types="['doctor', 'patient']"
              @search="performSearch"
              @clear="searchQuery = ''; searchResults = null"
              class="w-full"
            />

            <!-- Search Results -->
            <div v-if="searchResults" class="mt-8 space-y-8 animate-fade-in">
              <div v-if="searchResults.doctors.length > 0">
                <h4 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4 ml-1">Doctors Found</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                  <div v-for="doc in searchResults.doctors" :key="doc.id" 
                       class="flex justify-between items-center p-5 bg-white rounded-2xl border border-slate-100 hover:border-primary-200 hover:shadow-lg hover:shadow-primary-500/5 transition-all duration-300 group">
                    <div class="flex items-center gap-4">
                      <div class="w-12 h-12 rounded-2xl bg-primary-50 text-primary-600 flex items-center justify-center font-bold text-lg group-hover:bg-primary-600 group-hover:text-white transition-colors duration-300 shadow-sm">
                        {{ doc.name.charAt(0) }}
                      </div>
                      <div>
                        <p class="font-bold text-slate-800 group-hover:text-primary-700 transition-colors">{{ doc.name }}</p>
                        <p class="text-xs text-slate-500 font-medium">{{ doc.email }}</p>
                      </div>
                    </div>
                    <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button @click="editDoctor(doc)" class="p-2.5 text-slate-400 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all" title="Edit">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button @click="deleteDoctor(doc.id)" class="p-2.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all" title="Delete">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="searchResults.patients.length > 0">
                <h4 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4 ml-1">Patients Found</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                  <div v-for="pat in searchResults.patients" :key="pat.id" 
                       class="flex justify-between items-center p-5 bg-white rounded-2xl border border-slate-100 hover:border-emerald-200 hover:shadow-lg hover:shadow-emerald-500/5 transition-all duration-300 group">
                    <div class="flex items-center gap-4">
                      <div class="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold text-lg group-hover:bg-emerald-600 group-hover:text-white transition-colors duration-300 shadow-sm">
                        {{ pat.name.charAt(0) }}
                      </div>
                      <div>
                        <p class="font-bold text-slate-800 group-hover:text-emerald-700 transition-colors">{{ pat.name }}</p>
                        <p class="text-xs text-slate-500 font-medium">{{ pat.email }}</p>
                      </div>
                    </div>
                    <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button @click="editPatient(pat)" class="p-2.5 text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-xl transition-all" title="Edit">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                      </button>
                      <button @click="deletePatient(pat.id)" class="p-2.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-all" title="Delete">
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
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="bg-white p-10 rounded-3xl shadow-lg shadow-slate-200/50 border border-slate-100/50 flex flex-col items-center text-center hover:shadow-2xl hover:shadow-blue-500/10 hover:-translate-y-2 transition-all duration-500 group cursor-pointer relative overflow-hidden" @click="showDoctorsList">
              <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-blue-400 to-blue-600 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></div>
              <div class="w-24 h-24 bg-blue-50 rounded-[2rem] flex items-center justify-center mb-8 text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-all duration-500 shadow-lg shadow-blue-500/20 group-hover:scale-110 group-hover:rotate-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-slate-800 mb-3 group-hover:text-blue-600 transition-colors">Manage Doctors</h3>
              <p class="text-slate-500 mb-10 leading-relaxed max-w-xs mx-auto">View profiles, assign departments, and manage schedules efficiently.</p>
              <button class="w-full py-4 px-6 bg-slate-50 text-slate-600 font-bold rounded-2xl hover:bg-blue-600 hover:text-white transition-all duration-300 flex items-center justify-center gap-3 group-hover:shadow-lg group-hover:shadow-blue-500/25 mt-auto">
                View All Doctors
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </button>
            </div>

            <div class="bg-white p-10 rounded-3xl shadow-lg shadow-slate-200/50 border border-slate-100/50 flex flex-col items-center text-center hover:shadow-2xl hover:shadow-emerald-500/10 hover:-translate-y-2 transition-all duration-500 group cursor-pointer relative overflow-hidden" @click="showPatientsList">
              <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-emerald-400 to-emerald-600 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></div>
              <div class="w-24 h-24 bg-emerald-50 rounded-[2rem] flex items-center justify-center mb-8 text-emerald-600 group-hover:bg-emerald-600 group-hover:text-white transition-all duration-500 shadow-lg shadow-emerald-500/20 group-hover:scale-110 group-hover:rotate-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-slate-800 mb-3 group-hover:text-emerald-600 transition-colors">Manage Patients</h3>
              <p class="text-slate-500 mb-10 leading-relaxed max-w-xs mx-auto">Access medical records, history, and patient details securely.</p>
              <button class="w-full py-4 px-6 bg-slate-50 text-slate-600 font-bold rounded-2xl hover:bg-emerald-600 hover:text-white transition-all duration-300 flex items-center justify-center gap-3 group-hover:shadow-lg group-hover:shadow-emerald-500/25 mt-auto">
                View All Patients
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </button>
            </div>

            <div class="bg-white p-10 rounded-3xl shadow-lg shadow-slate-200/50 border border-slate-100/50 flex flex-col items-center text-center hover:shadow-2xl hover:shadow-violet-500/10 hover:-translate-y-2 transition-all duration-500 group cursor-pointer relative overflow-hidden" @click="showAllAppointments">
              <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-violet-400 to-violet-600 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></div>
              <div class="w-24 h-24 bg-violet-50 rounded-[2rem] flex items-center justify-center mb-8 text-violet-600 group-hover:bg-violet-600 group-hover:text-white transition-all duration-500 shadow-lg shadow-violet-500/20 group-hover:scale-110 group-hover:rotate-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-slate-800 mb-3 group-hover:text-violet-600 transition-colors">Appointments</h3>
              <p class="text-slate-500 mb-10 leading-relaxed max-w-xs mx-auto">Monitor scheduled visits and appointment history in real-time.</p>
              <button class="w-full py-4 px-6 bg-slate-50 text-slate-600 font-bold rounded-2xl hover:bg-violet-600 hover:text-white transition-all duration-300 flex items-center justify-center gap-3 group-hover:shadow-lg group-hover:shadow-violet-500/25 mt-auto">
                View All Appointments
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </button>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Department Modal -->
    <div v-if="showDepartmentModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-md animate-fade-in">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-2xl max-h-[85vh] flex flex-col overflow-hidden transform transition-all scale-100">
        <div class="p-8 border-b border-slate-100 flex justify-between items-center bg-slate-50/80 backdrop-blur-sm">
          <div>
            <h3 class="text-2xl font-bold text-slate-800">Manage Departments</h3>
            <p class="text-slate-500 text-sm mt-1">Add or remove hospital departments</p>
          </div>
          <button @click="showDepartmentModal = false" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-400 hover:text-slate-600 hover:bg-slate-50 transition-all shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-8 overflow-y-auto custom-scrollbar">
          <!-- Add Department Form -->
          <form @submit.prevent="addDepartment" class="mb-10 p-6 bg-slate-50 rounded-2xl border border-slate-100 shadow-sm">
            <h4 class="text-sm font-bold text-slate-700 mb-4 uppercase tracking-wide flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Add New Department
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <input v-model="newDept.name" placeholder="Department Name" class="input bg-white h-12" required />
              <input v-model="newDept.overview" placeholder="Overview (Optional)" class="input bg-white h-12" />
            </div>
            <button type="submit" class="btn btn-primary w-full mt-5 rounded-xl h-12 font-bold shadow-lg shadow-primary-500/20">Add Department</button>
          </form>

          <!-- Departments List -->
          <div class="space-y-4">
            <h4 class="text-sm font-bold text-slate-700 uppercase tracking-wide mb-3 ml-1">Existing Departments</h4>
            <div v-for="dept in departments" :key="dept.id" 
                 class="group border border-slate-100 rounded-2xl p-5 hover:shadow-lg hover:border-primary-100 transition-all bg-white duration-300">
              <div class="flex justify-between items-start mb-4">
                <div>
                  <p class="font-bold text-lg text-slate-800 group-hover:text-primary-700 transition-colors">{{ dept.name }}</p>
                  <p class="text-xs font-bold text-slate-500 bg-slate-100 inline-block px-3 py-1 rounded-full mt-2 group-hover:bg-primary-50 group-hover:text-primary-600 transition-colors">
                    {{ dept.doctor_count }} Doctors Assigned
                  </p>
                </div>
                <button @click="deleteDepartment(dept.id)" 
                        class="text-slate-400 hover:text-red-500 transition-colors p-2.5 hover:bg-red-50 rounded-xl"
                        :disabled="dept.doctor_count > 0"
                        title="Delete Department">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
              
              <!-- Doctors List -->
              <div v-if="dept.doctors && dept.doctors.length > 0" class="pl-5 border-l-2 border-primary-100 group-hover:border-primary-300 transition-colors">
                <ul class="space-y-3 mt-3">
                  <li v-for="doc in dept.doctors" :key="doc.id" class="text-sm text-slate-600 flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center text-xs font-bold shadow-sm">
                      {{ doc.user?.name?.charAt(0) }}
                    </div>
                    <span class="font-medium">{{ doc.user?.name || 'Unknown Doctor' }}</span>
                  </li>
                </ul>
              </div>
              <div v-else class="text-sm text-slate-400 italic pl-5 border-l-2 border-slate-100 mt-3">
                No doctors currently assigned
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Doctor Modal -->
    <div v-if="showDoctorModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-md animate-fade-in">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden">
        <div class="p-8 border-b border-slate-100 flex justify-between items-center bg-slate-50/80 backdrop-blur-sm">
          <div>
            <h3 class="text-2xl font-bold text-slate-800">Add New Doctor</h3>
            <p class="text-slate-500 text-sm mt-1">Create a new doctor account</p>
          </div>
          <button @click="showDoctorModal = false" class="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-400 hover:text-slate-600 hover:bg-slate-50 transition-all shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-8 overflow-y-auto custom-scrollbar">
          <form @submit.prevent="createDoctor" class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="form-group">
                <label class="label font-bold text-slate-700 mb-2">Full Name</label>
                <input v-model="newDoctor.name" class="input h-12 bg-slate-50 focus:bg-white transition-colors" placeholder="Dr. John Doe" required />
              </div>
              <div class="form-group">
                <label class="label font-bold text-slate-700 mb-2">Email Address</label>
                <input type="email" v-model="newDoctor.email" class="input h-12 bg-slate-50 focus:bg-white transition-colors" placeholder="doctor@hospital.com" required />
              </div>
              <div class="form-group">
                <label class="label font-bold text-slate-700 mb-2">Password</label>
                <input type="password" v-model="newDoctor.password" class="input h-12 bg-slate-50 focus:bg-white transition-colors" placeholder="••••••••" required />
              </div>
              <div class="form-group">
                <label class="label font-bold text-slate-700 mb-2">Contact Number</label>
                <input v-model="newDoctor.contact_number" class="input h-12 bg-slate-50 focus:bg-white transition-colors" placeholder="+1 234 567 890" required />
              </div>
              <div class="form-group md:col-span-2">
                <label class="label font-bold text-slate-700 mb-2">Department</label>
                <div class="relative">
                  <select v-model="newDoctor.department_id" class="input h-12 bg-slate-50 focus:bg-white transition-colors appearance-none" required>
                    <option value="">Select Department</option>
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                      {{ dept.name }}
                    </option>
                  </select>
                  <div class="absolute inset-y-0 right-0 flex items-center px-4 pointer-events-none text-slate-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>
              <div class="form-group">
                <label class="label font-bold text-slate-700 mb-2">Specialization</label>
                <input v-model="newDoctor.specialization" class="input h-12 bg-slate-50 focus:bg-white transition-colors" placeholder="e.g. Cardiology" required />
              </div>
              <div class="form-group">
                <label class="label font-bold text-slate-700 mb-2">Experience (Years)</label>
                <input type="number" v-model="newDoctor.experience" class="input h-12 bg-slate-50 focus:bg-white transition-colors" placeholder="e.g. 10" required />
              </div>
              <div class="form-group md:col-span-2">
                <label class="label font-bold text-slate-700 mb-2">Qualifications</label>
                <input v-model="newDoctor.qualifications" class="input h-12 bg-slate-50 focus:bg-white transition-colors" placeholder="e.g. MBBS, MD, PhD" required />
              </div>
            </div>
            
            <div class="flex gap-4 pt-6 border-t border-slate-100 mt-6">
              <button type="button" @click="showDoctorModal = false" class="btn btn-outline flex-1 rounded-xl h-12 font-semibold border-slate-300 hover:bg-slate-50 hover:text-slate-800">Cancel</button>
              <button type="submit" class="btn btn-primary flex-1 rounded-xl h-12 font-bold shadow-lg shadow-primary-500/20 hover:shadow-primary-500/30">Create Doctor Account</button>
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
