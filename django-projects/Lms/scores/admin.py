from django.contrib import admin
from .models import CourseGrade

@admin.register(CourseGrade)
class CourseGradeAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'average_grade', 'adjusted_grade')
    search_fields = ('course__name', 'student__username')