from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

urlpatterns = [
    path('exams/', views.exam_list, name='exam_list'),  # 老師查看所有考試
    path('exams/new/', views.exam_create, name='exam_create'),  # 老師新增考試
    path('exams/<int:pk>/edit/', views.exam_update, name='exam_update'),  # 老師修改考試
    path('exams/<int:pk>/delete/', views.exam_delete, name='exam_delete'),  # 老師刪除考試
    path('exams/<int:pk>/', views.exam_detail, name='exam_detail'),  # 老師查看考試詳情並出考題
    path('exams/<int:exam_pk>/take/', views.take_exam, name='take_exam'),  # 學生進行考試
    path('exams/submissions/', views.exam_submissions, name='exam_submissions'),  # 老師查看所有成績
    path('exams/submissions/<int:submission_pk>/result/', views.exam_result, name='exam_result'),  # 學生查看考試成績
    path('questions/<int:pk>/edit/', views.question_update, name='question_update'),  # 老師編輯考題
    path('questions/<int:pk>/delete/', views.question_delete, name='question_delete'),  # 老師刪除考題
    path('grades/', views.total_grades, name='total_grades'),  # 學生查看總成績
    path('', include(router.urls)),  # API 路徑
]