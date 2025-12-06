# FalcoVita - Hospital Management System V2

FalcoVita is a comprehensive **Hospital Management System (HMS)** designed to streamline healthcare operations. It serves as a centralized platform for managing patients, doctors, appointments, and medical records, improving efficiency and patient care.

## Key Features

*   **Role-Based Access**: Distinct portals for **Admins**, **Doctors**, and **Patients**.
*   **Appointment Management**: Full lifecycle handling (booking, rescheduling, cancellation) with availability tracking.
*   **Medical Records**: Digital management of patient history, diagnoses, and prescriptions.
*   **Admin Dashboard**: Analytics on hospital stats, doctor performance, and patient demographics.
*   **Data Export**: Capability to export patient history and appointment logs.
*   **Automated Reminders**: Daily appointment reminders sent via **Google Chat Webhooks** using **Celery Beat**.
*   **Email Testing**: **Mailhog** integration for capturing and viewing dummy emails during development.

## Technology Stack

### Frontend
*   **Vue.js 3**: Progressive JavaScript framework.
*   **Vite**: Next-generation frontend tooling.
*   **Bootstrap 5**: Responsive design framework.
*   **Vuex**: State management pattern + library.
*   **Chart.js**: Simple yet flexible JavaScript charting for designers & developers.

### Backend
*   **Python (Flask)**: Micro web framework for Python.
*   **SQLite**: C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
*   **Redis**: In-memory data structure store, used as a database, cache, and message broker.
*   **Celery**: Distributed task queue.
*   **Flask-Security-Too**: Quick and simple security for Flask applications.
*   **Flask-RESTful**: Extension for building REST APIs.

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites
*   Python 3.8+
*   Node.js & npm
*   Redis Server (must be running for Celery)
*   [Mailhog](https://github.com/mailhog/MailHog) (for email testing)

### Configuration

1.  **Environment Variables**:
    Create a `.env` file in the root directory (copy from `.env.example`).
    -   `GOOGLE_CHAT_WEBHOOK_URL`: Your Google Chat webhook URL for notifications.
    -   `SMTP_SERVER`: `localhost` (default for Mailhog)
    -   `SMTP_PORT`: `1025` (default for Mailhog)

### Backend Setup

1.  **Navigate to the project root.**
2.  **Install dependencies:**
    ```bash
    pip install -r backend/requirements.txt
    ```
3.  **Start Redis Server:**
    Ensure your Redis server is running (usually `redis-server`).
4.  **Start Mailhog:**
    Download and run the Mailhog executable.
    -   **SMTP Server**: `localhost:1025`
    -   **Web UI**: `http://localhost:8025`
5.  **Start Celery Worker:**
    ```bash
    celery -A backend.app.celery worker --loglevel=info
    ```
6.  **Start Celery Beat (for scheduled tasks):**
    ```bash
    celery -A backend.app.celery beat --loglevel=info
    ```
    *This scheduler triggers daily reminders via Google Chat or Email.*
7.  **Run the Flask Application:**
    ```bash
    python -m backend.app
    ```
    The backend API will be available at `http://localhost:5000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The application will be accessible at `http://localhost:5173` (or the port shown in your terminal).