from django.contrib import admin
from .models import Course, Category, Material

# 註冊 Course 模型到 Django 管理後台
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'teacher', 'start_date', 'end_date', 'created_at', 'updated_at')  # 在管理後台顯示的欄位
    search_fields = ('code', 'name', 'description', 'teacher__username')  # 可搜尋的欄位
    list_filter = ('category', 'start_date', 'end_date')  # 可過濾的欄位

    # 自定義管理後台的表單顯示
    fieldsets = (
        (None, {
            'fields': ('code', 'name', 'category', 'description', 'teacher', 'students', 'start_date', 'end_date', 'notes')
        }),
    )
    readonly_fields = ('code',)  # 設定 code 欄位為唯讀

# 註冊 Category 模型到 Django 管理後台
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # 在管理後台顯示的欄位
    search_fields = ('name', 'description')  # 可搜尋的欄位

# 註冊 Material 模型到 Django 管理後台
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('course', 'file', 'description', 'uploaded_at')  # 在管理後台顯示的欄位
    search_fields = ('course__name', 'file', 'description')  # 可搜尋的欄位
    list_filter = ('uploaded_at',)  # 可過濾的欄位