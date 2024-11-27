from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CourseForm, MaterialForm
from .models import Course, Material

# 課程總表視圖
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'lms/courses/course_list.html', {'courses': courses})

# 老師新增課程視圖
@login_required
def add_course(request):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            form.save_m2m()
            messages.success(request, "課程已成功新增。")
            return redirect('teacher_dashboard')
    else:
        form = CourseForm()
    return render(request, 'lms/courses/add_course.html', {'form': form})

# 老師修改課程視圖
@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.teacher:
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "課程已成功修改。")
            return redirect('teacher_dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'lms/courses/edit_course.html', {'form': form, 'course': course})

# 老師刪除課程視圖
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.teacher:
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, "課程已成功刪除。")
        return redirect('teacher_dashboard')
    return render(request, 'lms/courses/delete_course.html', {'course': course})

# 老師新增教材視圖
@login_required
def add_material(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.teacher:
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            messages.success(request, "教材已成功新增。")
            return redirect('course_detail', course_id=course.id)
    else:
        form = MaterialForm()
    return render(request, 'lms/materials/add_material.html', {'form': form, 'course': course})

# 老師修改教材視圖
@login_required
def edit_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.user != material.course.teacher:
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, "教材已成功修改。")
            return redirect('course_detail', course_id=material.course.id)
    else:
        form = MaterialForm(instance=material)
    return render(request, 'lms/materials/edit_material.html', {'form': form, 'material': material})

# 老師刪除教材視圖
@login_required
def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.user != material.course.teacher:
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    if request.method == 'POST':
        material.delete()
        messages.success(request, "教材已成功刪除。")
        return redirect('course_detail', course_id=material.course.id)
    return render(request, 'lms/materials/delete_material.html', {'material': material})

# 課程詳情視圖
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'lms/courses/course_detail.html', {'course': course})

# 學生選修課程視圖
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.profile.role != 'student':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    course.students.add(request.user)
    messages.success(request, "您已成功選修此課程。")
    return redirect('student_dashboard')

# 學生退選課程視圖
@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.profile.role != 'student':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('dashboard')
    
    course.students.remove(request.user)
    messages.success(request, "您已成功退選此課程。")
    return redirect('student_dashboard')