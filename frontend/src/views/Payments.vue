<template>
  <div class="d-flex min-vh-100 bg-light">
    <!-- Sidebar from your Dashboard theme -->
    <Sidebar />

    <main class="flex-grow-1 d-flex flex-column overflow-hidden">
      <!-- Header Area -->
      <div class="p-4 pb-0">
        <div class="d-flex justify-content-between align-items-end mb-4">
          <div>
            <h2 class="h3 fw-bold text-dark mb-1">Financial Dashboard</h2>
            <p class="text-muted mb-0">Track revenue, manage invoices, and process payments.</p>
          </div>
          <button v-if="isAdmin" class="btn btn-success fw-bold px-4 py-2 d-flex align-items-center gap-2" @click="showCreateModal = true">
            <span>+</span> New Invoice
          </button>
        </div>

        <!-- Stats Cards (Visible for ALL users now) -->
        <div class="row g-4 mb-4">
          <!-- Card 1: Revenue (Admin) / Total Billed (Patient) -->
          <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column justify-content-between">
                <div class="mb-4">
                  <div class="icon-circle bg-success bg-opacity-10 text-success mb-3">
                    <span class="fs-4">💰</span>
                  </div>
                  <div class="text-muted small fw-bold text-uppercase">
                    {{ isAdmin ? 'Total Revenue' : 'Total Billed' }}
                  </div>
                  <div class="d-flex align-items-baseline gap-2">
                    <h2 class="fw-bold text-dark mb-0">${{ stats.totalRevenue.toLocaleString() }}</h2>
                  </div>
                </div>
                <div class="text-success small fw-bold">
                  <span class="me-1">↑ 12%</span> vs last month
                </div>
              </div>
            </div>
          </div>

          <!-- Card 2: Pending Collection (Admin) / Due Amount (Patient) -->
          <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column justify-content-between">
                <div class="mb-4">
                  <div class="icon-circle bg-warning bg-opacity-10 text-warning mb-3">
                    <span class="fs-4">⏳</span>
                  </div>
                  <div class="text-muted small fw-bold text-uppercase">
                    {{ isAdmin ? 'Pending Collection' : 'Your Balance Due' }}
                  </div>
                  <div class="d-flex align-items-baseline gap-2">
                    <h2 class="fw-bold text-dark mb-0">${{ stats.pendingAmount.toLocaleString() }}</h2>
                  </div>
                </div>
                <div class="text-warning small fw-bold">
                  <span>• {{ pendingCount }}</span> invoices overdue
                </div>
              </div>
            </div>
          </div>

          <!-- Card 3: Monthly In-Flow (Admin) / Last Paid (Patient) -->
          <div class="col-md-4">
            <div class="card border-0 shadow-sm rounded-4 h-100">
              <div class="card-body p-4 d-flex flex-column justify-content-between">
                <div class="mb-4">
                  <div class="icon-circle bg-primary bg-opacity-10 text-primary mb-3">
                    <span class="fs-4">📊</span>
                  </div>
                  <div class="text-muted small fw-bold text-uppercase">
                    {{ isAdmin ? 'Monthly In-Flow' : 'Total Paid' }}
                  </div>
                  <div class="d-flex align-items-baseline gap-2">
                    <h2 class="fw-bold text-dark mb-0">${{ stats.thisMonth.toLocaleString() }}</h2>
                  </div>
                </div>
                <div class="text-muted small">
                  {{ isAdmin ? 'Current projection' : 'Lifetime payments' }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Controls Bar (Search Left, Toggles Right) -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <!-- Search -->
          <!-- Search -->
          <SearchBar 
            v-model="searchQuery" 
            placeholder="Search invoices, patients, or IDs..." 
            class="shadow-sm"
            style="width: 350px;"
          />

          <!-- Filter Toggles (Updated to Blue Theme) -->
          <div class="bg-white rounded-pill shadow-sm p-1 d-flex">
            <button class="btn btn-sm rounded-pill fw-bold px-3 transition-all" :class="filter === 'all' ? 'btn-primary' : 'text-muted'" @click="filter = 'all'">All</button>
            <button class="btn btn-sm rounded-pill fw-bold px-3 transition-all" :class="filter === 'pending' ? 'btn-primary' : 'text-muted'" @click="filter = 'pending'">
              Pending <span v-if="pendingCount > 0" class="badge bg-white text-primary rounded-circle ms-1" style="font-size: 8px; vertical-align: top;">{{ pendingCount }}</span>
            </button>
            <button class="btn btn-sm rounded-pill fw-bold px-3 transition-all" :class="filter === 'paid' ? 'btn-primary' : 'text-muted'" @click="filter = 'paid'">Paid</button>
          </div>
        </div>
      </div>

      <!-- Scrollable Table Area with "Floating Rows" -->
      <div class="flex-grow-1 overflow-auto px-4 pb-4 custom-scrollbar">
        <table class="table table-borderless floating-table">
          <thead>
            <tr>
              <th class="text-uppercase text-muted small fw-bold ps-4">Invoice Info</th>
              <th v-if="isAdmin" class="text-uppercase text-muted small fw-bold">Patient</th>
              <th class="text-uppercase text-muted small fw-bold">Date Issued</th>
              <th class="text-uppercase text-muted small fw-bold">Due Date</th>
              <th class="text-uppercase text-muted small fw-bold">Amount</th>
              <th class="text-uppercase text-muted small fw-bold">Status</th>
              <th class="text-uppercase text-muted small fw-bold text-end pe-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading"><td colspan="7" class="text-center py-5 text-muted">Loading transactions...</td></tr>
            <tr v-else-if="filteredBills.length === 0"><td colspan="7" class="text-center py-5 text-muted">No records found.</td></tr>
            
            <tr v-for="bill in filteredBills" :key="bill.id" class="align-middle shadow-sm bg-white rounded-3">
              <!-- Invoice Info -->
              <td class="ps-4 py-3 rounded-start-3">
                <div class="fw-bold text-dark">#{{ bill.id }}</div>
                <div class="small text-muted">{{ bill.extra_details?.department || 'General' }}</div>
                <div class="small text-primary mt-1" v-if="bill.extra_details?.doctor_name">
                  <i class="bi bi-person-fill me-1"></i>{{ bill.extra_details.doctor_name }}
                </div>
              </td>

              <!-- Patient -->
              <td v-if="isAdmin" class="py-3">
                <div class="d-flex align-items-center gap-3">
                  <div class="avatar-circle bg-success bg-opacity-10 text-success fw-bold small">
                    {{ getInitials(bill.extra_details?.patient_name) }}
                  </div>
                  <div>
                    <div class="fw-bold text-dark small">{{ bill.extra_details?.patient_name }}</div>
                    <div class="small text-muted" style="font-size: 11px;">{{ bill.patient_id }}</div>
                  </div>
                </div>
              </td>

              <!-- Date Issued -->
              <td class="py-3 text-muted small fw-medium">{{ new Date(bill.created_at).toLocaleDateString() }}</td>

              <!-- Due Date -->
              <td class="py-3 small fw-bold" :class="isOverdue(bill) ? 'text-danger' : 'text-dark'">
                {{ new Date(bill.due_date).toLocaleDateString() }}
              </td>

              <!-- Amount -->
              <td class="py-3 fw-bold text-dark">${{ bill.total_amount.toFixed(2) }}</td>

              <!-- Status -->
              <td class="py-3">
                 <span class="badge rounded-pill px-3 py-2 fw-bold" 
                      :class="{
                        'bg-success bg-opacity-10 text-success': bill.status === 'paid',
                        'bg-warning bg-opacity-10 text-warning': bill.status === 'pending',
                        'bg-danger bg-opacity-10 text-danger': bill.status === 'overdue'
                      }">
                    • {{ bill.status.toUpperCase() }}
                 </span>
              </td>

              <!-- Actions (Buttons Updated to Blue Theme) -->
              <td class="text-end pe-4 py-3 rounded-end-3">
                 <button v-if="bill.status !== 'paid'" 
                        class="btn btn-primary btn-sm fw-bold px-4 rounded-pill" 
                        @click="openPayModal(bill)">
                    Pay Now
                 </button>
                 <button v-else 
                        class="btn btn-light btn-sm text-dark border fw-bold px-3 rounded-pill" 
                        @click="generateReceipt(bill)">
                    Download PDF
                 </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- Payment Modal (Header Updated to Blue Theme) -->
    <Teleport to="body">
      <div v-if="showPayModal" class="modal-overlay d-flex align-items-center justify-content-center" @click.self="closePayModal">
        <div class="modal-content bg-white rounded-4 shadow-lg border-0" style="width: 450px; overflow: hidden;">
           <!-- Modal Header (Blue Background) -->
           <div class="bg-primary text-white p-4">
              <div class="d-flex justify-content-between align-items-start">
                 <div>
                    <h5 class="fw-bold mb-1">Confirm Payment</h5>
                    <div class="small opacity-75">Secure Transaction</div>
                 </div>
                 <button class="btn-close btn-close-white" @click="closePayModal"></button>
              </div>
              <div class="mt-4 d-flex justify-content-between align-items-end">
                 <div>
                    <div class="small opacity-75 text-uppercase">Total Amount</div>
                    <div class="h2 fw-bold mb-0">${{ selectedBill?.total_amount.toFixed(2) }}</div>
                 </div>
                 <div class="badge bg-white text-primary fw-normal px-3 py-2">INV #{{ selectedBill?.id }}</div>
              </div>
           </div>

           <!-- Modal Body -->
           <div class="p-4">
              <div class="mb-4">
                 <label class="form-label small fw-bold text-uppercase text-muted">Select Method</label>
                 <div class="row g-2">
                    <div class="col-4">
                       <div class="border rounded-3 p-3 text-center cursor-pointer transition-all" 
                            :class="paymentForm.method === 'card' ? 'border-primary bg-primary bg-opacity-10 text-primary' : 'bg-light'"
                            @click="paymentForm.method = 'card'">
                          <div class="h4 mb-1">💳</div>
                          <div class="small fw-bold">Card</div>
                       </div>
                    </div>
                    <div class="col-4" v-if="!isAdmin">
                       <div class="border rounded-3 p-3 text-center cursor-pointer transition-all"
                            :class="paymentForm.method === 'insurance' ? 'border-primary bg-primary bg-opacity-10 text-primary' : 'bg-light'"
                            @click="paymentForm.method = 'insurance'">
                          <div class="h4 mb-1">🏥</div>
                          <div class="small fw-bold">Ins.</div>
                       </div>
                    </div>
                    <div class="col-4" v-if="isAdmin">
                       <div class="border rounded-3 p-3 text-center cursor-pointer transition-all"
                            :class="paymentForm.method === 'cash' ? 'border-primary bg-primary bg-opacity-10 text-primary' : 'bg-light'"
                            @click="paymentForm.method = 'cash'">
                          <div class="h4 mb-1">💵</div>
                          <div class="small fw-bold">Cash</div>
                       </div>
                    </div>
                 </div>
              </div>

              <div v-if="paymentForm.method === 'card'" class="mb-4">
                 <label class="form-label small fw-bold text-uppercase text-muted">Card Details</label>
                 <div class="bg-light rounded-3 p-3 border">
                    <div class="d-flex justify-content-between mb-3">
                       <div class="small text-muted">Card Number</div>
                       <div class="small fw-bold font-monospace">**** **** **** 4242</div>
                    </div>
                    <div class="d-flex gap-4">
                       <div>
                          <div class="small text-muted">Expiry</div>
                          <div class="small fw-bold font-monospace">12/25</div>
                       </div>
                       <div>
                          <div class="small text-muted">CVC</div>
                          <div class="small fw-bold font-monospace">***</div>
                       </div>
                    </div>
                 </div>
              </div>

              <button class="btn btn-primary w-100 py-3 fw-bold shadow-sm" @click="processPayment" :disabled="processing">
                 {{ processing ? 'Processing...' : 'Complete Payment' }}
              </button>
           </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import Sidebar from '@/components/Sidebar.vue';
