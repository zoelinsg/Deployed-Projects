from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 首頁路由
    path('login/', views.login_user, name='login'),  # 登入路由
    path('logout/', views.logout_user, name='logout'),  # 登出路由
    path('register/', views.register_user, name='register'),  # 註冊路由
    path('record/<int:pk>', views.customer_record, name='record'),  # 顯示單筆客戶記錄的路由
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),  # 刪除客戶記錄的路由
    path('add_record/', views.add_record, name='add_record'),  # 新增客戶記錄的路由
    path('update_record/<int:pk>', views.update_record, name='update_record'),  # 更新客戶記錄的路由
]