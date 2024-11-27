from django.contrib import admin
from .models import UserProfile  # 引入 UserProfile 模型

# 註冊 UserProfile 模型到 Django 管理後台
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'gender', 'phone', 'country', 'role')  # 設定在管理後台顯示的欄位
    search_fields = ('user__username', 'phone', 'country')  # 設定可搜尋的欄位
    list_filter = ('gender', 'country', 'role')  # 設定篩選器