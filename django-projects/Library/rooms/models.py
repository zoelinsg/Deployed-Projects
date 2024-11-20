from django.db import models
from django.contrib.auth.models import User

# 自修室模型
class Room(models.Model):
    name = models.CharField(max_length=255)  # 自修室名稱
    STATUS_CHOICES = [
        ('available', '可借閱'),
        ('in_use', '使用中'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')  # 狀態欄位
    borrowed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # 借閱者
    cancelled = models.BooleanField(default=False)  # 是否取消預約

    def __str__(self):
        return self.name  # 返回自修室名稱作為模型的字串表示