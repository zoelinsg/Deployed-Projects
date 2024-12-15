from django.db import models
from django.contrib.auth.models import User

# 相片模型
class Photo(models.Model):
    title = models.CharField(max_length=100)  # 相片標題
    description = models.TextField(blank=True)  # 相片描述，可空白
    image = models.ImageField(upload_to='photos')  # 相片檔案
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # 相片作者
    album = models.ForeignKey('Album', on_delete=models.CASCADE)  # 相簿
    location = models.CharField(max_length=100, blank=True)  # 相片拍攝地點，可空白
    category = models.ForeignKey('Category', on_delete=models.CASCADE)  # 相片類別
    tags = models.ManyToManyField('Tag', blank=True)  # 相片標籤，可多選
    created_at = models.DateTimeField(auto_now_add=True)  # 創建時間
    updated_at = models.DateTimeField(auto_now=True)  # 更新時間

    def __str__(self):
        return self.title

# 相片類別模型
class Category(models.Model):
    name = models.CharField(max_length=100)  # 類別名稱

    def __str__(self):
        return self.name

# 相簿模型
class Album(models.Model):
    name = models.CharField(max_length=100)  # 相簿名稱
    description = models.TextField(blank=True)  # 相簿描述，可空白
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # 相簿作者
    created_at = models.DateTimeField(auto_now_add=True)  # 創建時間
    updated_at = models.DateTimeField(auto_now=True)  # 更新時間

    def __str__(self):
        return self.name

# 標籤模型
class Tag(models.Model):
    name = models.CharField(max_length=100)  # 標籤名稱

    def __str__(self):
        return self.name