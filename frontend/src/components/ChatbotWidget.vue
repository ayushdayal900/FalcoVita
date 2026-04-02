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
                  class="btn btn-sm btn-outline-secondary"
                  @click="sendMessage(opt)">
                  {{ opt }}
                </button>
              </div>

              <!-- ESCALATION -->
              <div v-if="msg.action.action === 'escalate_to_human'" class="alert alert-warning p-2 mt-2">
                <strong>Support ticket created</strong><br>
                A staff member will contact you shortly.
              </div>

            </div>
          </div>
        </div>

        <div v-if="isLoading" class="message bot">
          <div class="message-content">Typing...</div>
        </div>
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
        messages.value.push({
          id: Date.now() + Math.random(),
          sender: m.role === 'assistant' ? 'bot' : 'user',
          text: m.content,
          action: m.action_data ? JSON.parse(m.action_data) : null
        });
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
    }
  });
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

    messages.value.push({
      id: Date.now() + 1,
      sender: 'bot',
      text: response.data.text,
      action: response.data.action || null
    });

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
