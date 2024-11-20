from django.db import models
from django.core.exceptions import ValidationError
from menu.models import Product
from django.contrib.auth.models import User

# 建立你的模型
class Order(models.Model):
    """
    訂單模型，儲存訂單基本資訊及其狀態
    """
    STATUS_CHOICES = [
        ('PENDING', '待處理'),
        ('PREPARING', '準備中'),
        ('SERVED', '已送達'),
        ('COMPLETED', '已完成'),
        ('CANCELLED', '已取消'),
    ]
    order_number = models.AutoField(primary_key=True, verbose_name="訂單號碼")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用戶", default=1)  # 設置默認值
    table = models.IntegerField(choices=[(i, f"桌號 {i}") for i in range(1, 6)], verbose_name="餐桌")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', verbose_name="訂單狀態")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    def __str__(self):
        return f"訂單 #{self.order_number} - 餐桌 {self.table}"

    def total_price(self):
        """
        計算訂單的總價
        """
        return sum(item.total_price for item in self.items.all())

    class Meta:
        verbose_name = "訂單"
        verbose_name_plural = "訂單管理"

class OrderItem(models.Model):
    """
    訂單項目模型，儲存每筆訂單的具體菜單項目與數量
    """
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE, verbose_name="訂單")
    menu_item = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="菜單項目")
    quantity = models.PositiveIntegerField(default=1, verbose_name="數量")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="項目總價")

    def save(self, *args, **kwargs):
        """
        計算總價
        """
        self.clean()
        self.total_price = self.quantity * self.menu_item.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

    class Meta:
        verbose_name = "訂單項目"
        verbose_name_plural = "訂單項目管理"