from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

# 書籍模型
class Book(models.Model):
    CATEGORY_CHOICES = [
        ('fiction', '小說'),
        ('non-fiction', '非小說'),
        ('biography', '傳記'),
        ('reference', '參考書'),
        ('other', '其他'),
    ]
    
    STATUS_CHOICES = [
        ('available', '可借閱'),
        ('borrowed', '已借出'),
    ]
    
    title = models.CharField(max_length=255)  # 書名
    cover = models.ImageField(upload_to='covers/', null=True, blank=True, default='covers/default_cover.jpg')  # 書籍圖片，預設為 default_cover.jpg
    author = models.CharField(max_length=255)  # 作者
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)  # 類別欄位
    description = models.TextField()  # 書籍描述
    publication_date = models.DateField()  # 出版日期
    isbn = models.CharField(max_length=13)  # ISBN
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')  # 狀態欄位
    borrowed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # 借閱者
    borrowed_date = models.DateField(null=True, blank=True)  # 借閱日期
    due_date = models.DateField(null=True, blank=True)  # 到期日期
    cancelled_date = models.DateField(null=True, blank=True)  # 取消預約日期

    def save(self, *args, **kwargs):
        if self.borrowed_date and not self.due_date:
            self.due_date = self.borrowed_date + timedelta(days=30)  # 借閱日期和到期日差一個月
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title  # 返回書名作為模型的字串表示

# 借閱歷史模型
class BorrowHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # 連結到書籍模型的外鍵
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 連結到用戶模型的外鍵
    borrowed_date = models.DateField()  # 借閱日期
    returned_date = models.DateField(null=True, blank=True)  # 歸還日期

    def __str__(self):
        return f"{self.book.title} - {self.user.username}"  # 返回書名和用戶名作為模型的字串表示