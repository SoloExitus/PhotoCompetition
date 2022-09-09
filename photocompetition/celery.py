import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photocompetition.settings')

app = Celery('notification')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'all_user_notifications': {
        'task': 'notices.tasks.send_notification',
        'schedule': 5.0,
    }
}

app.autodiscover_tasks()