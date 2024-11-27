from django.urls import path
from . import views

urlpatterns = [
    path('assignments/', views.assignment_list, name='assignment_list'),  # 老師查看所有作業
    path('assignments/new/', views.assignment_create, name='assignment_create'),  # 老師新增作業
    path('assignments/<int:pk>/edit/', views.assignment_update, name='assignment_update'),  # 老師修改作業
    path('assignments/<int:pk>/delete/', views.assignment_delete, name='assignment_delete'),  # 老師刪除作業
    path('assignments/<int:pk>/', views.assignment_detail, name='assignment_detail'),  # 學生查看作業
    path('assignments/<int:assignment_pk>/submit/', views.submission_create, name='submission_create'),  # 學生提交作業
    path('submissions/<int:submission_pk>/grade/', views.grade_submission, name='grade_submission'),  # 老師批改作業
    path('grades/', views.grade_list, name='grade_list'),  # 學生查看成績
]