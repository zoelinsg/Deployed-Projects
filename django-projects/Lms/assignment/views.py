from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assignment, Submission, Grade
from .forms import AssignmentForm, SubmissionForm, GradeForm
from courses.models import Course

# 老師查看所有作業
@login_required
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'lms/assignments/assignment_list.html', {'assignments': assignments})

# 老師新增作業
@login_required
def assignment_create(request):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'lms/assignments/assignment_form.html', {'form': form})

# 老師修改作業
@login_required
def assignment_update(request, pk):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'lms/assignments/assignment_form.html', {'form': form})

# 老師刪除作業
@login_required
def assignment_delete(request, pk):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list')
    return render(request, 'lms/assignments/assignment_confirm_delete.html', {'assignment': assignment})

# 學生查看作業
@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, 'lms/assignments/assignment_detail.html', {'assignment': assignment, 'submissions': submissions})

# 學生提交作業
@login_required
def submission_create(request, assignment_pk):
    if request.user.profile.role != 'student':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    if Submission.objects.filter(assignment=assignment, student=request.user).exists():
        messages.error(request, "您已經提交過此作業，不能重複提交。")
        return redirect('assignment_detail', pk=assignment.pk)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.save()
            messages.success(request, "作業提交成功！")
            return redirect('assignment_detail', pk=assignment.pk)
    else:
        form = SubmissionForm()
    return render(request, 'lms/assignments/submission_form.html', {'form': form, 'assignment': assignment})

# 老師批改作業
@login_required
def grade_submission(request, submission_pk):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    submission = get_object_or_404(Submission, pk=submission_pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            # 更新或創建成績記錄
            grade, created = Grade.objects.get_or_create(
                student=submission.student,
                course=submission.assignment.course,
                assignment=submission.assignment,
                defaults={'grade': submission.grade}
            )
            if not created:
                grade.grade = submission.grade
                grade.save()
            return redirect('assignment_detail', pk=submission.assignment.pk)
    else:
        form = GradeForm(instance=submission)
    return render(request, 'lms/assignments/grade_form.html', {'form': form, 'submission': submission})

# 學生查看成績
@login_required
def grade_list(request):
    if request.user.profile.role != 'student':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    grades = Grade.objects.filter(student=request.user)
    # 計算每個課程的總成績
    course_assignment_grades = {}
    for grade in grades:
        if grade.course not in course_assignment_grades:
            course_assignment_grades[grade.course] = []
        course_assignment_grades[grade.course].append(grade.grade)
    
    total_assignment_grades = {course: sum(grades) / len(grades) for course, grades in course_assignment_grades.items()}
    
    return render(request, 'lms/assignments/grade_list.html', {'grades': grades, 'total_assignment_grades': total_assignment_grades})