import logging
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

logger = logging.getLogger("celery")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project", broker=f"redis://{settings.REDIS_HOST}:6379/1")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# this allows you to schedule items in the Django admin.
app.conf.beat_scheduler = "django_celery_beat.schedulers.DatabaseScheduler"


@app.task(bind=True)
def debug_task(self):
    logger.debug(f"Request: {repr(self.request)}")


# Default tasks
app.conf.beat_schedule = {
    "sync_all": {"task": "sync.tasks.sync_all_projects", "schedule": crontab(minute=0, hour=2), "args": tuple()}
}
