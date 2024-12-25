# 檔案: users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]  # 性別選項

    ROLE_CHOICES = [
        ('librarian', '館員'),
        ('reader', '讀者'),
    ]  # 登入身分選項

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # 連結到用戶模型的OneToOneField
    library_card_number = models.CharField(max_length=10, editable=False, unique=True, blank=True)  # 圖書館證號碼，不可編輯，唯一
    phone = models.CharField(max_length=15, blank=True)  # 電話欄位
    address = models.TextField(blank=True)  # 地址欄位
    birth_date = models.DateField(null=True, blank=True)  # 生日欄位
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)  # 性別欄位，使用選擇框
    website = models.URLField(blank=True)  # 個人網站欄位
    bio = models.TextField(blank=True)  # 簡介欄位
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='reader')  # 登入身分欄位，預設為讀者

    def __str__(self):
        return self.user.username  # 返回用戶名作為模型的字串表示

# 圖書館證號碼的自動生成
@receiver(post_save, sender=UserProfile)
def create_library_card_number(sender, instance, created, **kwargs):
    if created:
        instance.library_card_number = 'L' + str(instance.id).zfill(9)  # 生成圖書館證號碼，格式為 L + 用戶 ID，不足9位補0
        instance.save()  # 儲存用戶資料
        
# 當 User 被創建時自動創建 UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)  # 創建新用戶時，自動創建 UserProfile

# 當 User 儲存時也儲存對應的 UserProfile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()  # 儲存 User 時，自動儲存對應的 UserProfile