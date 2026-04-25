from django.db import models


class City(models.Model):
    """城市模型"""
    name = models.CharField(max_length=100, null=False, verbose_name="城市名称")
    code = models.CharField(max_length=50, null=False, verbose_name="城市代码")
    is_deleted = models.BooleanField(default=False, null=False, verbose_name="是否删除")
    deleted_at = models.DateTimeField(null=True, verbose_name="删除时间")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cities"
        verbose_name = "城市"
        managed = False


class IDC(models.Model):
    """机房模型"""
    name = models.CharField(max_length=100, null=False, verbose_name="机房名称")
    code = models.CharField(max_length=50, null=False, verbose_name="机房代码")
    city_id = models.IntegerField(null=False, verbose_name="城市 ID")
    address = models.CharField(max_length=200, null=False, verbose_name="机房地址")
    contact = models.CharField(max_length=100, null=False, verbose_name="联系人")
    phone = models.CharField(max_length=20, null=False, verbose_name="联系电话")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    deleted_at = models.DateTimeField(null=True, verbose_name="删除时间")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "idcs"
        verbose_name = "机房"
        managed = False


class Host(models.Model):
    """主机模型"""
    STATUS_CHOICES = [
        ("active", "活跃"),
        ("inactive", "不活跃"),
        ("maintenance", "维护中"),
    ]

    hostname = models.CharField(max_length=100, null=False, verbose_name="主机名")
    ip_address = models.CharField(max_length=15, null=False, verbose_name="IP地址")
    city_id = models.IntegerField(null=False, verbose_name="城市ID")
    idc_id = models.IntegerField(null=False, verbose_name="机房ID")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", null=False, verbose_name="状态")
    password = models.TextField(null=False, verbose_name="密码")
    password_changed_at = models.DateTimeField(auto_now=True, verbose_name="密码更改时间")
    is_deleted = models.BooleanField(default=False, null=False, verbose_name="是否删除")
    deleted_at = models.DateTimeField(null=True, verbose_name="删除时间")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hosts"
        verbose_name = "主机"
        managed = False
