from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomPasswordChangeView, CustomPasswordChangeDoneView, CustomPasswordResetDoneView, CustomPasswordResetView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, logout_user
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 首頁
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),  # 登入
    path('logout/', logout_user, name='logout'),  # 登出
    path('logout/success/', views.logout_success, name='logout_success'),  # 登出成功頁面
    path('register/', views.register_user, name='register'),  # 註冊
    path('profile/', views.user_profile_view, name='user-profile'),  # 個人資料
    
    # 忘記密碼功能的 URL 路由
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),  # 忘記密碼
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),  # 忘記密碼郵件發送成功
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # 重設密碼確認
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),  # 重設密碼完成

    # 修改密碼功能的 URL 路由
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),  # 修改密碼
    path('password_change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),  # 修改密碼成功

    # 儀表板路由
    path('boss-dashboard/', views.boss_dashboard, name='boss_dashboard'),  # 老闆儀表板
    path('consumer-dashboard/', views.consumer_dashboard, name='consumer_dashboard'),  # 客人儀表板
]