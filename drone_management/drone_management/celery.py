from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drone_management.settings')
celery_app = Celery('drone_management')

# Use Redis as the message broker
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.conf.broker_transport_options = {'visibility_timeout': 3600}

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()

#For testing purposes, the intervals are in minutes less than 30
celery_app.conf.beat_schedule = {
    'battery-use-and-log': {
        'task': 'drones_api.tasks.battery_use_and_log',
        'schedule': crontab(minute='*/1'),  # Run every 1 minute
    },
    'recharge-batteries': {
        'task': 'drones_api.tasks.recharge_batteries',
        'schedule': crontab(minute='*/20'),# Run every 10 minutes
    },
    'change-drone-state': { # This won't run if the drone is idle
        'task': 'drones_api.tasks.change_drone_state',
        'schedule': crontab(minute='*/1'),# Run every 1 minute
    },
}