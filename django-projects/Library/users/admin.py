from django.contrib import admin
from .models import UserProfile

# 註冊 UserProfile 模型到 Django 管理後台
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'library_card_number', 'phone', 'address', 'birth_date', 'gender', 'website', 'role')  # 在管理後台顯示的欄位
    search_fields = ('user__username', 'phone', 'address')  # 可搜尋的欄位
    list_filter = ('gender', 'role')  # 可過濾的欄位

    # 自定義管理後台的表單顯示
    fieldsets = (
        (None, {
            'fields': ('user', 'phone', 'address', 'birth_date', 'gender', 'website', 'bio', 'role')  # 移除 library_card_number
        }),
    )