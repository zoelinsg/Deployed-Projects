from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# 作業模型
class Assignment(models.Model):
    title = models.CharField(max_length=200)  # 作業標題
    description = models.TextField()  # 作業描述
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')  # 所屬課程
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    deadline = models.DateTimeField()  # 截止日期

    def __str__(self):
        return self.title

# 提交模型
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')  # 所屬作業
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')  # 提交學生
    submitted_at = models.DateTimeField(auto_now_add=True)  # 提交時間
    file = models.FileField(upload_to='submissions/')  # 提交的文件
    grade = models.FloatField(null=True, blank=True)  # 成績

    def __str__(self):
        return f"{self.student.username} 的提交作業 {self.assignment.title}"

    class Meta:
        unique_together = ('assignment', 'student')  # 確保每個學生只能提交一次作業

# 成績模型
class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')  # 學生
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')  # 課程
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='grades')  # 作業
    grade = models.FloatField()  # 成績

    def __str__(self):
        return f"{self.student.username} 在 {self.course.title} 的成績"