import api from '@/services/api';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import SearchBar from '@/components/SearchBar.vue';

const store = useStore();
const isAdmin = computed(() => store.getters.currentUser?.role === 'admin');
const userName = computed(() => store.getters.currentUser?.name || 'User');
const bills = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const filter = ref('all');

const showPayModal = ref(false);
const selectedBill = ref(null);
const processing = ref(false);
const paymentForm = ref({ method: 'card' });

// --- Real Data & API Integration ---
const loadBills = async () => {
  loading.value = true;
  try {
    const res = await api.get('/billing/');
    bills.value = res.data;
  } catch (err) {
    console.error("Failed to load bills", err);
  } finally {
    loading.value = false;
  }
};

const stats = computed(() => {
  const totalRevenue = bills.value.filter(b => b.status === 'paid').reduce((sum, b) => sum + b.total_amount, 0);
  const pendingAmount = bills.value.filter(b => b.status === 'pending' || b.status === 'overdue').reduce((sum, b) => sum + b.total_amount, 0);
  return { totalRevenue, pendingAmount, thisMonth: totalRevenue * 0.45 };
});

const filteredBills = computed(() => {
  return bills.value.filter(b => {
    const query = searchQuery.value.toLowerCase();
    const details = b.extra_details || {};
    const matchesSearch = b.id.toString().includes(query) || (details.patient_name?.toLowerCase() || '').includes(query);
    const matchesFilter = filter.value === 'all' || b.status === filter.value;
    return matchesSearch && matchesFilter;
  });
});

