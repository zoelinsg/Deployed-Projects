from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

# 考試模型
class Exam(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    duration = models.DurationField()
    total_marks = models.IntegerField()

    def __str__(self):
        return self.title

# 問題模型
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=200)
    marks = models.IntegerField()

    def __str__(self):
        return f"Question {self.id} for {self.exam.title}"

# 考試提交模型
class ExamSubmission(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username}'s submission for {self.exam.title}"

    def calculate_score(self):
        total_score = 0
        questions = self.exam.questions.all()
        for question in questions:
            answer = self.answers.filter(question=question).first()
            if answer and answer.selected_option == question.correct_option:
                total_score += question.marks
        self.score = total_score
        self.save()

# 考試答案模型
class ExamAnswer(models.Model):
    submission = models.ForeignKey(ExamSubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    selected_option = models.CharField(max_length=200)

    def __str__(self):
        return f"Answer to {self.question.text} by {self.submission.student.username}"