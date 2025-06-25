import os
from celery import Celery

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatserver.settings')

app = Celery('chatserver')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Use Redis as broker
app.conf.broker_url = REDIS_URL

app.autodiscover_tasks()
