# FalcoVita - Project QA Log

This file contains the questions and answers regarding the FalcoVita Hospital Management System project.

---

### Question 1: Why use Vue.js and Flask instead of the MERN stack?

#### Clear Information
* **Rich AI & RAG Ecosystem**: Python's native support for AI libraries (`google-generativeai`, `openai`, `pinecone`) makes building the FalcoVita AI Chatbot and RAG pipeline straightforward compared to Node.js (Express).
* **Strict Relational Data Integrity**: Hospital management systems deal with highly structured, relational data (e.g., Doctors, Patients, Appointments, and Billing). Using SQLite/SQLAlchemy enforces schema constraints and foreign key relationships out of the box, whereas MongoDB (in MERN) is a non-relational document database where enforcing integrity is more complex.
* **Simplicity & Development Speed**: Flask is extremely lightweight and integrates seamlessly with `Flask-Security-Too` for rapid SPA authentication. Vue.js provides a progressive, easy-to-learn reactive system with clean state management (Vuex) that simplifies dashboard layouts.

#### Short Code Example
Python makes relational modeling and AI integration clean and concise:
```python
# Relational schema enforcement (SQLAlchemy vs NoSQL MongoDB)
class Appointment(BaseModel):
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    
# Clean integration with Google Generative AI in Flask
import google.generativeai as genai
model = genai.GenerativeModel('gemini-pro')
```

#### Brief Explanation
The Vue-Flask stack is preferred for FalcoVita because of Python's robust AI/ML capabilities for powering the RAG chatbot and background services (Celery + Redis). Additionally, hospital data is naturally relational, making SQL schemas and foreign key integrity (via SQLite/SQLAlchemy) a much safer choice than NoSQL databases like MongoDB.


### Question 2: What is Celery and how is it used in this project?

#### Clear Information
* **What is Celery**: Celery is an asynchronous distributed task queue used to run time-consuming tasks in the background, separating them from the main web request-response cycle.
* **Usage in FalcoVita**:
  * **Asynchronous Jobs**: Triggering CSV exports of patient histories (`export_patient_history_csv`) and emailing them so that the frontend doesn't hang waiting for file generation.
  * **Scheduled Reminders (Celery Beat)**: Running daily checks for scheduled appointments and notifying patients via Google Chat Webhooks or MailHog emails (`send_daily_reminders`).
  * **Periodic Reports**: Generating and emailing monthly activity statistics (`send_monthly_reports`) to doctors.

#### Short Code Example
```python
# Task definition (backend/tasks.py)
@celery_app.task(name='backend.tasks.export_patient_history_csv')
def export_patient_history_csv(patient_id):
    # Generates CSV and sends via SMTP email in the background
    ...

# Beat scheduler configuration (backend/celery_config.py)
celery_app.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'backend.tasks.send_daily_reminders',
        'schedule': 20.0,  # Scheduled to run every 20 seconds in development
    }
}
```

#### Brief Explanation
In FalcoVita, Celery is used to offload long-running operations from the main Flask web server. When a user requests a patient history CSV export, Celery processes the report asynchronously. Additionally, the Celery Beat scheduler automatically triggers daily appointment reminders and monthly doctor reports in the background.


### Question 3: Provide all details about how Celery is configured and used in this project.

#### Clear Information
* **Broker & Backend**: Celery uses **Redis** (`redis://localhost:6379/0` on Database 0) as both the message broker (to queue tasks) and the result backend (to store task states).
* **Worker & Beat Execution**:
  * Celery Worker runs via: `python -m celery -A backend.app.celery worker --loglevel=info`
  * Celery Beat Scheduler runs via: `python -m celery -A backend.app.celery beat --loglevel=info`
* **Periodic Schedules (backend/celery_config.py)**:
  * `send-test-google-chat`: Triggers every 20 seconds.
  * `send-daily-reminders`: Triggers every 20 seconds (accelerated for testing).
  * `send-monthly-reports`: Triggers every 60 seconds (accelerated for testing).
* **Task Definitions (backend/tasks.py)**:
  1. **`send_test_google_chat`**: Periodically sends dummy appointment card notifications to a Google Chat Webhook URL (`GOOGLE_CHAT_WEBHOOK_URL`).
  2. **`send_daily_reminders`**: Checks for scheduled appointments for the current day. Sends a rich Google Chat card webhook notification if configured; otherwise, it sends an email to the patient using SMTP (MailHog).
  3. **`send_monthly_reports`**: Compiles previous-month analytics (appointments scheduled, completed, cancelled, and recent diagnoses) and emails an HTML summary report to each doctor.
  4. **`export_patient_history_csv`**: Generates a CSV file of a patient's medical and prescription histories in memory, attaches it to a multipart MIME email, and sends it to the patient.

#### Short Code Example
```python
# Initialization (backend/celery_config.py)
celery_app = Celery(
    'hospital_management',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['backend.tasks']
)

# Daily reminder task utilizing Flask app context (backend/tasks.py)
@celery_app.task(name='backend.tasks.send_daily_reminders')
def send_daily_reminders():
    with app.app_context():  # Bind to SQLAlchemy models
        today = datetime.now(timezone.utc).date()
        appointments = Appointment.query.filter(Appointment.status == 'scheduled').all()
        # Trigger reminders...
```

