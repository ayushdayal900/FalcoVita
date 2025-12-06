<template>
  <div class="d-flex min-vh-100 bg-light">
    <Sidebar />
    
    <main class="flex-grow-1 p-4 overflow-auto">
      <div class="container-fluid" style="max-width: 1200px;">
        
        <!-- Header -->
        <header class="d-flex justify-content-between align-items-center mb-4">
          <div>
            <h1 class="h3 fw-bold text-dark mb-1">Payments & Billing</h1>
            <p class="text-muted mb-0">{{ isAdmin ? 'Manage hospital finances and patient bills' : 'View and pay your medical bills' }}</p>
          </div>
          <button v-if="isAdmin" class="btn btn-primary" @click="showCreateModal = true">
            + Create New Bill
          </button>
        </header>

        <!-- Stats Cards (Admin Only) -->
        <div v-if="isAdmin" class="row g-3 mb-4">
          <div class="col-md-3">
             <div class="card border-0 shadow-sm h-100 border-start border-4 border-primary">
               <div class="card-body">
                 <h6 class="text-uppercase text-muted small fw-bold">Total Revenue</h6>
                 <h2 class="mb-0 text-dark">${{ stats.totalRevenue.toLocaleString() }}</h2>
               </div>
             </div>
          </div>
          <div class="col-md-3">
             <div class="card border-0 shadow-sm h-100 border-start border-4 border-warning">
               <div class="card-body">
                 <h6 class="text-uppercase text-muted small fw-bold">Pending</h6>
                 <h2 class="mb-0 text-dark">${{ stats.pendingAmount.toLocaleString() }}</h2>
               </div>
             </div>
          </div>
          <div class="col-md-3">
             <div class="card border-0 shadow-sm h-100 border-start border-4 border-success">
               <div class="card-body">
                 <h6 class="text-uppercase text-muted small fw-bold">Collected (This Month)</h6>
                 <h2 class="mb-0 text-dark">${{ stats.thisMonth.toLocaleString() }}</h2>
               </div>
             </div>
          </div>
        </div>

        <!-- Filters & Search -->
        <div class="card border-0 shadow-sm mb-4">
            <div class="card-body py-2">
                <div class="row align-items-center">
                    <div class="col-md-4">
                        <div class="input-group input-group-sm">
                            <span class="input-group-text bg-white border-end-0">🔍</span>
                            <input type="text" class="form-control border-start-0 ps-0" placeholder="Search by Bill ID or Patient..." v-model="searchQuery">
                        </div>
                    </div>
                    <div class="col-md-8 text-end">
                         <div class="btn-group btn-group-sm">
                            <button class="btn" :class="filter === 'all' ? 'btn-primary' : 'btn-outline-secondary'" @click="filter = 'all'">All</button>
                            <button class="btn" :class="filter === 'pending' ? 'btn-primary' : 'btn-outline-secondary'" @click="filter = 'pending'">Pending</button>
                            <button class="btn" :class="filter === 'paid' ? 'btn-primary' : 'btn-outline-secondary'" @click="filter = 'paid'">Paid</button>
                         </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Bills List -->
        <div class="card border-0 shadow-sm">
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="bg-light">
                  <tr>
                    <th class="ps-4">Bill ID</th>
                    <th v-if="isAdmin">Patient ID</th>
                    <th>Date</th>
                    <th>Due Date</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th class="text-end pe-4">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="loading" class="text-center"><td colspan="7" class="py-4 text-muted">Loading transactions...</td></tr>
                  <tr v-else-if="filteredBills.length === 0" class="text-center"><td colspan="7" class="py-4 text-muted">No bills found.</td></tr>
                  
                  <tr v-for="bill in filteredBills" :key="bill.id">
                    <td class="ps-4 fw-medium text-primary">#INV-{{ bill.id }}</td>
                    <td v-if="isAdmin"><span class="badge bg-light text-dark border">User #{{ bill.patient_id }}</span></td>
                    <td class="text-muted small">{{ new Date(bill.created_at).toLocaleDateString() }}</td>
                    <td class="small" :class="isOverdue(bill) ? 'text-danger fw-bold' : ''">{{ new Date(bill.due_date).toLocaleDateString() }}</td>
                    <td class="fw-bold">${{ bill.total_amount.toFixed(2) }}</td>
                    <td>
                        <span class="badge rounded-pill" 
                              :class="{
                                'bg-success-subtle text-success': bill.status === 'paid',
                                'bg-warning-subtle text-warning-emphasis': bill.status === 'pending',
                                'bg-danger-subtle text-danger': bill.status === 'overdue' || bill.status === 'partial'
                              }">
                            {{ bill.status.toUpperCase() }}
                        </span>
                    </td>
                    <td class="text-end pe-4">
                        <button v-if="bill.status !== 'paid'" 
                                class="btn btn-sm btn-primary px-3" 
                                @click="openPayModal(bill)">
                            {{ isAdmin ? 'Record Payment' : 'Pay Now' }}
                        </button>
                        <button v-else 
                                class="btn btn-sm btn-outline-dark" 
                                @click="generateReceipt(bill)">
                            ⬇ Receipt
                        </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>
    </main>

    <!-- Payment Modal -->
    <Teleport to="body">
    <div v-if="showPayModal" class="modal-overlay d-flex align-items-center justify-content-center">
        <div class="modal-dialog card border-0 shadow-lg" style="width: 400px; pointer-events: auto;">
            <div class="card-header bg-white border-bottom-0 pt-4 px-4 pb-0 d-flex justify-content-between">
                <h5 class="fw-bold">Make Payment</h5>
                <button class="btn-close" @click="closePayModal"></button>
            </div>
            <div class="card-body px-4">
                <div class="bg-light p-3 rounded mb-3">
                    <div class="d-flex justify-content-between text-muted small mb-1">
                        <span>Invoice</span>
                        <span>#INV-{{ selectedBill.id }}</span>
                    </div>
                    <div class="d-flex justify-content-between fw-bold fs-5">
                        <span>Total Due</span>
                        <span>${{ selectedBill.total_amount.toFixed(2) }}</span>
                    </div>
                </div>

                <div class="mb-3">
                    <label class="form-label small fw-bold text-muted">Payment Method</label>
                    <select class="form-select" v-model="paymentForm.method">
                        <option value="card">Credit/Debit Card</option>
                        <option value="insurance" v-if="!isAdmin">Insurance</option>
                        <option value="cash" v-if="isAdmin">Cash</option>
                    </select>
                </div>
                
                <div class="mb-4" v-if="paymentForm.method === 'card'">
                     <label class="form-label small fw-bold text-muted">Card Details (Mock)</label>
                     <div class="form-control bg-light text-muted">**** **** **** 4242</div>
                </div>

            </div>
            <div class="card-footer bg-white border-top-0 pb-4 px-4 pt-0">
                <div class="d-flex gap-2">
                    <button class="btn btn-outline-primary w-50 py-2 fs-6 fw-bold" @click="handlePayLater">
                        Pay Later
                    </button>
                    <button class="btn btn-success w-50 py-2 fs-6 fw-bold" @click="processPayment" :disabled="processing">
                        {{ processing ? 'Processing...' : `Pay $${selectedBill.total_amount.toFixed(2)}` }}
                    </button>
                </div>
            </div>
        </div>
    </div>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import api from '@/services/api';
