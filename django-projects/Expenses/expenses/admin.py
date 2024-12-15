from django.contrib import admin
from .models import Account, Category, Expense

# 註冊模型到管理介面
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance', 'created', 'updated')  # 顯示的欄位
    search_fields = ('name', 'user__username')  # 搜尋欄位
    list_filter = ('user',)  # 過濾器

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 顯示的欄位
    search_fields = ('name',)  # 搜尋欄位

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'category', 'user', 'amount', 'is_income', 'date', 'created', 'updated')  # 顯示的欄位
    search_fields = ('name', 'account__name', 'category__name', 'user__username')  # 搜尋欄位
    list_filter = ('user', 'is_income', 'date')  # 過濾器