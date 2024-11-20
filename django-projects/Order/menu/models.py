from django.db import models

# 建立你的模型
class Category(models.Model):
    """
    類別模型，用於分類菜單項目
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="類別名稱")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "菜單類別"
        verbose_name_plural = "菜單類別"  # 複數形式

class Tag(models.Model):
    """
    標籤模型，用於標記菜單項目
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="標籤名稱")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "標籤"
        verbose_name_plural = "標籤"  # 複數形式

class Product(models.Model):
    """
    菜單項目模型，包含每個餐點的資訊
    """
    name = models.CharField(max_length=100, verbose_name="菜名")
    image = models.ImageField(upload_to='menu_images/', default='menu_images/default.jpg', verbose_name="圖片")
    description = models.TextField(blank=True, verbose_name="描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="價格")
    available = models.BooleanField(default=True, verbose_name="是否可供應")
    category = models.ForeignKey(Category, related_name="menu_items", on_delete=models.SET_NULL, null=True, verbose_name="所屬類別")
    tags = models.ManyToManyField(Tag, blank=True, related_name="menu_items", verbose_name="標籤")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "菜單項目"
        verbose_name_plural = "菜單項目"  # 複數形式

class Cart(models.Model):
    """
    購物車項目模型，暫存客人所選擇的菜單項目
    """
    session_id = models.CharField(max_length=255, verbose_name="Session ID", default='')  # 設置默認值
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="菜單項目")
    quantity = models.PositiveIntegerField(default=1, verbose_name="數量")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間")

    def total_price(self):
        """
        計算購物車項目的總價
        """
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        verbose_name = "購物車"
        verbose_name_plural = "購物車管理"