# 檔案: users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]  # 性別選項

    ROLE_CHOICES = [
        ('teacher', '老師'),
        ('student', '學生'),
    ]  # 登入身分選項

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # 連結到用戶模型的OneToOneField
    lms_number = models.CharField(max_length=10, editable=False, unique=True, blank=True)  # 學號欄位，唯一且不可編輯
    phone = models.CharField(max_length=15, blank=True)  # 電話欄位
    address = models.TextField(blank=True)  # 地址欄位
    birth_date = models.DateField(null=True, blank=True)  # 生日欄位
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)  # 性別欄位，使用選擇框
    website = models.URLField(blank=True)  # 個人網站欄位
    bio = models.TextField(blank=True)  # 簡介欄位
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')  # 登入身分欄位，預設為讀者

    # 自動生成學號
    def generate_lms_number(self):
        current_year = datetime.now().year  # 取得當前年份
        last_profile = UserProfile.objects.filter(lms_number__startswith=f'S{current_year}').order_by('lms_number').last()
        if last_profile:
            last_number = int(last_profile.lms_number[-4:])  # 取得最後一個用戶的學號的最後四位數字
            new_number = last_number + 1  # 新的學號序號加1
        else:
            new_number = 1  # 如果沒有用戶，則從1開始
        self.lms_number = f'S{current_year}{new_number:04d}'  # 生成新的學號

    def __str__(self):
        return self.user.username  # 返回用戶名作為模型的字串表示

# 當 User 被創建時自動創建 UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile(user=instance)
        profile.generate_lms_number()  # 生成學號
        profile.save()  # 儲存 UserProfile

# 當 User 儲存時也儲存對應的 UserProfile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # 儲存 User 時，自動儲存對應的 UserProfile