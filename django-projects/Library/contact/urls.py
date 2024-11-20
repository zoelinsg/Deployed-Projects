from django.urls import path
from .views import send_message, toggle_read_status, archive_message, unarchive_message, message_list, archived_message_list

urlpatterns = [
    path('send_message/', send_message, name='send_message'),  # 發送訊息
    path('toggle_read_status/<int:pk>/', toggle_read_status, name='toggle_read_status'),  # 標記訊息為已讀或未讀
    path('archive_message/<int:pk>/', archive_message, name='archive_message'),  # 封存訊息
    path('unarchive_message/<int:pk>/', unarchive_message, name='unarchive_message'),  # 解除封存訊息
    path('messages/', message_list, name='message_list'),  # 訊息列表
    path('archived_messages/', archived_message_list, name='archived_message_list'),  # 封存訊息列表
]