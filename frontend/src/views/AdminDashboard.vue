<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />
    
    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <!-- Top Header -->
      <header class="bg-white border-bottom py-3 px-4 d-flex align-items-center justify-content-between sticky-top z-2">
        <div>
          <h2 class="h4 fw-bold text-dark mb-0">Admin Dashboard</h2>
          <p class="text-muted small mb-0">Overview of hospital operations</p>
        </div>
        <div class="d-flex gap-2">
          <button @click="showDoctorModal = true" class="btn btn-primary d-flex align-items-center gap-2 shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Add Doctor
          </button>
          <button @click="showDepartmentModal = true" class="btn btn-outline-secondary d-flex align-items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            Departments
          </button>
        </div>
      </header>

      <div class="flex-grow-1 overflow-auto p-4 custom-scrollbar">
        <div class="container-fluid p-0" style="max-width: 1600px;">
          
          <!-- Statistics Cards -->
          <div class="row g-4 mb-4">
            <!-- Total Doctors -->
            <div class="col-md-6 col-lg-3">
              <div class="card bg-primary text-white border-0 shadow h-100 overflow-hidden cursor-pointer hover-lift" @click="showDoctorsList">
                <div class="card-body position-relative p-4">
                  <div class="position-absolute top-0 end-0 opacity-10 translate-middle-y me-n3 mt-n3">
                     <svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
                     </svg>
                  </div>
                  <div class="d-flex justify-content-between align-items-start mb-4 position-relative z-1">
                    <div class="bg-white bg-opacity-25 rounded p-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                    </div>
                    <span class="badge bg-white bg-opacity-25 text-white border border-white border-opacity-25">Active</span>
                  </div>
                  <div class="position-relative z-1">
                    <h3 class="display-5 fw-bold mb-1">{{ stats.total_doctors }}</h3>
                    <p class="text-white-50 mb-0 fw-medium">Total Doctors</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Total Patients -->
            <div class="col-md-6 col-lg-3">
              <div class="card bg-success text-white border-0 shadow h-100 overflow-hidden cursor-pointer hover-lift" @click="showPatientsList">
                <div class="card-body position-relative p-4">
                   <div class="position-absolute top-0 end-0 opacity-10 translate-middle-y me-n3 mt-n3">
                     <svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M7 14s-1 0-1-1 1-4 5-4 5 3 5 4 0 1 1 1H1zm4 0c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
                     </svg>
                  </div>
                  <div class="d-flex justify-content-between align-items-start mb-4 position-relative z-1">
                    <div class="bg-white bg-opacity-25 rounded p-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                    </div>
                    <span class="badge bg-white bg-opacity-25 text-white border border-white border-opacity-25">+12%</span>
                  </div>
                  <div class="position-relative z-1">
                    <h3 class="display-5 fw-bold mb-1">{{ stats.total_patients }}</h3>
                    <p class="text-white-50 mb-0 fw-medium">Total Patients</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Total Appointments -->
            <div class="col-md-6 col-lg-3">
              <div class="card bg-info text-white border-0 shadow h-100 overflow-hidden cursor-pointer hover-lift" @click="showAllAppointments">
                <div class="card-body position-relative p-4">
                   <div class="position-absolute top-0 end-0 opacity-10 translate-middle-y me-n3 mt-n3">
                     <svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
                     </svg>
                  </div>
                  <div class="d-flex justify-content-between align-items-start mb-4 position-relative z-1">
                    <div class="bg-white bg-opacity-25 rounded p-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                  </div>
                  <div class="position-relative z-1">
                    <h3 class="display-5 fw-bold mb-1">{{ stats.total_appointments }}</h3>
                    <p class="text-white-50 mb-0 fw-medium">Total Appointments</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Upcoming -->
            <div class="col-md-6 col-lg-3">
              <div class="card bg-warning text-white border-0 shadow h-100 overflow-hidden cursor-pointer hover-lift" @click="showUpcomingAppointments">
                <div class="card-body position-relative p-4">
                   <div class="position-absolute top-0 end-0 opacity-10 translate-middle-y me-n3 mt-n3">
                     <svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
                        <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
                     </svg>
                  </div>
                  <div class="d-flex justify-content-between align-items-start mb-4 position-relative z-1">
                    <div class="bg-white bg-opacity-25 rounded p-2">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <span class="badge bg-white bg-opacity-25 text-white border border-white border-opacity-25">Next 24h</span>
                  </div>
                  <div class="position-relative z-1">
                    <h3 class="display-5 fw-bold mb-1">{{ stats.upcoming_appointments }}</h3>
                    <p class="text-white-50 mb-0 fw-medium">Upcoming</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Search Section -->
          <div class="card border-0 shadow-sm rounded-4 mb-4">
            <div class="card-body p-4">
              <h3 class="h5 fw-bold text-dark mb-4 d-flex align-items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-primary">
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
                class="w-100"
              />

              <!-- Search Results -->
              <div v-if="searchResults" class="mt-4 animate-fade-in">
                <div v-if="searchResults.doctors.length > 0" class="mb-4">
                  <h4 class="h6 fw-bold text-muted text-uppercase mb-3">Doctors Found</h4>
                  <div class="row g-3">
                    <div v-for="doc in searchResults.doctors" :key="doc.id" class="col-md-6 col-lg-4">
                      <div class="card h-100 border-0 shadow-sm hover-shadow transition-all">
                        <div class="card-body d-flex align-items-center justify-content-between">
                          <div class="d-flex align-items-center gap-3">
                            <div class="rounded-circle bg-primary bg-opacity-10 text-primary d-flex align-items-center justify-content-center fw-bold fs-5" style="width: 48px; height: 48px;">
                              {{ doc.name.charAt(0) }}
                            </div>
                            <div>
                              <p class="fw-bold mb-0 text-dark">{{ doc.name }}</p>
                              <p class="small text-muted mb-0">{{ doc.email }}</p>
                            </div>
                          </div>
                          <div class="d-flex gap-1">
                            <button @click="editDoctor(doc)" class="btn btn-sm btn-light text-primary" title="Edit">
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                              </svg>
                            </button>
                            <button @click="deleteDoctor(doc.id)" class="btn btn-sm btn-light text-danger" title="Delete">
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div v-if="searchResults.patients.length > 0">
                  <h4 class="h6 fw-bold text-muted text-uppercase mb-3">Patients Found</h4>
                  <div class="row g-3">
                    <div v-for="pat in searchResults.patients" :key="pat.id" class="col-md-6 col-lg-4">
                      <div class="card h-100 border-0 shadow-sm hover-shadow transition-all">
                        <div class="card-body d-flex align-items-center justify-content-between">
                          <div class="d-flex align-items-center gap-3">
                            <div class="rounded-circle bg-success bg-opacity-10 text-success d-flex align-items-center justify-content-center fw-bold fs-5" style="width: 48px; height: 48px;">
                              {{ pat.name.charAt(0) }}
                            </div>
                            <div>
                              <p class="fw-bold mb-0 text-dark">{{ pat.name }}</p>
                              <p class="small text-muted mb-0">{{ pat.email }}</p>
                            </div>
                          </div>
                          <div class="d-flex gap-1">
                            <button @click="editPatient(pat)" class="btn btn-sm btn-light text-success" title="Edit">
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                              </svg>
                            </button>
                            <button @click="deletePatient(pat.id)" class="btn btn-sm btn-light text-danger" title="Delete">
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions Grid -->
          <div class="row g-4">
            <div class="col-md-4">
              <div class="card border-0 shadow-sm h-100 hover-lift cursor-pointer" @click="showDoctorsList">
                <div class="card-body p-4 text-center d-flex flex-column align-items-center">
                  <div class="rounded-circle bg-primary bg-opacity-10 text-primary d-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                  </div>
                  <h4 class="fw-bold text-dark">Manage Doctors</h4>
                  <p class="text-muted small mb-4">View profiles, assign departments, and manage schedules efficiently.</p>
                  <button class="btn btn-outline-primary w-100 mt-auto rounded-pill fw-bold">View All Doctors</button>
                </div>
              </div>
            </div>

            <div class="col-md-4">
              <div class="card border-0 shadow-sm h-100 hover-lift cursor-pointer" @click="showPatientsList">
                <div class="card-body p-4 text-center d-flex flex-column align-items-center">
                  <div class="rounded-circle bg-success bg-opacity-10 text-success d-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                  </div>
                  <h4 class="fw-bold text-dark">Manage Patients</h4>
                  <p class="text-muted small mb-4">Access medical records, history, and patient details securely.</p>
                  <button class="btn btn-outline-success w-100 mt-auto rounded-pill fw-bold">View All Patients</button>
                </div>
              </div>
            </div>

            <div class="col-md-4">
              <div class="card border-0 shadow-sm h-100 hover-lift cursor-pointer" @click="showAllAppointments">
                <div class="card-body p-4 text-center d-flex flex-column align-items-center">
                  <div class="rounded-circle bg-info bg-opacity-10 text-info d-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <h4 class="fw-bold text-dark">Appointments</h4>
                  <p class="text-muted small mb-4">Monitor scheduled visits and appointment history in real-time.</p>
                  <button class="btn btn-outline-info w-100 mt-auto rounded-pill fw-bold">View All Appointments</button>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Department Modal -->
    <div v-if="showDepartmentModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-bottom-0 pb-0">
            <h5 class="modal-title fw-bold">Manage Departments</h5>
            <button type="button" class="btn-close" @click="showDepartmentModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <!-- Add Department Form -->
            <form @submit.prevent="addDepartment" class="mb-4 p-3 bg-light rounded-3 border">
              <h6 class="fw-bold text-primary mb-3 text-uppercase small">Add New Department</h6>
              <div class="row g-3">
                <div class="col-md-6">
                  <input v-model="newDept.name" placeholder="Department Name" class="form-control" required />
                </div>
                <div class="col-md-6">
                  <input v-model="newDept.overview" placeholder="Overview (Optional)" class="form-control" />
                </div>
                <div class="col-12">
                  <button type="submit" class="btn btn-primary w-100">Add Department</button>
                </div>
              </div>
            </form>

            <!-- Departments List -->
            <div>
              <h6 class="fw-bold text-muted text-uppercase small mb-3">Existing Departments</h6>
              <div class="list-group">
                <div v-for="dept in departments" :key="dept.id" class="list-group-item list-group-item-action border-0 mb-2 rounded shadow-sm">
                  <div class="d-flex w-100 justify-content-between align-items-center">
                    <div>
                      <h6 class="mb-1 fw-bold text-dark">{{ dept.name }}</h6>
                      <small class="text-muted">{{ dept.doctor_count }} Doctors Assigned</small>
                    </div>
                    <button @click="deleteDepartment(dept.id)" class="btn btn-sm btn-outline-danger" :disabled="dept.doctor_count > 0">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                  
                  <!-- Doctors List -->
                  <div v-if="dept.doctors && dept.doctors.length > 0" class="mt-2 ps-3 border-start border-primary">
                    <ul class="list-unstyled mb-0 small text-muted">
                      <li v-for="doc in dept.doctors" :key="doc.id" class="mb-1">
                        {{ doc.user?.name || 'Unknown Doctor' }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Doctor Modal -->
    <div v-if="showDoctorModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content border-0 shadow-lg rounded-4">
          <div class="modal-header border-bottom-0 pb-0">
            <h5 class="modal-title fw-bold">Add New Doctor</h5>
            <button type="button" class="btn-close" @click="showDoctorModal = false"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="createDoctor">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Full Name</label>
                  <input v-model="newDoctor.name" class="form-control" placeholder="Dr. John Doe" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Email Address</label>
                  <input type="email" v-model="newDoctor.email" class="form-control" placeholder="doctor@hospital.com" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Password</label>
                  <input type="password" v-model="newDoctor.password" class="form-control" placeholder="••••••••" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Contact Number</label>
                  <input v-model="newDoctor.contact_number" class="form-control" placeholder="+1 234 567 890" required />
                </div>
                <div class="col-12">
                  <label class="form-label fw-bold small">Department</label>
                  <select v-model="newDoctor.department_id" class="form-select" required>
                    <option value="">Select Department</option>
                    <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                      {{ dept.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Specialization</label>
                  <input v-model="newDoctor.specialization" class="form-control" placeholder="e.g. Cardiology" required />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small">Experience (Years)</label>
                  <input type="number" v-model="newDoctor.experience" class="form-control" placeholder="e.g. 10" required />
                </div>
                <div class="col-12">
                  <label class="form-label fw-bold small">Qualifications</label>
                  <input v-model="newDoctor.qualifications" class="form-control" placeholder="e.g. MBBS, MD, PhD" required />
                </div>
              </div>
              
              <div class="d-flex gap-2 mt-4 pt-3 border-top">
                <button type="button" @click="showDoctorModal = false" class="btn btn-light flex-grow-1">Cancel</button>
                <button type="submit" class="btn btn-primary flex-grow-1 fw-bold">Create Doctor Account</button>
              </div>
            </form>
          </div>
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
