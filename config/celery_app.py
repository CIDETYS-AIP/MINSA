import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("covid19_panama")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
     'autoupdate': {
         'task': 'covid19_panama.autoupdate_module.tasks.autoupdate',
         'schedule': int(settings.AUTOUPDATE_FREQUENCY_IN_SECONDS)
     }
}