import Sidebar from '@/components/Sidebar.vue';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

const store = useStore();
const isAdmin = computed(() => store.getters.currentUser?.role === 'admin');
const bills = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const filter = ref('all');

const showPayModal = ref(false);
const showCreateModal = ref(false);
const selectedBill = ref(null);
const processing = ref(false);
const paymentForm = ref({ method: 'card' });

// Admin Stats
const stats = computed(() => {
    const totalRevenue = bills.value.filter(b => b.status === 'paid').reduce((sum, b) => sum + b.total_amount, 0);
    const pendingAmount = bills.value.filter(b => b.status === 'pending').reduce((sum, b) => sum + b.total_amount, 0);
    return { totalRevenue, pendingAmount, thisMonth: totalRevenue * 0.4 }; // Mock monthly
});

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

const filteredBills = computed(() => {
    return bills.value.filter(b => {
        const matchesSearch = b.id.toString().includes(searchQuery.value) || (isAdmin.value && b.patient_id.toString().includes(searchQuery.value));
        const matchesFilter = filter.value === 'all' || b.status === filter.value;
        return matchesSearch && matchesFilter;
    });
});

const isOverdue = (bill) => {
    return bill.status === 'pending' && new Date(bill.due_date) < new Date();
};

const openPayModal = (bill) => {
    selectedBill.value = bill;
    showPayModal.value = true;
};

const closePayModal = () => {
    showPayModal.value = false;
    selectedBill.value = null;
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
        await loadBills(); // Reload
        closePayModal();
        alert('Payment Successful! ✅');
    } catch (err) {
        alert("Payment failed: " + (err.response?.data?.message || err.message));
    } finally {
        processing.value = false;
    }
};

const handlePayLater = () => {
    alert("Bill remains pending. You can pay anytime from this dashboard.");
    closePayModal();
};

