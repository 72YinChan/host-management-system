import json

from django.http import JsonResponse
from django.views.generic import View
from django.utils import timezone

from .models import City, IDC, Host
from host_management_system.utils import check_need_params
from .tasks import ping_host_task


class CityListView(View):
    def get(self, request):
        data = list(City.objects.filter(is_deleted=False).values("id", "name", "code"))
        return JsonResponse({"code": 0, "msg": "success", "data": data})

    def post(self, request):
        body = json.loads(request.body.decode())

        # 判断参数合法性
        need_params = ["name", "code"]
        miss_params = check_need_params(body, need_params)
        if miss_params:
            return JsonResponse({"code": 1, "msg": f"缺少必填参数: {', '.join(miss_params)}"})
        name = body.get("name")
        code = body.get("code").lower()

        # 判断是否已存在
        item = City.objects.filter(name=name, code=code).values("id", "is_deleted").first()
        if item:
            if item.get("is_deleted"):
                City.objects.filter(name=name, code=code).update(is_deleted=False, updated_at=timezone.now())
                return JsonResponse({"code": 0, "msg": "success"})
            else:
                return JsonResponse({"code": 2, "msg": "已存在相同的城市信息"})

        City.objects.create(name=name, code=code)
        return JsonResponse({"code": 0, "msg": "success"})


class CityDetailView(View):
    def get(self, request, pk):
        data = City.objects.filter(id=pk, is_deleted=False).values("id", "name", "code").first()
        if data:
            return JsonResponse({"code": 0, "msg": "success", "data": data})
        else:
            return JsonResponse({"code": 1, "msg": "不存在该城市"})

    def put(self, request, pk):
        body = json.loads(request.body.decode())

        # 判断参数合法性
        need_params = ["name", "code"]
        miss_params = check_need_params(body, need_params)
        if miss_params:
            return JsonResponse({"code": 1, "msg": f"缺少必填参数: {', '.join(miss_params)}"})

        # 判断是否已存在
        item = City.objects.filter(id=pk, is_deleted=False).values("id").first()
        if item is None:
            return JsonResponse({"code": 1, "msg": "不存在该城市"})

        City.objects.filter(id=pk, is_deleted=False).update(**body, updated_at=timezone.now())
        return JsonResponse({"code": 0, "msg": "success"})

    def delete(self, request, pk):
        # 判断是否已存在
        item = City.objects.filter(id=pk, is_deleted=False).values("id").first()
        if item is None:
            return JsonResponse({"code": 1, "msg": "不存在该城市"})

        City.objects.filter(id=pk).update(is_deleted=True, deleted_at=timezone.now(), updated_at=timezone.now())
        return JsonResponse({"code": 0, "msg": "success"})


class IDCListView(View):
    def get(self, request):
        data = list(IDC.objects.filter(is_deleted=False).values(
            "id", "name", "code", "city_id", "address", "contact", "phone"))
        return JsonResponse({"code": 0, "msg": "success", "data": data})

    def post(self, request):
        body = json.loads(request.body.decode())

        # 判断参数合法性
        need_params = ["name", "code", "city_id", "address", "contact", "phone"]
        miss_params = check_need_params(body, need_params)
        if miss_params:
            return JsonResponse({"code": 1, "msg": f"缺少必填参数: {', '.join(miss_params)}"})
        name = body.get("name")
        code = body.get("code").lower()
        city_id = body.get("city_id")
        address = body.get("address")
        contact = body.get("contact")
        phone = body.get("phone")

        # 判断是否已存在
        item = IDC.objects.filter(name=name, code=code, city_id=city_id).values("id", "is_deleted").first()
        if item:
            if item.get("is_deleted"):
                IDC.objects.filter(name=name, code=code, city_id=city_id).update(
                    address=address, contact=contact, phone=phone, is_deleted=False, updated_at=timezone.now())
                return JsonResponse({"code": 0, "msg": "success"})
            else:
                return JsonResponse({"code": 2, "msg": "已存在相同的机房信息"})

        IDC.objects.create(name=name, code=code, city_id=city_id, address=address, contact=contact, phone=phone)
        return JsonResponse({"code": 0, "msg": "success"})


