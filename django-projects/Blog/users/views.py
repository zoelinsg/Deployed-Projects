from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserProfileForm, SignUpForm, CustomPasswordResetForm, CustomSetPasswordForm, CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetDoneView, PasswordChangeView, PasswordChangeDoneView, PasswordResetCompleteView

# 登入視圖
def login_user(request):
    if request.method == 'POST':  # 檢查是否提交登入表單
        username = request.POST['username']  # 從 POST 請求中取得使用者名稱
        password = request.POST['password']  # 從 POST 請求中取得密碼
        user = authenticate(request, username=username, password=password)  # 認證使用者
        if user is not None:
            login(request, user)  # 登入使用者
            messages.success(request, "成功登入！")
            return redirect('home')  # 登入後重定向到首頁
        else:
            messages.error(request, "登入失敗，請再試一次...")
            return redirect('login')
    else:
        return render(request, 'users/login.html')  # 渲染登入頁面

# 登出視圖
def logout_user(request):
    logout(request)  # 執行登出操作
    messages.success(request, "您已成功登出...")
    return render(request, 'users/logout.html')  # 渲染登出頁面

# 使用者註冊視圖
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # 使用提交的資料建立註冊表單
        if form.is_valid():
            form.save()  # 保存新使用者
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)  # 自動登入註冊的使用者
            login(request, user)
            messages.success(request, "註冊成功！歡迎！")
            return redirect('home')  # 註冊後重定向到首頁
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
    template_name = 'registration/password_reset.html'

# 自定義密碼重設確認視圖，使用自定義的設定密碼表單。
class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'registration/password_reset_confirm.html'

# 自定義密碼重設完成視圖，使用正確的模板
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'  

# 自定義密碼修改視圖，使用自定義的密碼修改表單。
class CustomPasswordChangeView(auth_views.PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password_change.html'

# 自定義密碼重設成功視圖，使用正確的模板
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'  

# 自定義的密碼修改視圖，使用 password_change.html 模板
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'  

# 自定義的密碼修改成功視圖，使用 password_change_done.html 模板
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'