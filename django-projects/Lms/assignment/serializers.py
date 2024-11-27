from rest_framework import serializers
from .models import Assignment, Submission, Grade

# 作業序列化器
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'course', 'created_at', 'deadline']  # 序列化欄位

# 提交序列化器
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'submitted_at', 'file', 'grade']  # 序列化欄位

# 成績序列化器
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'assignment', 'grade']  # 序列化欄位