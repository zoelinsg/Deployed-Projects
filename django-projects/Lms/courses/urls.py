from django.urls import path
from .views import (
    course_list, add_course, edit_course, delete_course, add_material, edit_material, delete_material,
    course_detail, enroll_course, unenroll_course
)

urlpatterns = [
    path('courses/', course_list, name='course_list'),  # 課程總表
    path('course/add/', add_course, name='add_course'),  # 新增課程
    path('course/edit/<int:course_id>/', edit_course, name='edit_course'),  # 修改課程
    path('course/delete/<int:course_id>/', delete_course, name='delete_course'),  # 刪除課程
    path('course/<int:course_id>/', course_detail, name='course_detail'),  # 課程詳情
    path('course/<int:course_id>/material/add/', add_material, name='add_material'),  # 新增教材
    path('material/edit/<int:material_id>/', edit_material, name='edit_material'),  # 修改教材
    path('material/delete/<int:material_id>/', delete_material, name='delete_material'),  # 刪除教材
    path('course/enroll/<int:course_id>/', enroll_course, name='enroll_course'),  # 選修課程
    path('course/unenroll/<int:course_id>/', unenroll_course, name='unenroll_course'),  # 退選課程
]