/* ----------------------------------------------------
   RECEIPT GENERATION
---------------------------------------------------- */
const generateReceipt = (bill) => {
    const doc = new jsPDF();
    const details = bill.extra_details || {};
    const payment = bill.payments && bill.payments.length > 0 ? bill.payments[0] : null;

    // 1. Hospital Info
    doc.setFontSize(18);
    doc.setTextColor(13, 110, 253); // Bootstrap Primary Color
    doc.text("FalcoVita Hospital", 105, 15, { align: "center" });
    
    doc.setFontSize(10);
    doc.setTextColor(100);
    doc.text("123 Healthcare Blvd, Medical District, NY 10001", 105, 22, { align: "center" });
    doc.text("Phone: +1 555-0123 | Email: billing@falcovita.com", 105, 27, { align: "center" });
    doc.line(15, 30, 195, 30); // Divider

    // 2. Receipt Details
    doc.setFontSize(11);
    doc.setTextColor(0);
    doc.text(`Receipt No: FV-${new Date().getFullYear()}-${bill.id.toString().padStart(6, '0')}`, 15, 40);
    doc.text(`Date: ${new Date().toLocaleDateString()}`, 150, 40);

    // 3. Patient Information
    doc.setFontSize(12);
    doc.setFont("helvetica", "bold");
    doc.text("Patient Details", 15, 55);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    
    doc.text(`Name: ${details.patient_name || 'N/A'}`, 15, 62);
    doc.text(`UHID: ${details.patient_uhid || bill.patient_id}`, 15, 67);
    doc.text(`Contact: ${details.patient_contact || 'N/A'}`, 15, 72);

    // 4. Visit Details
    doc.setFontSize(12);
    doc.setFont("helvetica", "bold");
    doc.text("Visit Details", 110, 55);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);

    doc.text(`Doctor: ${details.doctor_name || 'N/A'}`, 110, 62);
    doc.text(`Dept: ${details.department || 'General'}`, 110, 67);
    doc.text(`Type: ${details.visit_type || 'OPD'}`, 110, 72);

    // 5. Fee Breakdown Table
    const tableData = [
        ["Consultation Fee", "1", `₹${bill.total_amount}`, `₹${bill.total_amount}`],
    ];

    autoTable(doc, {
        startY: 85,
        head: [['Description', 'Qty', 'Rate', 'Amount']],
        body: tableData,
        theme: 'striped',
        headStyles: { fillColor: [13, 110, 253] }
    });

    const finalY = doc.lastAutoTable.finalY + 10;

    // 8. Total Summary
    doc.text(`Subtotal:`, 140, finalY);
    doc.text(`₹${bill.total_amount.toFixed(2)}`, 180, finalY, { align: 'right' });
    
    doc.text(`Total Discount:`, 140, finalY + 5);
    doc.text(`- ₹0.00`, 180, finalY + 5, { align: 'right' });

    doc.setFont("helvetica", "bold");
    doc.text(`Net Payable:`, 140, finalY + 12);
    doc.text(`₹${bill.total_amount.toFixed(2)}`, 180, finalY + 12, { align: 'right' });
    doc.setFont("helvetica", "normal");

    // 9. Payment Confirmation
    if (payment) {
        doc.setFillColor(220, 255, 220);
        doc.rect(15, finalY, 100, 25, 'F');
        doc.setTextColor(0, 100, 0);
        doc.setFontSize(10);
        doc.text(`Status: PAID`, 20, finalY + 7);
        doc.text(`Method: ${payment.payment_method.toUpperCase()}`, 20, finalY + 12);
        doc.text(`Txn ID: ${payment.transaction_id}`, 20, finalY + 17);
    } else {
        doc.setFillColor(255, 240, 240);
        doc.rect(15, finalY, 100, 20, 'F');
        doc.setTextColor(150, 0, 0);
        doc.text(`Status: PENDING / UNPAID`, 20, finalY + 10);
    }

    // 10. Terms
    doc.setTextColor(150);
    doc.setFontSize(8);
    doc.text("This is a system-generated receipt and does not require signature.", 105, 280, { align: "center" });
    
    // Save
    doc.save(`Receipt-${bill.id}.pdf`);
};

onMounted(() => {
    loadBills();
});
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    z-index: 2000;
    backdrop-filter: blur(2px);
}
.bg-success-subtle { background-color: #d1e7dd; }
.text-success { color: #146c43; }
.bg-warning-subtle { background-color: #fff3cd; }
.text-warning-emphasis { color: #664d03; }
</style>
