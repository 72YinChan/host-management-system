import subprocess

from host_management_system.celery import celery_app
from host_management.models import Host


@celery_app.task(bind=True, name="ping_host_task")
def ping_host_task(self, host_pk, ip_address):
    command = ["ping", "-n", "5", ip_address]
    try:
        result = subprocess.run(command, capture_output=True, timeout=5)
        info = result.stdout.decode()
        if "Destination Host Unreachable" in info or "100% packet loss" in info:
            Host.objects.filter(id=host_pk, is_deleted=False).update(status="inactive")
        else:
            Host.objects.filter(id=host_pk, is_deleted=False).update(status="active")
    except subprocess.TimeoutExpired as e:
        Host.objects.filter(id=host_pk, is_deleted=False).update(status="inactive")
