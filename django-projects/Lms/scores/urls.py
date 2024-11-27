from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'course_grades', views.CourseGradeViewSet)

urlpatterns = [
    path('course_grades_overview/', views.course_grades_overview, name='course_grades_overview'),
    path('student_grades/', views.student_course_grades, name='student_course_grades'),
    path('manage_course_grades/<int:course_pk>/<int:student_pk>/', views.manage_course_grades, name='manage_course_grades'),
    path('', include(router.urls)),
]