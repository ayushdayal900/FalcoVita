# FalcoVita Backend Setup

## Prerequisites

- Python 3.8+
- **WSL2** (Windows Subsystem for Linux) for Redis

## 1. Install Dependencies

Run the following command from the root `FalcoVita` directory:

```powershell
pip install -r backend/requirements.txt
```

## 2. Set up Redis (Required for Celery)

Since you are on Windows, we will use WSL to run the Redis server.

1.  Open your WSL terminal (e.g., Ubuntu).
2.  Update packages: `sudo apt update`
3.  Install Redis: `sudo apt install redis-server`
4.  Start Redis: `sudo service redis-server start`

You can verify it's running by typing `redis-cli ping` inside WSL. It should reply `PONG`.

## 3. Run the Application

### Start the Flask API
In your Windows PowerShell/Terminal:

```powershell
# Make sure you are in the FalcoVita directory
$env:FLASK_APP = "backend/app.py"
flask run --debug
```

### Start the Celery Worker
Open a **new** PowerShell window for the background worker:

```powershell
# Windows requires the 'solo' pool or 'eventlet'
celery -A backend.app.celery_app worker --loglevel=info --pool=solo
```

## Troubleshooting

- **"Module not found: celery"**: Ensure you activated your virtual environment if you use one, and ran the `pip install` command above.
- **Redis Connection Error**: Make sure `sudo service redis-server start` was run inside WSL.