const pendingCount = computed(() => bills.value.filter(b => b.status === 'pending').length);
const getInitials = (name) => name ? name.split(' ').map(n=>n[0]).join('').substring(0,2) : 'U';
const isOverdue = (bill) => (bill.status === 'pending' || bill.status === 'overdue') && new Date(bill.due_date) < new Date();

const openPayModal = (bill) => {
  selectedBill.value = bill;
  showPayModal.value = true;
};

const closePayModal = () => {
  showPayModal.value = false;
  setTimeout(() => { selectedBill.value = null; }, 200);
  paymentForm.value = { method: 'card' };
};

const processPayment = async () => {
  if (!selectedBill.value) return;
  processing.value = true;
  try {
    await api.post(`/billing/${selectedBill.value.id}/pay`, {
        amount_paid: selectedBill.value.total_amount,
        payment_method: paymentForm.value.method
    });
    // Success
    await loadBills(); // Reload real data
    closePayModal();
    alert('Payment Successful! DONE:');
  } catch (err) {
    alert("Payment failed: " + (err.response?.data?.message || err.message));
  } finally {
    processing.value = false;
  }
};

// --- PDF Generation (Premium) ---
const generateReceipt = (bill) => {
    const doc = new jsPDF();
    const details = bill.extra_details || {};
    const payment = bill.payments && bill.payments.length > 0 ? bill.payments[0] : null;
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();

    // ============ OUTER BORDER ============
    doc.setDrawColor(0, 0, 0);
    doc.setLineWidth(0.8);
    doc.rect(8, 8, pageWidth - 16, pageHeight - 16);

    // ============ HEADER SECTION ============
    // Header background
    doc.setFillColor(25, 25, 112);
    doc.rect(8, 8, pageWidth - 16, 42, 'F');

    // Logo box
    doc.setFillColor(255, 255, 255);
    doc.rect(15, 15, 28, 28);
    doc.setFontSize(7);
    doc.setTextColor(25, 25, 112);
    doc.setFont("helvetica", "bold");
    doc.text("FALCO", 29, 26, { align: "center" });
    doc.text("VITA", 29, 31, { align: "center" });
    doc.setFontSize(5);
    doc.text("HOSPITAL", 29, 36, { align: "center" });

    // Hospital name and details
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(22);
    doc.setFont("helvetica", "bold");
    doc.text("FALCOVITA HOSPITAL", pageWidth / 2, 24, { align: "center" });
    
    doc.setFontSize(8);
    doc.setFont("helvetica", "normal");
    doc.text("123 Healthcare Boulevard, Medical District, New York, NY 10001", pageWidth / 2, 32, { align: "center" });
    doc.text("Tel: +1 (555) 0123-456  |  Email: billing@falcovita.com  |  Tax ID: 12-3456789", pageWidth / 2, 38, { align: "center" });
    doc.text("24/7 Emergency Services Available  |  www.falcovitahospital.com", pageWidth / 2, 44, { align: "center" });

    // ============ RECEIPT TITLE ============
    doc.setTextColor(0, 0, 0);
    doc.setFontSize(18);
    doc.setFont("helvetica", "bold");
    doc.text("OFFICIAL PAYMENT RECEIPT", pageWidth / 2, 58, { align: "center" });
    
    doc.setDrawColor(25, 25, 112);
    doc.setLineWidth(0.5);
    doc.line(60, 60, pageWidth - 60, 60);

    // ============ RECEIPT METADATA BOX ============
    doc.setFillColor(248, 249, 250);
    doc.setDrawColor(200, 200, 200);
    doc.setLineWidth(0.3);
    doc.roundedRect(15, 66, pageWidth - 30, 24, 2, 2, 'FD');

    // Left column
    doc.setFontSize(8);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(80, 80, 80);
    doc.text("RECEIPT NO:", 20, 73);
    doc.text("INVOICE NO:", 20, 78);
    doc.text("ISSUE DATE:", 20, 83);
    
    doc.setFont("helvetica", "normal");
    doc.setTextColor(0, 0, 0);
    doc.setFontSize(9);
    doc.text(`FV-${new Date().getFullYear()}-${bill.id.toString().padStart(6, '0')}`, 48, 73);
    doc.text(`INV-${bill.id.toString().padStart(6, '0')}`, 48, 78);
    
    // Define issueDate (Appointment Date or Created At)
    const issueDate = details.appointment_date ? new Date(details.appointment_date).toLocaleDateString() : new Date(bill.created_at).toLocaleDateString();
    doc.text(issueDate, 48, 83);

    // Center column
    doc.setFontSize(8);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(80, 80, 80);
    doc.text("BILL DATE:", 95, 73);
    doc.text("DUE DATE:", 95, 78);
    doc.text("PAYMENT DATE:", 95, 83);
    
    doc.setFont("helvetica", "normal");
    doc.setTextColor(0, 0, 0);
    doc.setFontSize(9);

    doc.text(issueDate, 123, 73);
    doc.text(new Date(bill.due_date).toLocaleDateString(), 123, 78);
    doc.text(payment ? new Date(payment.payment_date).toLocaleDateString() : 'Pending', 123, 83);

    // Right column - Status badge
    if (payment) {
        doc.setFillColor(34, 197, 94);
        doc.roundedRect(155, 70, 35, 12, 2, 2, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(10);
        doc.setFont("helvetica", "bold");
        doc.text("PAID", 172.5, 78, { align: "center" });
    } else {
        doc.setFillColor(239, 68, 68);
        doc.roundedRect(152, 70, 38, 12, 2, 2, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(10);
        doc.setFont("helvetica", "bold");
        doc.text("UNPAID", 171, 78, { align: "center" });
    }

    // ============ PATIENT & VISIT INFO BOXES ============
    // Patient box
    doc.setDrawColor(200, 200, 200);
    doc.setLineWidth(0.4);
    doc.roundedRect(15, 96, 89, 40, 2, 2, 'D');
    
    doc.setFillColor(25, 25, 112);
    doc.roundedRect(15, 96, 89, 8, 2, 2, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(9);
    doc.setFont("helvetica", "bold");
    doc.text("PATIENT INFORMATION", 20, 101);

    doc.setFontSize(8);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(80, 80, 80);
    doc.text("Name:", 20, 110);
    doc.text("UHID:", 20, 116);
    doc.text("Contact:", 20, 122);
    doc.text("Address:", 20, 128);
    
    doc.setFont("helvetica", "normal");
    doc.setTextColor(0, 0, 0);
    doc.setFontSize(8);
    
    doc.text((details.patient_name || 'Not Provided').substring(0, 30), 38, 110);
    doc.text(details.patient_uhid || `P-${bill.patient_id}`, 38, 116);
    doc.text(details.patient_contact || 'Not Provided', 38, 122);
    doc.text((details.patient_address || 'Not Provided').substring(0, 30), 38, 128);

    // Visit box
    doc.roundedRect(106, 96, 89, 40, 2, 2, 'D');
    
    doc.setFillColor(25, 25, 112);
    doc.roundedRect(106, 96, 89, 8, 2, 2, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(9);
    doc.setFont("helvetica", "bold");
    doc.text("VISIT DETAILS", 111, 101);

    doc.setFontSize(8);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(80, 80, 80);
    doc.text("Consulting Doctor:", 111, 110);
    doc.text("Department:", 111, 116);
    doc.text("Visit Type:", 111, 122);
    doc.text("Visit ID:", 111, 128);
    
    doc.setFont("helvetica", "normal");
    doc.setTextColor(0, 0, 0);
    doc.setFontSize(8);
    
    doc.text((details.doctor_name || 'Dr. General').substring(0, 28), 147, 110);
    doc.text((details.department || 'General').substring(0, 28), 147, 116);
    doc.text(details.visit_type || 'OPD', 147, 122);
    doc.text(details.visit_id || `VST-${bill.id}`, 147, 128);

    // ============ SERVICES TABLE ============
    const tableData = [
        ["Medical Consultation & Services", "1", `${bill.total_amount.toFixed(2)}`, `${bill.total_amount.toFixed(2)}`],
    ];

    autoTable(doc, {
        startY: 143,
        head: [['DESCRIPTION OF SERVICES', 'QTY', 'UNIT PRICE', 'AMOUNT']],
        body: tableData,
        theme: 'grid',
        headStyles: { 
            fillColor: [25, 25, 112],
            textColor: [255, 255, 255],
            fontSize: 8,
            fontStyle: 'bold',
            halign: 'center',
            cellPadding: 3
        },
        bodyStyles: {
            fontSize: 9,
            textColor: [0, 0, 0],
            cellPadding: 3
        },
        columnStyles: {
            0: { cellWidth: 105, halign: 'left' },
            1: { cellWidth: 20, halign: 'center' },
            2: { cellWidth: 35, halign: 'right' },
            3: { cellWidth: 25, halign: 'right', fontStyle: 'bold' }
        },
        margin: { left: 15, right: 15 },
        tableLineColor: [200, 200, 200],
        tableLineWidth: 0.3
    });

    const finalY = doc.lastAutoTable.finalY || 160;

    // ============ FINANCIAL SUMMARY ============
    doc.setDrawColor(200, 200, 200);
    doc.setLineWidth(0.4);
    doc.roundedRect(125, finalY + 8, 70, 42, 2, 2, 'D');

    doc.setFontSize(8);
    doc.setFont("helvetica", "normal");
    doc.setTextColor(80, 80, 80);
    doc.text("Subtotal:", 130, finalY + 16);
    doc.text("Tax (0%):", 130, finalY + 22);
    doc.text("Discount:", 130, finalY + 28);
    
    doc.setTextColor(0, 0, 0);
    doc.text(`${bill.total_amount.toFixed(2)}`, 190, finalY + 16, { align: 'right' });
    doc.text("$0.00", 190, finalY + 22, { align: 'right' });
    doc.text("- $0.00", 190, finalY + 28, { align: 'right' });
    
    doc.setDrawColor(25, 25, 112);
    doc.setLineWidth(0.8);
    doc.line(130, finalY + 32, 190, finalY + 32);
    
    doc.setFillColor(25, 25, 112);
    doc.roundedRect(125, finalY + 35, 70, 15, 2, 2, 'F');
    doc.setFontSize(11);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(255, 255, 255);
    doc.text("TOTAL AMOUNT:", 130, finalY + 44);
    doc.text(`${bill.total_amount.toFixed(2)}`, 190, finalY + 44, { align: 'right' });

    // ============ PAYMENT STATUS SECTION ============
    const statusY = finalY + 60;
    
    if (payment) {
        doc.setFillColor(220, 252, 231);
        doc.setDrawColor(34, 197, 94);
        doc.setLineWidth(1.2);
        doc.roundedRect(15, statusY, 180, 32, 3, 3, 'FD');
        
        doc.setFontSize(14);
        doc.setFont("helvetica", "bold");
        doc.setTextColor(21, 128, 61);
        doc.text("✓ PAYMENT RECEIVED - THANK YOU", pageWidth / 2, statusY + 11, { align: "center" });
        
        doc.setFontSize(8);
        doc.setFont("helvetica", "normal");
        doc.setTextColor(60, 60, 60);
        doc.text(`Payment Method: ${payment.payment_method.toUpperCase()}`, 22, statusY + 20);
        doc.text(`Transaction ID: ${payment.transaction_id || 'N/A'}`, 22, statusY + 26);
        
        doc.text(`Amount Paid: ${bill.total_amount.toFixed(2)}`, 140, statusY + 20);
        doc.text(`Status: CLEARED`, 140, statusY + 26);
    } else {
        doc.setFillColor(254, 242, 242);
        doc.setDrawColor(239, 68, 68);
        doc.setLineWidth(1.2);
        doc.roundedRect(15, statusY, 180, 32, 3, 3, 'FD');
        
        doc.setFontSize(14);
        doc.setFont("helvetica", "bold");
        doc.setTextColor(185, 28, 28);
        doc.text("⚠ PAYMENT PENDING", pageWidth / 2, statusY + 11, { align: "center" });
        
        doc.setFontSize(8);
        doc.setFont("helvetica", "normal");
        doc.setTextColor(60, 60, 60);
        doc.text(`Outstanding Balance: ${bill.total_amount.toFixed(2)}`, pageWidth / 2, statusY + 20, { align: "center" });
        doc.text(`Payment Due By: ${new Date(bill.due_date).toLocaleDateString()}`, pageWidth / 2, statusY + 26, { align: "center" });
    }

    // ============ TERMS & CONDITIONS ============
    const termsY = statusY + 40;
    doc.setFontSize(8);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(60, 60, 60);
    doc.text("TERMS & CONDITIONS:", 15, termsY);
    
    doc.setFont("helvetica", "normal");
    doc.setFontSize(7);
    doc.setTextColor(80, 80, 80);
    const terms = [
        "1. This is an official computer-generated receipt and does not require a physical signature.",
        "2. Please retain this document for insurance reimbursement and tax purposes.",
        "3. For billing inquiries, contact our accounts department: billing@falcovita.com | +1 (555) 0123-456",
        "4. Payments by check should be made payable to 'FalcoVita Hospital' with receipt number on the memo line.",
        "5. All refunds will be processed within 14-21 business days from the date of request approval."
    ];
    
    let currentY = termsY + 5;
    terms.forEach(term => {
        doc.text(term, 15, currentY);
        currentY += 3.5;
    });

    // ============ FOOTER ============
    doc.setDrawColor(25, 25, 112);
    doc.setLineWidth(0.5);
    doc.line(15, pageHeight - 22, pageWidth - 15, pageHeight - 22);
    
    doc.setFontSize(7);
    doc.setTextColor(100, 100, 100);
    doc.setFont("helvetica", "italic");
    doc.text("Thank you for choosing FalcoVita Hospital for your healthcare needs.", pageWidth / 2, pageHeight - 17, { align: "center" });
    
    doc.setFont("helvetica", "normal");
    doc.setFontSize(6);
    doc.text(`Document generated on: ${new Date().toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' })}`, pageWidth / 2, pageHeight - 13, { align: "center" });
    doc.text("This is a computer-generated receipt and is valid without signature or stamp.", pageWidth / 2, pageHeight - 10, { align: "center" });
    
    // Save with professional filename
    const fileName = `FalcoVita_Receipt_${bill.id.toString().padStart(6, '0')}_${new Date().getFullYear()}.pdf`;
    doc.save(fileName);
};

onMounted(() => {
    loadBills();
});
</script>

<style scoped>
/* Key Styling for the "Floating Row" Table from your image */
.floating-table {
  border-collapse: separate;
  border-spacing: 0 15px; /* Creates the gap between rows */
}

.floating-table tbody tr {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.floating-table tbody tr:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.08) !important;
}

/* Rounded corners for the start and end of rows */
.rounded-start-3 { border-top-left-radius: 12px; border-bottom-left-radius: 12px; }
.rounded-end-3 { border-top-right-radius: 12px; border-bottom-right-radius: 12px; }

.icon-circle {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background-color: rgba(0,0,0,0.1); border-radius: 10px; }
.transition-all { transition: all 0.2s ease; }
.modal-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.5); z-index: 2000; backdrop-filter: blur(2px); }
.cursor-pointer { cursor: pointer; }
</style>