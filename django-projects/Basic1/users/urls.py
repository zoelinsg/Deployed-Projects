# 定義 URL 路徑，使用戶可以訪問其個人資料的查看和更新
from django.urls import path
from .views import user_profile_view
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 首頁路由
    path('login/', views.login_user, name='login'),  # 登入路由
    path('logout/', views.logout_user, name='logout'),  # 登出路由
    path('register/', views.register_user, name='register'),  # 註冊路由
    path('profile/', user_profile_view, name='user-profile'),
]