#### Brief Explanation
Celery in FalcoVita operates as a background task processor that connects to Redis on Database 0. It is configured to run four automated processes: sending Google Chat webhook/SMTP email reminders for daily patient appointments, mailing monthly statistics reports to doctors, running test webhook pings, and exporting patient medical histories to CSV in memory. By binding tasks to the Flask application context, Celery can query SQLAlchemy database models.


### Question 4: What is Redis and how is it used in this project?

#### Clear Information
* **What is Redis**: Redis is an open-source, in-memory key-value store renowned for high-speed read/write performance. It is commonly utilized as a database, cache, and message broker.
* **Usage in FalcoVita**:
  * **Celery Message Broker & Backend (Database 0)**: It hosts the task queues that hold background jobs (such as PDF/CSV generation, daily notifications) before a Celery worker processes them. It also logs the task states.
  * **Application API Caching (Database 1)**: The system utilizes `flask-caching` with the `RedisCache` type to cache high-frequency, read-only API calls (like listings of departments or doctors) for 300 seconds, reducing load on SQLite.

#### Short Code Example
```python
# Configuration settings separating Celery and Cache databases (backend/config.py)
class DevelopmentConfig(BaseConfig):
    # Celery Broker and Backend on Redis Database 0
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    RESULT_BACKEND = "redis://localhost:6379/0"
    
    # Caching on Redis Database 1
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/1"
    CACHE_DEFAULT_TIMEOUT = 300
```

#### Brief Explanation
Redis acts as a key utility store in FalcoVita, separated into two databases: Database 0 manages message routing and task execution logs for Celery, while Database 1 handles API-level caching via Flask-Caching, dramatically lowering database read overhead.


### Question 5: How are OpenAI, RAG, and Pinecone used in this project?

#### Clear Information
* **RAG Pipeline**: Implemented in `RAGService` to supplement chatbot queries with additional information. It injects retrieved knowledge into the LLM context to ensure accurate, context-aware answers.
* **OpenAI (Embeddings)**: Used to convert the user's natural language message into a numeric vector using the `text-embedding-3-small` embedding model.
* **Pinecone (Vector DB)**: Hosts the `falcovita-rag` vector index. It matches the query embedding vector against stored documents to return the top 3 most relevant segments of information.
* **SQL Fallback**: If vector credentials are missing, the service falls back to `_mock_retrieve_context`, which queries the SQLite database directly using role-based filters to extract doctor listings, departments, or appointment counts.

#### Short Code Example
```python
# RAG context retrieval flow (backend/services/rag_service.py)
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("falcovita-rag")

# 1. Generate text embedding vector
emb = openai.embeddings.create(input=query, model="text-embedding-3-small")
vector = emb.data[0].embedding

# 2. Query vector database for context matches
results = index.query(vector=vector, top_k=3, include_metadata=True)
context = "\n".join([match['metadata']['text'] for match in results['matches']])
```

#### Brief Explanation
FalcoVita utilizes a Retrieval-Augmented Generation (RAG) architecture where user queries are vectorized via OpenAI's embedding API. These vectors are then compared inside a Pinecone vector database (`falcovita-rag` index) to fetch relevant hospital documentation. If the external services fail or are missing API keys, the system gracefully falls back to structured SQLite database queries to extract contextual metadata.


### Question 6: How are charts created in this project using Chart.js?

#### Clear Information
* **vue-chartjs Wrapper**: The frontend uses `vue-chartjs` to import native Chart.js components (such as `<Bar />`, `<Pie />`, `<Doughnut />`, `<Line />`, `<Bubble />`, `<Scatter />`) and render them reactively inside Vue templates.
* **Component Registration**: Chart.js elements, scales, controllers, and plugins (e.g., `CategoryScale`, `LinearScale`, `ArcElement`, `BarElement`, `Tooltip`, `Legend`, `ChartDataLabels`) are registered globally or locally using `ChartJS.register()`.
* **Computed Reactive Data**: Chart data is declared using Vue `computed()` properties that map API response reactive objects (e.g., `doctors.value.length`, `patients.value.length`) directly into Chart.js dataset formats.
* **Formatters & Plugins**: The application integrates `chartjs-plugin-datalabels` to render custom annotations (e.g., prefixing unpaid billing values with `$`) and custom tooltips to show review counts next to doctor ratings.

#### Short Code Example
```javascript
// Register and render components (frontend/src/views/AdminCharts.vue)
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Bar } from 'vue-chartjs';

ChartJS.register(CategoryScale, LinearScale, BarElement);

// Dynamic reactive dataset bound to template via computed properties
const doctorsVsPatientsData = computed(() => {
  return {
    labels: ['Doctors', 'Patients'],
    datasets: [{
      backgroundColor: ['#4e73df', '#1cc88a'],
      data: [doctors.value.length, patients.value.length]
    }]
  };
});
```

#### Brief Explanation
FalcoVita implements hospital data charting by embedding `vue-chartjs` wrapper components in Vue views. Core Chart.js utilities are registered, and database values are fed dynamically into computed datasets. Styling options and third-party plugins are applied to control responsiveness, render chart legends, and format labels (such as adding currency symbols or rendering custom hover tooltips).
