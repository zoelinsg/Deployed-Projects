# 檔案: admin.py
from django.contrib import admin
from .models import Book, BorrowHistory

# 註冊 Book 模型到 Django 管理後台
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'isbn', 'status', 'borrowed_by', 'borrowed_date', 'due_date', 'cancelled_date')  # 在管理後台顯示的欄位
    search_fields = ('title', 'author', 'isbn')  # 可搜尋的欄位
    list_filter = ('category', 'status')  # 可過濾的欄位

    # 自定義管理後台的表單顯示
    fieldsets = (
        (None, {
            'fields': ('title', 'cover', 'author', 'category', 'description', 'publication_date', 'isbn', 'status', 'borrowed_by', 'borrowed_date', 'due_date', 'cancelled_date')
        }),
    )

# 註冊 BorrowHistory 模型到 Django 管理後台
@admin.register(BorrowHistory)
class BorrowHistoryAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'borrowed_date', 'returned_date')  # 在管理後台顯示的欄位
    search_fields = ('book__title', 'user__username')  # 可搜尋的欄位
    list_filter = ('borrowed_date', 'returned_date')  # 可過濾的欄位