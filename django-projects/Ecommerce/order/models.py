from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# 類別模型，用於分類產品項目
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="類別名稱")  # 類別名稱欄位

    def __str__(self):
        return self.name  # 返回類別名稱作為模型的字串表示

    class Meta:
        verbose_name = "類別"
        verbose_name_plural = "類別"  # 複數形式

# 標籤模型，用於標記產品項目
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="標籤名稱")  # 標籤名稱欄位

    def __str__(self):
        return self.name  # 返回標籤名稱作為模型的字串表示

    class Meta:
        verbose_name = "標籤"
        verbose_name_plural = "標籤"  # 複數形式

# 產品項目模型，包含每個商品的資訊
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="產品名稱")  # 產品名稱欄位
    image = models.ImageField(upload_to='product_images/', default='product_images/default.jpg', verbose_name="圖片")  # 圖片欄位
    description = models.TextField(blank=True, verbose_name="描述")  # 描述欄位
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="價格")  # 價格欄位
    stock = models.PositiveIntegerField(default=0, verbose_name="庫存量")  # 庫存量欄位
    is_sold_out = models.BooleanField(default=False, verbose_name="是否售完")  # 是否售完欄位
    category = models.ForeignKey(Category, related_name="menu_items", on_delete=models.SET_NULL, null=True, verbose_name="所屬類別")  # 所屬類別欄位
    tags = models.ManyToManyField(Tag, blank=True, related_name="menu_items", verbose_name="標籤")  # 標籤欄位

    def __str__(self):
        return self.name  # 返回產品名稱作為模型的字串表示

    def save(self, *args, **kwargs):
        # 如果庫存為0，設置售完為True
        if self.stock == 0:
            self.is_sold_out = True
        else:
            self.is_sold_out = False
        super().save(*args, **kwargs)  # 調用父類的save方法

    class Meta:
        verbose_name = "產品"
        verbose_name_plural = "產品"  # 複數形式

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

    # 不可以買超過庫存量
    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError("購買數量不能超過庫存量")

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

    # 下訂單會扣除庫存
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for item in self.items.all():
            item.product.stock -= item.quantity
            item.product.save()

    # 計算訂單總金額
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

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

    # 計算訂單項目的總金額
    def get_cost(self):
        return self.price * self.quantity