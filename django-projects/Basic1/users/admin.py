# 註冊管理界面，用於管理UserProfile資料
from django.contrib import admin
from .models import UserProfile  # 匯入 UserProfile 模型

# 自訂 UserProfile 的顯示方式
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')  # 在管理界面顯示的欄位
    search_fields = ('user__username', 'phone')  # 設置搜尋欄位，方便管理者查找用戶
    list_filter = ('user',)  # 設置過濾器，以便按用戶篩選

# 註冊 UserProfile 模型到 Django 管理介面
admin.site.register(UserProfile, UserProfileAdmin)  # 註冊 UserProfile 並使用自訂的顯示方式
