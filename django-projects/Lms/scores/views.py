from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from .models import CourseGrade
from .serializers import CourseGradeSerializer
from .forms import CourseGradeForm
from courses.models import Course
from assignment.models import Grade
from exam.models import ExamSubmission
from django.contrib.auth.models import User

# 顯示成績管理總表
@login_required
def course_grades_overview(request):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    courses = Course.objects.filter(teacher=request.user)
    return render(request, 'lms/scores/course_grades_overview.html', {'courses': courses})

# 學生查看自己的課程總成績
@login_required
def student_course_grades(request):
    if request.user.profile.role != 'student':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    course_grades = CourseGrade.objects.filter(student=request.user)
    
    return render(request, 'lms/scores/student_course_grades.html', {'course_grades': course_grades})

# 老師管理課程總成績
@login_required
def manage_course_grades(request, course_pk, student_pk):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    course = get_object_or_404(Course, pk=course_pk)
    student = get_object_or_404(User, pk=student_pk)
    course_grade, created = CourseGrade.objects.get_or_create(course=course, student=student)
    assignment_grades = Grade.objects.filter(assignment__course=course, student=student)
    exam_submissions = ExamSubmission.objects.filter(exam__course=course, student=student)
    
    if request.method == 'POST':
        form = CourseGradeForm(request.POST, instance=course_grade)
        if form.is_valid():
            form.save()
            messages.success(request, "課程總成績已更新。")
            return redirect('course_grades_overview')
    else:
        form = CourseGradeForm(instance=course_grade)
    
    return render(request, 'lms/scores/manage_course_grades.html', {
        'form': form,
        'course_grade': course_grade,
        'assignment_grades': assignment_grades,
        'exam_submissions': exam_submissions
    })

# 課程總成績視圖集
class CourseGradeViewSet(viewsets.ModelViewSet):
    queryset = CourseGrade.objects.all()
    serializer_class = CourseGradeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.profile.role == 'teacher':
            return CourseGrade.objects.filter(course__teacher=user)
        elif user.profile.role == 'student':
            return CourseGrade.objects.filter(student=user)
        else:
            return CourseGrade.objects.none()