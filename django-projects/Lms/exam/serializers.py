from rest_framework import serializers
from .models import Exam, Question, ExamSubmission, ExamAnswer

# 考試序列化器
class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'title', 'course', 'date', 'duration', 'total_marks']  # 序列化欄位

# 問題序列化器
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'exam', 'text', 'option1', 'option2', 'option3', 'option4', 'correct_option', 'marks']  # 序列化欄位

# 考試提交序列化器
class ExamSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSubmission
        fields = ['id', 'exam', 'student', 'submitted_at', 'score']  # 序列化欄位

# 考試答案序列化器
class ExamAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamAnswer
        fields = ['id', 'submission', 'question', 'selected_option']  # 序列化欄位