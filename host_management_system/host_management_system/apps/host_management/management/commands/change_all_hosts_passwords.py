import concurrent.futures as c_futures
import subprocess
import logging
import traceback

from django.core.management.base import BaseCommand
from django.utils import timezone

from host_management.models import Host
from host_management_system.utils import (
    generate_password,
    encrypt_password,
    decrypt_password,
)


logger = logging.getLogger("django")


class Command(BaseCommand):
    """随机修改每台主机密码任务"""
    def add_arguments(self, parser):
        parser.add_argument("--batch-size", dest='batch_size', type=int, default=1000)

    def handle(self, *args, **options):
        batch_size = options["batch_size"]

        host_pks = list(Host.objects.filter(is_deleted=False).values_list("id", flat=True))
        for idx in range(0, len(host_pks), batch_size):
            sub_host_pks = host_pks[idx: idx + batch_size]
            host_objs = list(Host.objects.filter(id__in=sub_host_pks))
            task2host_obj = {}
            with c_futures.ThreadPoolExecutor(max_workers=10) as executor:
                for host_obj in host_objs:
                    old_password = host_obj.password
                    ip_address = host_obj.ip_address
                    task = executor.submit(self.change_host_password, old_password, ip_address)
                    task2host_obj[task] = host_obj

                for task in c_futures.as_completed(task2host_obj):
                    host_obj = task2host_obj[task]
                    try:
                        ret_flag, new_password = task.result()
                        if ret_flag:
                            host_obj.password = encrypt_password(new_password)
                            host_obj.password_changed_at = timezone.now()
                            host_obj.updated_at = timezone.now()
                    except Exception as e:
                        logger.error(f"修改主机({ip_address})密码时发生错误: {e}\n{traceback.format_exc()}")

            Host.objects.bulk_update(host_objs, ["password", "password_changed_at", "updated_at"])

    @staticmethod
    def change_host_password(old_password, ip_address):
        new_password = generate_password()
        cmd = [
            "sshpass", "-p", old_password, "ssh", f"root@{ip_address}",
            f"echo '{old_password}' | sudo -S sh -c 'echo \"root:{new_password}\" | chpasswd'",
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return True, new_password
            else:
                logger.error(f"修改主机({ip_address})密码发生错误: {result.stderr.decode()}")
                return False, None
        except subprocess.TimeoutExpired as e:
            logger.error(f"修改主机({ip_address})密码超时")
            return False, None
        except Exception as e:
            logger.error(f"修改主机({ip_address})密码时发生错误: {e}\n{traceback.format_exc()}")
            return False, None
