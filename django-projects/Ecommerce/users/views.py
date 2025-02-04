from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm, SignUpForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.contrib.auth import views as auth_views

# 首頁視圖
def home(request):
    return render(request, 'home.html')

# 儀表板視圖，根據用戶角色重定向到不同的儀表板
@login_required
def dashboard(request):
    if request.user.profile.role == 'boss':
        return redirect('boss_dashboard')  # 老闆儀表板
    else:
        return redirect('consumer_dashboard')  # 客人儀表板

# 老闆儀表板
@login_required
def boss_dashboard(request):
    if request.user.profile.role != 'boss':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('home')
    return render(request, 'dashboard/boss_dashboard.html')

# 客人儀表板
@login_required
def consumer_dashboard(request):
    if request.user.profile.role != 'consumer':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('home')
    return render(request, 'dashboard/consumer_dashboard.html')

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
    return redirect('logout_success')  # 登出後重定向到登出成功頁面

# 登出成功視圖
def logout_success(request):
    return render(request, 'users/logout.html')  # 渲染登出成功頁面

# 使用者註冊視圖
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # 使用提交的資料建立註冊表單
        if form.is_valid():
            user = form.save()  # 保存新使用者
            user.refresh_from_db()  # 加載用戶的 profile 實例
            user.profile.role = 'consumer'  # 設定用戶的角色為客人
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)  # 自動登入註冊的使用者
            login(request, user)
            messages.success(request, "註冊成功！歡迎！")
            if user.profile.role == 'boss':
                return redirect('boss_dashboard')  # 註冊後重定向到老闆儀表板
            else:
                return redirect('consumer_dashboard')  # 註冊後重定向到客人儀表板
    else:
        form = SignUpForm()  # 如果是 GET 請求，返回空白註冊表單
    return render(request, 'users/register.html', {'form': form})  # 渲染註冊頁面並傳遞表單

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