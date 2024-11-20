from django.contrib import admin
from .models import Record

# 註冊 Record 模型到管理界面
@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'company', 'position', 'created_at')  # 設定列表顯示的欄位
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'company')  # 設定可搜尋的欄位
    list_filter = ('city', 'company')  # 設定篩選器