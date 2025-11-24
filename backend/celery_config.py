from celery import Celery
from celery.schedules import crontab
import os

def make_celery(app_name=__name__):
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    celery = Celery(
        app_name,
        broker=redis_url,
        backend=redis_url
    )
    
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )
    
    return celery

celery_app = make_celery('hospital_management')

# Configure periodic tasks
celery_app.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'backend.tasks.send_daily_reminders',
        'schedule': crontab(hour=8, minute=0),  # Every day at 8 AM
    },
    'send-monthly-reports': {
        'task': 'backend.tasks.send_monthly_reports',
        'schedule': crontab(day_of_month=1, hour=9, minute=0),  # 1st of every month at 9 AM
    },
}