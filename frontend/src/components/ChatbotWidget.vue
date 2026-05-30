<template>
  <div class="chatbot-wrapper">
    <button class="chatbot-toggle" @click="toggleChat">
      <span v-if="!isOpen">💬</span>
      <span v-else>✖</span>
    </button>

    <div v-if="isOpen" class="chatbot-window card shadow">
      <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
        <h6 class="mb-0">FalcoVita AI</h6>
        <div class="d-flex gap-2">
          <button class="btn btn-sm btn-link text-white p-0" @click="toggleSpeech">
            {{ isSpeaking ? '🔇' : '🔊' }}
          </button>
          <small>Online</small>
        </div>
      </div>

      <div class="card-body chat-body" ref="chatContainer">
        <div v-for="msg in messages" :key="msg.id" :class="['message', msg.sender]">
          <div class="message-content">
            {{ msg.text }}

            <!-- ACTIONS -->
            <div v-if="msg.action" class="mt-2">

              <!-- BOOK APPOINTMENT -->
              <button 
                v-if="msg.action.action === 'book_appointment'"
                class="btn btn-sm btn-light border"
                @click="handleAction(msg.action)">
                Confirm Booking →
              </button>

              <!-- CANCEL APPOINTMENT -->
              <button 
                v-if="msg.action.action === 'cancel_appointment'"
                class="btn btn-sm btn-danger border"
                @click="handleAction(msg.action)">
                Cancel Appointment →
              </button>

              <!-- CHECK AVAILABILITY -->
              <div 
                v-if="msg.action.action === 'check_availability'" 
                class="d-flex flex-wrap gap-2">
                <button 
                  v-for="slot in msg.action.data.slots || []"
                  :key="slot"
                  class="btn btn-sm btn-outline-primary"
                  @click="chooseSlot(slot, msg.action)">
                  {{ slot }}
                </button>
              </div>

              <!-- CHOICE BUTTONS -->
              <div v-if="msg.action.action === 'choices'" class="d-flex flex-wrap gap-2">
                <button
                  v-for="opt in msg.action.data.options"
                  :key="opt"
                  @click="sendMessage(opt)">
                  {{ opt }}
                </button>
              </div>

              <!-- ESCALATION -->
              <div v-if="msg.action.action === 'escalate_to_human'" class="alert alert-warning p-2 mt-2">
                <strong>Support ticket created</strong><br>
                A staff member will contact you shortly.
              </div>

              <!-- AUTO-EXECUTED ACTIONS (LOADING, ERROR, AND PREMIUM UI CARDS) -->
              <div v-if="msg.actionLoading" class="mt-2 text-center text-muted py-2">
                <div class="spinner-border spinner-border-sm text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <span class="ms-2" style="font-size: 0.8rem;">Retrieving details...</span>
              </div>

              <div v-if="msg.actionError" class="mt-2 alert alert-danger p-2" style="font-size: 0.8rem;">
                {{ msg.actionError }}
              </div>

              <!-- BILLING INFO CARD -->
              <div v-if="msg.action.action === 'get_billing_info' && msg.actionResult" class="mt-2 p-2 bg-white rounded border border-light-subtle shadow-sm text-start">
                <div class="d-flex justify-content-between align-items-center mb-2 pb-1 border-bottom">
                  <span class="fw-bold text-dark" style="font-size: 0.8rem;">Billing Summary</span>
                  <span class="badge bg-warning-subtle text-warning-emphasis" style="font-size: 0.65rem;">
                    Dues: {{ msg.actionResult.summary?.outstanding_bills || 0 }}
                  </span>
                </div>
                <div class="row g-1 mb-2">
                  <div class="col-6">
                    <div class="p-1 bg-danger-subtle rounded text-center" style="font-size: 0.7rem;">
                      <span class="text-uppercase text-danger-emphasis d-block fw-semibold" style="font-size: 0.55rem;">Total Due</span>
                      <strong class="text-danger-emphasis">${{ msg.actionResult.summary?.total_due || 0 }}</strong>
                    </div>
                  </div>
                  <div class="col-6">
                    <div class="p-1 bg-success-subtle rounded text-center" style="font-size: 0.7rem;">
                      <span class="text-uppercase text-success-emphasis d-block fw-semibold" style="font-size: 0.55rem;">Total Paid</span>
                      <strong class="text-success-emphasis">${{ msg.actionResult.summary?.total_paid || 0 }}</strong>
                    </div>
                  </div>
                </div>
                <div class="billing-list overflow-y-auto" style="max-height: 120px; font-size: 0.75rem;">
                  <div v-if="!msg.actionResult.bills || msg.actionResult.bills.length === 0" class="text-muted text-center py-1">No billing records.</div>
                  <div v-else v-for="bill in msg.actionResult.bills" :key="bill.id" class="p-2 border-bottom border-light mb-1 bg-light rounded-1">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <span class="fw-bold text-dark" style="font-size: 0.7rem;">{{ bill.invoice_number }}</span>
                      <span :class="['badge', bill.status === 'paid' ? 'bg-success-subtle text-success-emphasis' : 'bg-danger-subtle text-danger-emphasis']" style="font-size: 0.6rem;">
                        {{ bill.status.toUpperCase() }}
                      </span>
                    </div>
                    <div class="d-flex justify-content-between text-muted" style="font-size: 0.65rem;">
                      <span>{{ bill.description }}</span>
                      <span class="fw-bold text-dark">${{ bill.amount }}</span>
                    </div>
                    <div class="text-muted mt-1" style="font-size: 0.6rem;">
                      Due: {{ bill.due_date }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- APPOINTMENTS CARD -->
              <div v-if="msg.action.action === 'view_appointments' && msg.actionResult" class="mt-2 p-2 bg-white rounded border border-light-subtle shadow-sm text-start">
                <div class="d-flex justify-content-between align-items-center mb-2 pb-1 border-bottom">
                  <span class="fw-bold text-dark" style="font-size: 0.8rem;">Upcoming Visits ({{ msg.actionResult.count || 0 }})</span>
                  <span class="badge bg-primary-subtle text-primary-emphasis" style="font-size: 0.65rem;">Schedule</span>
                </div>
                <div class="appointments-list overflow-y-auto" style="max-height: 120px; font-size: 0.75rem;">
                  <div v-if="!msg.actionResult.appointments || msg.actionResult.appointments.length === 0" class="text-muted text-center py-1">No upcoming appointments.</div>
                  <div v-else v-for="apt in msg.actionResult.appointments" :key="apt.id" class="p-2 border-bottom border-light mb-1 bg-light rounded-1">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <span class="fw-bold text-dark" style="font-size: 0.7rem;">Dr. {{ apt.doctor_name }}</span>
                      <span :class="['badge', apt.status === 'confirmed' ? 'bg-success-subtle text-success-emphasis' : apt.status === 'pending' ? 'bg-warning-subtle text-warning-emphasis' : 'bg-secondary-subtle text-secondary-emphasis']" style="font-size: 0.6rem;">
                        {{ apt.status.toUpperCase() }}
                      </span>
                    </div>
                    <div class="text-muted" style="font-size: 0.65rem;">
                      <div>📅 {{ apt.day }}, {{ apt.date }}</div>
                      <div>⏰ {{ apt.time }}</div>
                    </div>
                    <div v-if="apt.status !== 'cancelled'" class="mt-1 text-end">
                      <button class="btn btn-xs btn-outline-danger py-0 px-2" style="font-size: 0.55rem; line-height: 1.2;" @click="sendMessage('Cancel appointment #' + apt.id)">
                        Cancel
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- DOCTORS CARD -->
              <div v-if="msg.action.action === 'search_doctors' && msg.actionResult" class="mt-2 p-2 bg-white rounded border border-light-subtle shadow-sm text-start">
                <div class="d-flex justify-content-between align-items-center mb-2 pb-1 border-bottom">
                  <span class="fw-bold text-dark" style="font-size: 0.8rem;">Available Doctors ({{ msg.actionResult.count || 0 }})</span>
                  <span class="badge bg-info-subtle text-info-emphasis" style="font-size: 0.65rem;">Directory</span>
                </div>
                <div class="doctors-list overflow-y-auto" style="max-height: 140px; font-size: 0.75rem;">
                  <div v-if="!msg.actionResult.doctors || msg.actionResult.doctors.length === 0" class="text-muted text-center py-1">No doctors found.</div>
                  <div v-else v-for="doc in msg.actionResult.doctors" :key="doc.id" class="p-2 border-bottom border-light mb-1 bg-light rounded-1">
                    <div class="d-flex justify-content-between align-items-start mb-1">
                      <div>
                        <span class="fw-bold text-primary" style="font-size: 0.75rem;">Dr. {{ doc.name }}</span>
                        <div class="text-muted" style="font-size: 0.6rem;">{{ doc.specialization }} ({{ doc.department }})</div>
                      </div>
                      <span :class="['badge', doc.availability === 'Available' ? 'bg-success-subtle text-success-emphasis' : 'bg-secondary-subtle text-secondary-emphasis']" style="font-size: 0.55rem;">
                        {{ doc.availability }}
                      </span>
                    </div>
                    <div class="d-flex gap-1 justify-content-end mt-1">
                      <button class="btn btn-xs btn-primary py-0 px-2" style="font-size: 0.55rem; line-height: 1.2;" @click="sendMessage('Book appointment with Dr. ' + doc.name)">
                        Book
                      </button>
                      <button class="btn btn-xs btn-outline-secondary py-0 px-2" style="font-size: 0.55rem; line-height: 1.2;" @click="sendMessage('Check availability for Dr. ' + doc.name)">
                        Slots
                      </button>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

        <div v-if="isLoading" class="message bot">
          <div class="message-content">Typing...</div>
        </div>

        <!-- Safety Spacer for premium scrolling -->
        <div class="chat-spacer pb-3" style="height: 15px;"></div>
      </div>

      <div class="card-footer p-2">
        <div class="input-group">
          <button class="btn btn-outline-secondary" @click="toggleVoice" :class="{ 'text-danger': isListening }">
            🎤
          </button>

          <input 
            v-model="userInput"
            @keyup.enter="sendMessage"
            type="text"
            class="form-control"
            placeholder="Type a message..."
          >

          <button class="btn btn-primary" @click="sendMessage">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, nextTick, onMounted } from 'vue';
