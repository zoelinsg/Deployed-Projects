from rest_framework import serializers
from .models import Course, Category, Material

# 課程序列化器
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code', 'name', 'category', 'description', 'teacher', 'students', 'start_date', 'end_date', 'notes', 'materials', 'created_at', 'updated_at']

# 課程類別序列化器
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

# 教材序列化器
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['course', 'file', 'description', 'uploaded_at']