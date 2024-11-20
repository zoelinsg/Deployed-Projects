from django.urls import path
from .views import create_activity, update_activity, delete_activity, activity_list, activity_detail, participate_activity, cancel_participation, activity_api

urlpatterns = [
    path('activities/', activity_list, name='activity_list'),  # 活動列表
    path('activities/create/', create_activity, name='create_activity'),  # 創建活動
    path('activities/<int:pk>/', activity_detail, name='activity_detail'),  # 活動詳情
    path('activities/<int:pk>/update/', update_activity, name='update_activity'),  # 更新活動
    path('activities/<int:pk>/delete/', delete_activity, name='delete_activity'),  # 刪除活動
    path('activities/<int:pk>/participate/', participate_activity, name='participate_activity'),  # 參與活動
    path('activities/<int:pk>/cancel/', cancel_participation, name='cancel_participation'),  # 取消參加活動
    path('api/activities/', activity_api, name='activity_api'),  # 活動 API
]