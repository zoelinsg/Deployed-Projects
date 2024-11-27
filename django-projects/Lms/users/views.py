from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from assignment.models import Assignment, Grade
from exam.models import ExamSubmission
from scores.models import CourseGrade
from .forms import CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm, SignUpForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.contrib.auth import views as auth_views
from courses.models import Course

# 首頁視圖
def home(request):
    return render(request, 'home.html')

# 首頁視圖(不同身分登入後導向不同頁面)
@login_required
def dashboard(request):
    if request.user.profile.role == 'teacher':
        return redirect('teacher_dashboard')  # 導向老師儀表板
    else:
        return redirect('student_dashboard')  # 導向學生儀表板

# 老師儀表板
@login_required
def teacher_dashboard(request):
    if request.user.profile.role != 'teacher':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('dashboard')
    
    courses = Course.objects.filter(teacher=request.user)
    grades = Grade.objects.filter(assignment__course__in=courses)
    submissions = ExamSubmission.objects.filter(exam__course__in=courses)
    course_grades = CourseGrade.objects.filter(course__in=courses)
    
    # 計算每個學生在每個課程的總成績
    student_grades = {}
    for grade in grades:
        student = grade.student
        course = grade.assignment.course
        if student not in student_grades:
            student_grades[student] = {}
        if course not in student_grades[student]:
            student_grades[student][course] = []
        student_grades[student][course].append(grade.grade)
    
    total_grades = {student: {course: sum(grades) / len(grades) for course, grades in courses.items()} for student, courses in student_grades.items()}
    
    # 計算每個學生的考試總成績
    student_exam_grades = {}
    for submission in submissions:
        student = submission.student
        course = submission.exam.course
        if student not in student_exam_grades:
            student_exam_grades[student] = {}
        if course not in student_exam_grades[student]:
            student_exam_grades[student][course] = []
        student_exam_grades[student][course].append(submission.score)
    
    total_exam_grades = {student: {course: sum(scores) / len(scores) for course, scores in courses.items()} for student, courses in student_exam_grades.items()}
    
    return render(request, 'lms/dashboard/teacher_dashboard.html', {
        'courses': courses,
        'total_grades': total_grades,
        'total_exam_grades': total_exam_grades,
        'course_grades': course_grades
    })

# 學生儀表板
@login_required
def student_dashboard(request):
    if request.user.profile.role != 'student':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('dashboard')
    
    courses = request.user.enrolled_courses.all()
    grades = Grade.objects.filter(student=request.user)
    submissions = ExamSubmission.objects.filter(student=request.user)
    course_grades = CourseGrade.objects.filter(student=request.user)
    
    # 計算每個課程的總成績
    course_grades_dict = {}
    for grade in grades:
        if grade.assignment.course not in course_grades_dict:
            course_grades_dict[grade.assignment.course] = []
        course_grades_dict[grade.assignment.course].append(grade.grade)
    
    total_grades = {course: sum(grades) / len(grades) for course, grades in course_grades_dict.items()}
    
    # 計算每個課程的考試總成績
    course_exam_grades = {}
    for submission in submissions:
        course = submission.exam.course
        if course not in course_exam_grades:
            course_exam_grades[course] = []
        course_exam_grades[course].append(submission.score)
    
    total_exam_grades = {course: sum(scores) / len(scores) for course, scores in course_exam_grades.items()}

    return render(request, 'lms/dashboard/student_dashboard.html', {
        'courses': courses,
        'total_grades': total_grades,
        'total_exam_grades': total_exam_grades,
        'course_grades': course_grades
    })

# 登入視圖
def login_user(request):
    if request.method == 'POST':  # 檢查是否提交登入表單
        username = request.POST['username']  # 從 POST 請求中取得使用者名稱
        password = request.POST['password']  # 從 POST 請求中取得密碼
        user = authenticate(request, username=username, password=password)  # 認證使用者
        if user is not None:
            login(request, user)  # 登入使用者
            messages.success(request, "成功登入！")
            return redirect('dashboard')  # 登入後重定向到儀表板
        else:
            messages.error(request, "登入失敗，請再試一次...")
            return redirect('login')
    else:
        return render(request, 'users/login.html')  # 渲染登入頁面

# 登出視圖
def logout_user(request):
    logout(request)  # 執行登出操作
    messages.success(request, "您已成功登出...")
    return redirect('home')  # 登出後重定向到首頁

# 使用者註冊視圖
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # 使用提交的資料建立註冊表單
        if form.is_valid():
            user = form.save()  # 保存新使用者
            user.refresh_from_db()  # 加載用戶的 profile 實例
            user.profile.role = form.cleaned_data.get('role')  # 設定用戶的 role
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)  # 自動登入註冊的使用者
            login(request, user)
            messages.success(request, "註冊成功！歡迎！")
            return redirect('dashboard')  # 註冊後重定向到儀表板
    else:
        form = SignUpForm()  # 如果是 GET 請求，返回空白註冊表單
    return render(request, 'users/register.html', {'form': form})

# UserProfileView 用於查看和更新用戶個人資料
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # 只允許已驗證用戶訪問

    def get_object(self):
        user = self.request.user
        # 檢查是否存在 UserProfile，若不存在則自動創建
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile

@login_required
def user_profile_view(request):
    user = request.user
    # 確認或創建該使用者的 UserProfile
    profile, created = UserProfile.objects.get_or_create(user=user)

    # 檢查是否為 POST 請求，處理表單提交
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '個人資料已更新。')
            return redirect('user-profile')
    else:
        form = UserProfileForm(instance=profile)

    # 格式化生日欄位為 `yyyy-MM-dd` 格式
    birth_date = profile.birth_date.strftime('%Y-%m-%d') if profile.birth_date else ''

    # 傳遞表單和格式化後的生日資料給模板
    return render(request, 'users/profile.html', {'form': form, 'user': user, 'birth_date': birth_date})

# 自定義密碼重設視圖，使用自定義的密碼重設表單。
class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'

# 自定義密碼重設確認視圖，使用自定義的設定密碼表單。
class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'users/password_reset_confirm.html'

# 自定義密碼重設完成視圖，使用正確的模板
class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'  # 指定模板路徑

# 自定義密碼修改視圖，使用自定義的密碼修改表單。
class CustomPasswordChangeView(auth_views.PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'

# 自定義密碼重設成功視圖，使用正確的模板
class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'  # 指定模板路徑

# 自定義的密碼修改視圖，使用 password_change.html 模板
class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'users/password_change.html'  # 指定模板路徑

# 自定義的密碼修改成功視圖，使用 password_change_done.html 模板
class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'  # 指定模板路徑