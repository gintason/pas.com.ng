from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paswebsite.settings")
app = Celery("paswebsite")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task
def debug_task():
    print("Celery is working!")