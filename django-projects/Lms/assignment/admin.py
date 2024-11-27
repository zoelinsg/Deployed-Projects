from django.contrib import admin
from .models import Assignment, Submission, Grade

# 註冊作業模型到管理介面
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'deadline')  # 顯示欄位
    search_fields = ('title', 'course__title')  # 搜尋欄位
    list_filter = ('course', 'created_at', 'deadline')  # 篩選器

# 註冊提交模型到管理介面
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'grade')  # 顯示欄位
    search_fields = ('assignment__title', 'student__username')  # 搜尋欄位
    list_filter = ('assignment', 'submitted_at', 'grade')  # 篩選器

# 註冊成績模型到管理介面
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'assignment', 'grade')  # 顯示欄位
    search_fields = ('student__username', 'course__title', 'assignment__title')  # 搜尋欄位
    list_filter = ('course', 'assignment', 'grade')  # 篩選器