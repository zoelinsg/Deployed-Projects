from django.urls import path
from .views import (
    borrow_room, return_room, room_list, room_detail
)

urlpatterns = [
    path('rooms/', room_list, name='room_list'),  # 自修室列表
    path('rooms/<int:pk>/', room_detail, name='room_detail'),  # 自修室詳情
    path('rooms/<int:pk>/borrow/', borrow_room, name='borrow_room'),  # 借自修室
    path('rooms/<int:pk>/return/', return_room, name='return_room'),  # 結束使用自修室
]