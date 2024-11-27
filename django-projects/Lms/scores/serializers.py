from rest_framework import serializers
from .models import CourseGrade

# 課程總成績序列化器
class CourseGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseGrade
        fields = ['course', 'student', 'average_grade', 'adjusted_grade']
        read_only_fields = ['average_grade']