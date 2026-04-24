import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "host_management_system.settings")

celery_app = Celery("host_management")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
