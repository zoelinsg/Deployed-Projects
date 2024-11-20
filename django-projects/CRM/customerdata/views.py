from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import viewsets
from .forms import SignUpForm, AddRecordForm
from .models import Record
from .serializers import RecordSerializer

# 首頁視圖
@login_required(login_url='login')  # 確保使用者登入，否則重定向到登入頁面
def home(request):
    records = Record.objects.all()  # 獲取所有客戶記錄
    return render(request, 'home.html', {'records': records})  # 渲染首頁模板並傳遞客戶記錄

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

# 顯示單筆客戶記錄的視圖
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)  # 根據主鍵（pk）查找特定客戶記錄
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "您必須登入後才能查看該頁面...")
        return redirect('home')

# 刪除客戶記錄的視圖
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)  # 根據主鍵（pk）查找並刪除記錄
        delete_it.delete()
        messages.success(request, "記錄已成功刪除...")
        return redirect('home')
    else:
        messages.error(request, "您必須登入後才能執行此操作...")
        return redirect('home')

# 新增客戶記錄的視圖
def add_record(request):
    form = AddRecordForm(request.POST or None)  # 建立新增記錄表單
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()  # 保存新記錄
                messages.success(request, "記錄已成功新增...")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})  # 返回新增記錄表單頁面
    else:
        messages.error(request, "您必須登入後才能執行此操作...")
        return redirect('home')

# 更新客戶記錄的視圖
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)  # 根據主鍵（pk）查找需要更新的記錄
        form = AddRecordForm(request.POST or None, instance=current_record)  # 將當前記錄加載到表單中
        if form.is_valid():
            form.save()  # 保存更新後的記錄
            messages.success(request, "記錄已成功更新！")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})  # 返回更新記錄表單頁面
    else:
        messages.error(request, "您必須登入後才能執行此操作...")
        return redirect('home')

# API 視圖集
class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()  # 設定查詢集
    serializer_class = RecordSerializer  # 設定序列化類