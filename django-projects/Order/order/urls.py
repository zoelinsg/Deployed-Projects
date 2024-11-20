# OrderManagement/urls.py

from django.urls import path
from .views import order_list, order_detail, create_order, create_order_item

urlpatterns = [
    path('orders/', order_list, name='order_list'),  # 顯示所有訂單的列表視圖
    path('orders/<int:pk>/', order_detail, name='order_detail'),  # 顯示單個訂單的詳細視圖
    path('orders/create/', create_order, name='create_order'),  # 創建新訂單的視圖
    path('orders/<int:order_id>/items/create/', create_order_item, name='create_order_item'),  # 為訂單創建新訂單項目的視圖
]