class IDCDetailView(View):
    def get(self, request, pk):
        data = IDC.objects.filter(id=pk, is_deleted=False).values(
            "id", "name", "code", "city_id", "address", "contact", "phone").first()
        if data:
            return JsonResponse({"code": 0, "msg": "success", "data": data})
        else:
            return JsonResponse({"code": 1, "msg": "不存在该机房"})

    def put(self, request, pk):
        body = json.loads(request.body.decode())

        # 判断参数合法性
        need_params = ["name", "code", "city_id", "address", "contact", "phone"]
        miss_params = check_need_params(body, need_params)
        if miss_params:
            return JsonResponse({"code": 1, "msg": f"缺少必填参数: {', '.join(miss_params)}"})

        # 判断是否已存在
        item = IDC.objects.filter(id=pk, is_deleted=False).values("id").first()
        if item is None:
            return JsonResponse({"code": 1, "msg": "不存在该机房"})

        IDC.objects.filter(id=pk, is_deleted=False).update(**body, updated_at=timezone.now())
        return JsonResponse({"code": 0, "msg": "success"})

    def delete(self, request, pk):
        # 判断是否已存在
        item = IDC.objects.filter(id=pk, is_deleted=False).values("id").first()
        if item is None:
            return JsonResponse({"code": 1, "msg": "不存在该机房"})

        IDC.objects.filter(id=pk).update(is_deleted=True, deleted_at=timezone.now(), updated_at=timezone.now())
        return JsonResponse({"code": 0, "msg": "success"})


class HostListView(View):
    def get(self, request):
        data = list(Host.objects.filter(is_deleted=False).values(
            "id", "hostname", "ip_address", "city_id", "idc_id", "status"))
        return JsonResponse({"code": 0, "msg": "success", "data": data})

    def post(self, request):
        body = json.loads(request.body.decode())

        # 判断参数合法性
        need_params = ["hostname", "ip_address", "city_id", "idc_id", "status"]
        miss_params = check_need_params(body, need_params)
        if miss_params:
            return JsonResponse({"code": 1, "msg": f"缺少必填参数: {', '.join(miss_params)}"})
        hostname = body.get("hostname")
        ip_address = body.get("ip_address")
        city_id = body.get("city_id")
        idc_id = body.get("idc_id")
        status = body.get("status")

        # 判断是否已存在
        item = Host.objects.filter(hostname=hostname, city_id=city_id, idc_id=idc_id).values("id", "is_deleted").first()
        if item:
            if item.get("is_deleted"):
                Host.objects.filter(hostname=hostname, city_id=city_id, idc_id=idc_id).update(
                    is_deleted=False, updated_at=timezone.now())
                return JsonResponse({"code": 0, "msg": "success"})
            else:
                return JsonResponse({"code": 2, "msg": "已存在相同的主机信息"})

        Host.objects.create(hostname=hostname, ip_address=ip_address, city_id=city_id, idc_id=idc_id, status=status)
        return JsonResponse({"code": 0, "msg": "success"})


class HostDetailView(View):
    def get(self, request, pk):
        data = Host.objects.filter(id=pk, is_deleted=False).values(
            "id", "hostname", "ip_address", "city_id", "idc_id", "status").first()
        if data:
            return JsonResponse({"code": 0, "msg": "success", "data": data})
        else:
            return JsonResponse({"code": 1, "msg": "不存在该主机"})

    def put(self, request, pk):
        body = json.loads(request.body.decode())

        # 判断参数合法性
        need_params = ["hostname", "ip_address", "city_id", "idc_id", "status"]
        miss_params = check_need_params(body, need_params)
        if miss_params:
            return JsonResponse({"code": 1, "msg": f"缺少必填参数: {', '.join(miss_params)}"})

        # 判断是否已存在
        item = Host.objects.filter(id=pk, is_deleted=False).values("id").first()
        if item is None:
            return JsonResponse({"code": 1, "msg": "不存在该主机"})

        Host.objects.filter(id=pk, is_deleted=False).update(**body, updated_at=timezone.now())
        return JsonResponse({"code": 0, "msg": "success"})

    def delete(self, request, pk):
        # 判断是否已存在
        item = Host.objects.filter(id=pk, is_deleted=False).values("id").first()
        if item is None:
            return JsonResponse({"code": 1, "msg": "不存在该主机"})

        Host.objects.filter(id=pk).update(is_deleted=True, deleted_at=timezone.now(), updated_at=timezone.now())
        return JsonResponse({"code": 0, "msg": "success"})


def host_ping_api(request, pk):
    """探测主机是否 ping 可达接口"""
    item = Host.objects.filter(id=pk, is_deleted=False).values_list("ip_address").first()
    if item is not None:
        ip_address = item[0]
        ping_host_task.delay(pk, ip_address)
        return JsonResponse({"code": 0, "msg": "success"})
    else:
        return JsonResponse({"code": 1, "msg": "不存在该主机"})
