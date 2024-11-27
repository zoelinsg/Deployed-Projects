from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 定義用戶的個人資料模型，儲存用戶的額外資訊
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]  # 性別選項

    ROLE_CHOICES = [
        ('boss', '老闆'),
        ('consumer', '客人'),
    ]  # 角色選項

    COUNTRY_CHOICES = [
        ('TW', '台灣'),
        ('CN', '中國'),
        ('US', '美國'),
        ('JP', '日本'),
        ('KR', '韓國'),
        ('SG', '新加坡'),
        ('MY', '馬來西亞'),
        ('TH', '泰國'),
        ('VN', '越南'),
        ('ID', '印尼'),
        ('PH', '菲律賓'),
        ('AU', '澳洲'),
        ('NZ', '紐西蘭'),
        ('CA', '加拿大'),
        ('GB', '英國'),
        ('FR', '法國'),
        ('DE', '德國'),
        ('IT', '義大利'),
        ('ES', '西班牙'),
        ('PT', '葡萄牙'),
        ('NL', '荷蘭'),
        ('BE', '比利時'),
        ('SE', '瑞典'),
        ('NO', '挪威'),
        ('FI', '芬蘭'),
        ('DK', '丹麥'),
    ]  # 國家選項

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # 連結到用戶模型的OneToOneField
    birth_date = models.DateField(null=True, blank=True)  # 生日欄位
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)  # 性別欄位，使用選擇框
    bio = models.TextField(blank=True)  # 簡介欄位
    phone = models.CharField(max_length=15, blank=True)  # 電話欄位
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True)  # 國家欄位，使用選擇框
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='consumer')  # 角色欄位，使用選擇框

    def __str__(self):
        return self.user.username  # 返回用戶名作為模型的字串表示

# 當 User 被創建時自動創建 UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)  # 創建新用戶時，自動創建 UserProfile

# 當 User 儲存時也儲存對應的 UserProfile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # 儲存 User 時，自動儲存對應的 UserProfile

# 自動設定用戶的角色和密碼
@receiver(post_save, sender=User)
def set_user_role_and_password(sender, instance, created, **kwargs):
    if created:
        if instance.email == 'boss001@gmail.com':
            instance.profile.role = 'boss'  # 設定老闆角色
            instance.set_password('boss001boss001')  # 設定老闆密碼
        else:
            instance.profile.role = 'consumer'  # 設定客人角色
        instance.save()
        instance.profile.save()  # 儲存 UserProfile