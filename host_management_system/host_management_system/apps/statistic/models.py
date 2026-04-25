from django.db import models


class HostStatistics(models.Model):
    """主机统计模型"""
    city_id = models.IntegerField(null=False, verbose_name="城市ID")
    idc_id = models.IntegerField(null=False, verbose_name="机房ID")
    host_count = models.IntegerField(default=0, verbose_name="主机数量")
    active_count = models.IntegerField(default=0, verbose_name="活跃主机数量")
    inactive_count = models.IntegerField(default=0, verbose_name="不活跃主机数量")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "host_statistics"
        verbose_name = "主机统计"
        managed = False
