# 用戶模型和個人資料模型的定義
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 定義用戶的個人資料模型，儲存用戶的額外資訊
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # 連結到用戶模型的OneToOneField
    phone = models.CharField(max_length=15, blank=True)  # 電話欄位
    address = models.TextField(blank=True)  # 地址欄位
    # 可根據需求添加更多個人資訊欄位

# 當 User 被創建時自動創建 UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)  # 創建新用戶時，自動創建 UserProfile

# 當 User 儲存時也儲存對應的 UserProfile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # 儲存 User 時，自動儲存對應的 UserProfile
