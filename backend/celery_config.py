from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

def make_celery(app_name=__name__):
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    celery = Celery(
        app_name,
        broker=redis_url,
        backend=redis_url,
        include=['backend.tasks']
    )
    
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        worker_send_task_events=False,  # Disable task events to reduce noise
        worker_heartbeat=30000,  # Heartbeat every 30 seconds instead of 2
    )
    
    return celery

celery_app = make_celery('hospital_management')

# Configure periodic tasks
celery_app.conf.beat_schedule = {
    'send-test-google-chat': {
        'task': 'backend.tasks.send_test_google_chat',
        'schedule': 20.0,  # Every 20 seconds (TEST)
    },
    'send-daily-reminders': {
        'task': 'backend.tasks.send_daily_reminders',
        'schedule': 20.0,  # Every 20 seconds (for testing)
    },
    'send-monthly-reports': {
        'task': 'backend.tasks.send_monthly_reports',
        # 'schedule': crontab(day_of_month=0, hour=0, minute=1),  # 1st of every month at 9 AM
        'schedule': 60.0,

    },
}