import { useStore } from 'vuex';
import api from '@/services/api';

const store = useStore();
const isOpen = ref(false);
const messages = ref([
  { id: 1, sender: 'bot', text: 'Hi, I’m FalcoVita AI. I can help you manage appointments, patient history, records, doctors, and more - based on your role.' }
]);

const userInput = ref('');
const isLoading = ref(false);
const chatContainer = ref(null);
const isListening = ref(false);
const isSpeaking = ref(false);

/* ---------------------------------------------------------------------
   SAFE HISTORY LOADER → does NOT endlessly reload when 401 happens
--------------------------------------------------------------------- */
onMounted(async () => {
  // Check if store has currentUser. If not, don't fetch history.
  // This prevents 401 loop if user is not logged in.
  if (!store.getters.currentUser) {
    return;
  }

  try {
    const res = await api.get('/chatbot/history?limit=20');

    // If backend returns 401 despite frontend check, stop.
    if (res.status === 401) return;

    if (res.data?.messages) {
      res.data.messages.forEach(m => {
        const action = m.action_data ? JSON.parse(m.action_data) : null;
        const msg = {
          id: Date.now() + Math.random(),
          sender: m.role === 'assistant' ? 'bot' : 'user',
          text: m.content,
          action: action,
          actionResult: null,
          actionLoading: false,
          actionError: null
        };
        messages.value.push(msg);

        // Auto-execute display-only actions
        if (action && ['get_billing_info', 'view_appointments', 'search_doctors'].includes(action.action)) {
          autoExecuteAction(msg);
        }
      });
    }
  } catch (e) {
    // Silent fail on 401 to avoid console spam
    if (e.response?.status !== 401) {
        console.warn("History load failed:", e);
    }
  }

  scrollToBottom();
});

