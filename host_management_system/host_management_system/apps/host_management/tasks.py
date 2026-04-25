import subprocess
import logging
import traceback

from host_management_system.celery import celery_app
from host_management.models import Host


logger = logging.getLogger("django")


@celery_app.task(bind=True, name="ping_host_task")
def ping_host_task(self, host_pk, ip_address):
    command = ["ping", "-n", "5", ip_address]
    pingable = True
    try:
        result = subprocess.run(command, capture_output=True, timeout=5)
        info = result.stdout.decode()
        if "Destination Host Unreachable" in info or "100% packet loss" in info:
            logger.error(f"主机({ip_address})不可达")
            pingable = False
    except subprocess.TimeoutExpired as e:
        logger.error(f"ping主机({ip_address})执行超时")
        pingable = False
    except Exception as e:
        logger.error(f"ping主机({ip_address})执行时发生错误: {e}\n{traceback.format_exc()}")
        pingable = False

    if pingable:
        Host.objects.filter(id=host_pk, is_deleted=False).update(status="active")
    else:
        Host.objects.filter(id=host_pk, is_deleted=False).update(status="inactive")


@celery_app.task(bind=True, name="change_all_hosts_passwords_task")
def change_all_hosts_passwords_task(self):
    """随机修改每台主机密码任务"""
    command = ["python", "manage.py", "change_all_hosts_passwords"]
    try:
        result = subprocess.run(command, capture_output=True)
        if result.returncode != 0:
            logger.error(f"执行随机修改每台主机密码任务时发生错误: {result.stderr.decode()}")
    except Exception as e:
        logger.error(f"执行随机修改每台主机密码任务时发生错误: {e}\n{traceback.format_exc()}")
