from django.contrib import admin
from .models import Exam, Question, ExamSubmission, ExamAnswer

# 註冊考試模型到管理介面
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'date', 'duration', 'total_marks')  # 顯示欄位
    search_fields = ('title', 'course__title')  # 搜尋欄位
    list_filter = ('course', 'date')  # 篩選器

# 註冊問題模型到管理介面
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'text', 'marks')  # 顯示欄位
    search_fields = ('exam__title', 'text')  # 搜尋欄位
    list_filter = ('exam',)  # 篩選器

# 註冊考試提交模型到管理介面
@admin.register(ExamSubmission)
class ExamSubmissionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'submitted_at', 'score')  # 顯示欄位
    search_fields = ('exam__title', 'student__username')  # 搜尋欄位
    list_filter = ('exam', 'submitted_at', 'score')  # 篩選器

# 註冊考試答案模型到管理介面
@admin.register(ExamAnswer)
class ExamAnswerAdmin(admin.ModelAdmin):
    list_display = ('submission', 'question', 'selected_option')  # 顯示欄位
    search_fields = ('submission__exam__title', 'question__text', 'submission__student__username')  # 搜尋欄位
    list_filter = ('submission__exam', 'question')  # 篩選器