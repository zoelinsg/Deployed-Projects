from django.db import models

# 建立你的模型
class Category(models.Model):
    """
    類別模型，用於分類產品項目
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="類別名稱")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "類別"
        verbose_name_plural = "類別"  # 複數形式

class Tag(models.Model):
    """
    標籤模型，用於標記產品項目
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="標籤名稱")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "標籤"
        verbose_name_plural = "標籤"  # 複數形式

class Product(models.Model):
    """
    產品項目模型，包含每個商品的資訊
    """
    name = models.CharField(max_length=100, verbose_name="產品名稱")
    image = models.ImageField(upload_to='product_images/', default='product_images/default.jpg', verbose_name="圖片")
    description = models.TextField(blank=True, verbose_name="描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="價格")
    stock = models.PositiveIntegerField(default=0, verbose_name="庫存量")
    category = models.ForeignKey(Category, related_name="menu_items", on_delete=models.SET_NULL, null=True, verbose_name="所屬類別")
    tags = models.ManyToManyField(Tag, blank=True, related_name="menu_items", verbose_name="標籤")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "產品"
        verbose_name_plural = "產品"  # 複數形式