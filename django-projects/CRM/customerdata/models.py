from django.db import models

# 建立 Record 模型
class Record(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="名字")  # 名字欄位
    last_name = models.CharField(max_length=30, verbose_name="姓氏")  # 姓氏欄位
    email = models.EmailField(max_length=100, verbose_name="電子郵件")  # 電子郵件欄位
    phone = models.CharField(max_length=15, verbose_name="電話號碼")  # 電話號碼欄位
    address = models.CharField(max_length=100, verbose_name="地址", blank=True, null=True)  # 地址欄位
    city = models.CharField(max_length=50, verbose_name="城市", blank=True, null=True)  # 城市欄位
    company = models.CharField(max_length=50, verbose_name="公司", blank=True, null=True)  # 公司欄位
    position = models.CharField(max_length=50, verbose_name="職位", blank=True, null=True)  # 職位欄位
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")  # 創建時間欄位
    remark = models.TextField(verbose_name="備註", blank=True, null=True)  # 備註欄位

    def __str__(self):  # 定義 __str__ 方法，返回該記錄的姓名
        return f"{self.first_name} {self.last_name}"  # 返回格式化的姓名，當物件被轉為字串時顯示
