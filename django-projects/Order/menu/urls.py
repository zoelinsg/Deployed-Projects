from django.urls import path
from .views import menu_item_list, menu_item_detail, search_menu_items, cart, add_to_cart, remove_from_cart, update_cart_item

urlpatterns = [
    path('', menu_item_list, name='menu_item_list'),  # 菜單項目列表視圖
    path('item/<int:pk>/', menu_item_detail, name='menu_item_detail'),  # 單個菜單項目詳細視圖
    path('search/', search_menu_items, name='search_menu_items'),  # 搜尋餐點視圖
    path('cart/', cart, name='cart'),  # 顯示購物車視圖
    path('cart/add/<int:pk>/', add_to_cart, name='add_to_cart'),  # 添加到購物車視圖
    path('cart/remove/<int:pk>/', remove_from_cart, name='remove_from_cart'),  # 刪除購物車項目視圖
    path('cart/update/<int:pk>/', update_cart_item, name='update_cart_item'),  # 修改購物車項目數量視圖
]