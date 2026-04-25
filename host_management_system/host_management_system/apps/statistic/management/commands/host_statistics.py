from django.core.management import BaseCommand
from django.db.models import Count

from host_management.models import Host
from statistic.models import HostStatistics


class Command(BaseCommand):
    """按城市和机房维度统计主机数量"""
    def add_arguments(self, parser):
        parser.add_argument("--batch-size", dest='batch_size', type=int, default=1000)

    def handle(self, *args, **options):
        batch_size = options["batch_size"]

        city_idc2data = {}

        city_idc_host_count = Host.objects.values("city_id", "idc_id").annotate(total=Count("id"))
        for item in city_idc_host_count:
            city_id = item.get("city_id")
            idc_id = item.get("idc_id")
            host_count = item.get("total")
            city_idc = f"{city_id}:{idc_id}"
            if city_idc not in city_idc2data:
                city_idc2data[city_idc] = {}
            city_idc2data[city_idc]["host_count"] = host_count

        city_idc_active_count = Host.objects.filter(
            status="active").values("city_id", "idc_id").annotate(total=Count("id"))
        for item in city_idc_active_count:
            city_id = item.get("city_id")
            idc_id = item.get("idc_id")
            active_count = item.get("total")
            city_idc = f"{city_id}:{idc_id}"
            if city_idc not in city_idc2data:
                city_idc2data[city_idc] = {}
            city_idc2data[city_idc]["active_count"] = active_count

        city_idc_inactive_count = Host.objects.filter(
            status="inactive").values("city_id", "idc_id").annotate(total=Count("id"))
        for item in city_idc_inactive_count:
            city_id = item.get("city_id")
            idc_id = item.get("idc_id")
            inactive_count = item.get("total")
            city_idc = f"{city_id}:{idc_id}"
            if city_idc not in city_idc2data:
                city_idc2data[city_idc] = {}
            city_idc2data[city_idc]["inactive_count"] = inactive_count

        host_statistic_objs = []
        for city_idc, data in city_idc2data.items():
            city_id, idc_id = city_idc.split(":")
            city_id = int(city_id)
            idc_id = int(idc_id)
            host_statistic_objs.append(HostStatistics(city_id=city_id, idc_id=idc_id, **data))

        HostStatistics.objects.bulk_create(host_statistic_objs, batch_size=batch_size)
