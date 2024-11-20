# 定義 UserProfile 的視圖，允許用戶查看和更新其個人資料
from rest_framework import generics, permissions
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserProfileForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# 首頁視圖
@login_required(login_url='login')  # 確保使用者登入，否則重定向到登入頁面
def home(request):
    return render(request, 'home.html')  # 渲染首頁模板並傳遞客戶記錄

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
        return render(request, 'login.html')  # 渲染登入頁面

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
            form.save()  # 保存新使用者
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)  # 自動登入註冊的使用者
            login(request, user)
            messages.success(request, "註冊成功！歡迎！")
            return redirect('home')  # 註冊後重定向到首頁
    else:
        form = SignUpForm()  # 如果是 GET 請求，返回空白註冊表單
    return render(request, 'register.html', {'form': form})

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
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '個人資料已更新。')
            return redirect('user-profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form, 'user': user})