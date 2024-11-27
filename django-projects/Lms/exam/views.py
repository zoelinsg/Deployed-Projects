from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exam, Question, ExamSubmission, ExamAnswer
from .forms import ExamForm, QuestionForm, ExamSubmissionForm, ExamAnswerForm

# 老師查看所有考試
@login_required
def exam_list(request):
    if request.user.profile.role != 'teacher' and request.user.profile.role != 'student':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    exams = Exam.objects.all()
    return render(request, 'lms/exams/exam_list.html', {'exams': exams})

# 老師新增考試
@login_required
def exam_create(request):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = ExamForm()
    return render(request, 'lms/exams/exam_form.html', {'form': form})

# 老師修改考試
@login_required
def exam_update(request, pk):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = ExamForm(instance=exam)
    return render(request, 'lms/exams/exam_form.html', {'form': form})

# 老師刪除考試
@login_required
def exam_delete(request, pk):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        return redirect('exam_list')
    return render(request, 'lms/exams/exam_confirm_delete.html', {'exam': exam})

# 老師查看考試詳情並出考題
@login_required
def exam_detail(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    questions = exam.questions.all()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = QuestionForm()
    return render(request, 'lms/exams/exam_detail.html', {'exam': exam, 'questions': questions, 'form': form})

# 老師編輯考題
@login_required
def question_update(request, pk):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('exam_detail', pk=question.exam.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'lms/exams/question_form.html', {'form': form})

# 老師刪除考題
@login_required
def question_delete(request, pk):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    question = get_object_or_404(Question, pk=pk)
    exam_pk = question.exam.pk
    question.delete()
    return redirect('exam_detail', pk=exam_pk)

# 學生進行考試
@login_required
def take_exam(request, exam_pk):
    if request.user.profile.role != 'student':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    exam = get_object_or_404(Exam, pk=exam_pk)
    if request.method == 'POST':
        submission = ExamSubmission.objects.create(exam=exam, student=request.user)
        for question in exam.questions.all():
            selected_option = request.POST.get(f'question_{question.id}')
            ExamAnswer.objects.create(submission=submission, question=question, selected_option=selected_option)
        submission.calculate_score()
        return redirect('exam_result', submission_pk=submission.pk)
    return render(request, 'lms/exams/take_exam.html', {'exam': exam})

# 學生查看考試成績
@login_required
def exam_result(request, submission_pk):
    if request.user.profile.role != 'student':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    submission = get_object_or_404(ExamSubmission, pk=submission_pk)
    return render(request, 'lms/exams/exam_result.html', {'submission': submission})

# 老師查看所有成績
@login_required
def exam_submissions(request):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    submissions = ExamSubmission.objects.all()
    
    # 計算每個學生的總成績
    student_exam_grades = {}
    for submission in submissions:
        student = submission.student
        if student not in student_exam_grades:
            student_exam_grades[student] = []
        student_exam_grades[student].append(submission.score)
    
    total_exam_grades = {student: sum(grades) / len(grades) for student, grades in student_exam_grades.items()}
    
    return render(request, 'lms/exams/exam_submissions.html', {'submissions': submissions, 'total_exam_grades': total_exam_grades})

# 學生查看總成績
@login_required
def total_grades(request):
    if request.user.profile.role != 'student':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    submissions = ExamSubmission.objects.filter(student=request.user)
    course_exam_grades = {}
    for submission in submissions:
        course = submission.exam.course
        if course not in course_exam_grades:
            course_exam_grades[course] = []
        course_exam_grades[course].append(submission.score)
    
    total_exam_grades = {course: sum(grades) / len(grades) for course, grades in course_exam_grades.items()}
    
    return render(request, 'lms/exams/total_grades.html', {'submissions': submissions, 'total_exam_grades': total_exam_grades})