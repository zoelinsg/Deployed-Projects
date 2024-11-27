from django.urls import path
from . import views

urlpatterns = [
    # 產品相關 URL
    path('', views.product_list, name='product_list'),  # 顯示所有商品
    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # 顯示單個產品的詳細資訊
    path('category/<str:category_name>/', views.product_category, name='product_category'),  # 顯示分類中的產品
    path('search/', views.product_search, name='product_search'),  # 搜尋產品
    path('manage-products/', views.manage_products, name='manage_products'),  # 管理產品
    path('add-product/', views.add_product, name='add_product'),  # 新增產品
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),  # 編輯產品
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),  # 刪除產品
    path('manage-stock/', views.manage_stock, name='manage_stock'),  # 管理庫存

    # 購物車相關 URL
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # 新增到購物車的 URL 模式
    path('view-cart/', views.view_cart, name='view_cart'),  # 顯示購物車
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # 從購物車中移除商品
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),  # 修改購物車中的商品

    # 訂單相關 URL
    path('place-order/', views.place_order, name='place_order'),  # 下訂單
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),  # 顯示訂單詳情
    path('order-list/', views.order_list, name='order_list'),  # 客人查看自己的訂單
    path('confirm-order/<int:order_id>/', views.confirm_order, name='confirm_order'),  # 確認訂單
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),  # 取消訂單
    path('order-list-boss/', views.order_list_boss, name='order_list_boss'),  # 老闆查看所有訂單
    path('order-detail-boss/<int:order_id>/', views.order_detail_boss, name='order_detail_boss'),  # 老闆查看訂單詳情
    path('manage-orders/', views.manage_orders, name='manage_orders'),  # 管理訂單
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),  # 更新訂單狀態

    # 支付相關 URL
    path('paypal-payment/<int:order_id>/', views.process_payment, name='process_payment'),  # PayPal 支付
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),  # 支付成功
    path('payment-cancel/<int:order_id>/', views.payment_cancel, name='payment_cancel'),  # 支付取消
    path('payment-error/<int:order_id>/', views.payment_error, name='payment_error'),  # 支付失敗

    # 銷售報表 URL
    path('sales-report/', views.sales_report, name='sales_report'),  # 銷售報表

    # API 相關 URL
    path('api/products/', views.api_product_list, name='api_product_list'),  # API 端點，獲取所有產品的序列化資料
    path('api/products/<int:pk>/', views.api_product_detail, name='api_product_detail'),  # API 端點，獲取單個產品的序列化資料
    path('api/carts/', views.CartListCreateAPIView.as_view(), name='api_cart_list_create'),  # API 端點，獲取和創建購物車
    path('api/cart-items/', views.CartItemListCreateAPIView.as_view(), name='api_cart_item_list_create'),  # API 端點，獲取和創建購物車項目
    path('api/orders/', views.OrderListCreateAPIView.as_view(), name='api_order_list_create'),  # API 端點，獲取和創建訂單
    path('api/order-items/', views.OrderItemListCreateAPIView.as_view(), name='api_order_item_list_create'),  # API 端點，獲取和創建訂單項目
]