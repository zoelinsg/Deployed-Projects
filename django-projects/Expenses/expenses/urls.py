from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 首頁
    path('accounts/new/', views.account_create, name='account_create'),  # 新增帳戶
    path('accounts/<int:pk>/edit/', views.account_edit, name='account_edit'),  # 編輯帳戶
    path('accounts/<int:pk>/delete/', views.account_delete, name='account_delete'),  # 刪除帳戶
    path('accounts/<int:pk>/expenses/', views.account_expense_list, name='account_expense_list'),  # 單個帳戶的所有記帳項目
    path('expenses/', views.expense_list, name='expense_list'),  # 記帳列表
    path('expenses/new/', views.expense_create, name='expense_create'),  # 新增記帳
    path('expenses/<int:pk>/edit/', views.expense_edit, name='expense_edit'),  # 編輯記帳
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),  # 刪除記帳
    path('transfer/', views.transfer, name='transfer'),  # 轉帳功能
    path('filter_by_date/', views.filter_by_date, name='filter_by_date'),  # 篩選日期顯示記帳項目
    path('filter_by_category/', views.filter_by_category, name='filter_by_category'),  # 篩選分類顯示記帳項目
]