/* ---------------------------------------------------------------------
   Chat Toggle
--------------------------------------------------------------------- */
const toggleChat = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) scrollToBottom();
};

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;

      // Delayed adjust scrolls to account for reactive elements finishing layout/fonts
      setTimeout(() => {
        if (chatContainer.value) {
          chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
        }
      }, 80);

      setTimeout(() => {
        if (chatContainer.value) {
          chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
        }
      }, 250);
    }
  });
};

/* ---------------------------------------------------------------------
   Auto Execute Display Actions
--------------------------------------------------------------------- */
const autoExecuteAction = async (msg) => {
  if (!msg.action) return;
  msg.actionLoading = true;
  msg.actionError = null;

  try {
    const res = await api.post('/chatbot/execute_action', {
      action: msg.action.action,
      data: msg.action.data
    });
    msg.actionResult = res.data.result;
  } catch (error) {
    console.error("Auto-execute action failed:", error);
    msg.actionError = error.response?.data?.message || "Failed to load information.";
  } finally {
    msg.actionLoading = false;
    scrollToBottom();
  }
};

/* ---------------------------------------------------------------------
   Send Message - FIXED URL + SAFE TEXT HANDLING
--------------------------------------------------------------------- */
const sendMessage = async (forcedText = null) => {
  let text = "";
  
  // If called from a button click/event, forcedText is an Event object.
  // We should treat that as "no forced text" and use userInput.
  if (forcedText && typeof forcedText === 'string') {
      text = forcedText;
  } else {
      text = userInput.value;
  }

  // Double check robustness
  if (typeof text !== "string") text = String(text);

  text = text.trim();
  if (!text) return;

  messages.value.push({ id: Date.now(), sender: 'user', text });
  userInput.value = '';
  scrollToBottom();
  isLoading.value = true;

  try {
    const response = await api.post('/chatbot/message', { message: text });

    const botMsg = {
      id: Date.now() + 1,
      sender: 'bot',
      text: response.data.text,
      action: response.data.action || null,
      actionResult: null,
      actionLoading: false,
      actionError: null
    };

    messages.value.push(botMsg);

    // Auto-execute if it's a data display action
    if (botMsg.action && ['get_billing_info', 'view_appointments', 'search_doctors'].includes(botMsg.action.action)) {
      await autoExecuteAction(botMsg);
    }

  } catch (error) {
    let msg = "I'm sorry, I encountered a server error.";
    if (error?.response?.status === 401) msg = "You must be logged in to use the chatbot.";

    messages.value.push({ id: Date.now() + 1, sender: 'bot', text: msg });
  }

  isLoading.value = false;
  scrollToBottom();
};

