from django import forms
from .models import CourseGrade

# 課程總成績表單
class CourseGradeForm(forms.ModelForm):
    class Meta:
        model = CourseGrade
        fields = ['course', 'student', 'average_grade', 'adjusted_grade']
        labels = {
            'course': '課程',
            'student': '學生',
            'average_grade': '平均成績',
            'adjusted_grade': '調整後成績',
        }