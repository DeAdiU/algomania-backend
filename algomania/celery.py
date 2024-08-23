# myproject/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'algomania.settings')

app = Celery('algomania')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'call-drf-endpoint-every-hour': {
        'task': 'myapp.tasks.call_drf_endpoint',
        'schedule': crontab(minute=0, hour='*'),  # Runs every hour at minute 0
    },
}

app.conf.timezone = 'UTC'