/* ---------------------------------------------------------------------
   EXECUTE ACTION → FIXED URL
--------------------------------------------------------------------- */
const handleAction = async (action) => {

  try {
    const res = await api.post('/chatbot/execute_action', {
      action: action.action,
      data: action.data
    });

    messages.value.push({
      id: Date.now(),
      sender: 'bot',
      text: "Done! ✔️\n" + JSON.stringify(res.data.result, null, 2)
    });

  } catch (e) {
    messages.value.push({
      id: Date.now(),
      sender: 'bot',
      text: "Action failed. Please try again."
    });
  }

  scrollToBottom();
};

/* ---------------------------------------------------------------------
   Slot Picker (intact)
--------------------------------------------------------------------- */
const chooseSlot = (slot, action) => {
  sendMessage(`Book appointment with doctor ${action.data.doctor_id} on ${action.data.date} at ${slot}`);
};

/* ---------------------------------------------------------------------
   Voice Input (unchanged)
--------------------------------------------------------------------- */
const toggleVoice = () => {
  if (!('webkitSpeechRecognition' in window)) {
    alert("Voice not supported.");
    return;
  }

  if (isListening.value) {
    isListening.value = false;
    return;
  }

  const rec = new window.webkitSpeechRecognition();
  rec.lang = 'en-US';
  rec.maxAlternatives = 1;

  rec.start();
  isListening.value = true;

  rec.onresult = (e) => {
    userInput.value = e.results[0][0].transcript;
    isListening.value = false;
  };
  rec.onerror = () => (isListening.value = false);
  rec.onend = () => (isListening.value = false);
};

/* ---------------------------------------------------------------------
   Text To Speech (unchanged)
--------------------------------------------------------------------- */
const toggleSpeech = () => {
  if (!("speechSynthesis" in window)) return;

  if (isSpeaking.value) {
    window.speechSynthesis.cancel();
    isSpeaking.value = false;
    return;
  }

  const last = [...messages.value].reverse().find(m => m.sender === "bot");
  if (last) {
    const u = new SpeechSynthesisUtterance(last.text);
    u.onend = () => (isSpeaking.value = false);
    isSpeaking.value = true;
    window.speechSynthesis.speak(u);
  }
};
</script>



<style scoped>
/* YOUR ORIGINAL STYLING - UNTOUCHED */
.chatbot-wrapper {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  font-family: 'Inter', sans-serif;
}

.chatbot-toggle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0d6efd, #0a58ca);
  color: white;
  border: none;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  transition: transform 0.2s;
}

.chatbot-toggle:hover {
  transform: scale(1.05);
}

.chatbot-window {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 350px;
  height: 500px;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  overflow: hidden;
  background: white;
}

.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #f8f9fa;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.message {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
  align-items: flex-end;
}

.message.bot {
  align-self: flex-start;
  align-items: flex-start;
}

.message-content {
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 0.95rem;
  line-height: 1.4;
}

.message.user .message-content {
  background: #0d6efd;
  color: white;
  border-bottom-right-radius: 2px;
}

.message.bot .message-content {
  background: #e9ecef;
  color: #212529;
  border-bottom-left-radius: 2px;
}
</style>
