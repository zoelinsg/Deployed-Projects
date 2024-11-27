from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from assignment.models import Grade
from exam.models import ExamSubmission

# 課程總成績模型
class CourseGrade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_grades', verbose_name="課程")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_grades', verbose_name="學生")
    average_grade = models.FloatField(verbose_name="平均成績")
    adjusted_grade = models.FloatField(null=True, blank=True, verbose_name="調整後成績")

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"

    def calculate_average_grade(self):
        # 計算作業總成績
        assignment_grades = Grade.objects.filter(assignment__course=self.course, student=self.student)
        if assignment_grades.exists():
            total_assignment_grade = sum(grade.grade for grade in assignment_grades) / assignment_grades.count()
        else:
            total_assignment_grade = 0

        # 計算考試總成績
        exam_submissions = ExamSubmission.objects.filter(exam__course=self.course, student=self.student)
        if exam_submissions.exists():
            total_exam_grade = sum(submission.score for submission in exam_submissions) / exam_submissions.count()
        else:
            total_exam_grade = 0

        # 計算課程總成績
        self.average_grade = (total_assignment_grade + total_exam_grade) / 2

    def save(self, *args, **kwargs):
        self.calculate_average_grade()
        super().save(*args, **kwargs)