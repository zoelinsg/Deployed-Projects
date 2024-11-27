from django.db import models
from django.contrib.auth.models import User
from products.models import Product  # 從產品 app 中引用產品模型

class Cart(models.Model):
    """
    購物車模型，包含用戶的購物車資訊
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用戶")

    def __str__(self):
        return f"購物車 - 用戶 {self.user.username}"

    class Meta:
        verbose_name = "購物車"
        verbose_name_plural = "購物車"  # 複數形式

class CartItem(models.Model):
    """
    購物車項目模型，包含購物車中的產品資訊
    """
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE, verbose_name="購物車")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="產品")
    quantity = models.PositiveIntegerField(default=1, verbose_name="數量")

    def __str__(self):
        return f"購物車 {self.cart.id} - 產品 {self.product.name}"

    class Meta:
        verbose_name = "購物車項目"
        verbose_name_plural = "購物車項目"  # 複數形式

class Order(models.Model):
    """
    訂單模型，包含每個訂單的資訊
    """
    STATUS_CHOICES = [
        ('pending', '未支付'),
        ('processing', '準備中'),
        ('shipped', '已出貨'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用戶")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="訂單狀態")
    is_paid = models.BooleanField(default=False, verbose_name="是否已支付")
    address = models.CharField(max_length=255, default='未提供', verbose_name="配送地址")
    phone = models.CharField(max_length=20, default='未提供', verbose_name="聯絡電話")

    def __str__(self):
        return f"訂單 {self.id} - 用戶 {self.user.username}"

    class Meta:
        verbose_name = "訂單"
        verbose_name_plural = "訂單"  # 複數形式

class OrderItem(models.Model):
    """
    訂單項目模型，包含每個訂單中的產品資訊
    """
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE, verbose_name="訂單")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="產品")
    quantity = models.PositiveIntegerField(default=1, verbose_name="數量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="價格")

    def __str__(self):
        return f"訂單 {self.order.id} - 產品 {self.product.name}"

    class Meta:
        verbose_name = "訂單項目"
        verbose_name_plural = "訂單項目"  # 複數形式