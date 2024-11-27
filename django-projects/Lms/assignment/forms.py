from django import forms
from .models import Assignment, Submission, Grade

# 作業表單
class AssignmentForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # 使用日期時間選擇器
        label='截止日期'
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'course', 'deadline']  # 表單欄位
        labels = {
            'title': '作業標題',
            'description': '作業描述',
            'course': '所屬課程',
            'deadline': '截止日期',
        }

# 提交表單
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['assignment', 'file']  # 表單欄位
        labels = {
            'assignment': '所屬作業',
            'file': '提交的文件',
        }

# 成績表單
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'course', 'assignment', 'grade']  # 表單欄位
        labels = {
            'student': '學生',
            'course': '課程',
            'assignment': '作業',
            'grade': '成績',
        }