from django.urls import path
from . import views

urlpatterns = [
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/delete/<int:item_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),  # 新增查看訂單詳情的路由
    path('order/confirm/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order/payment/<int:order_id>/', views.process_payment, name='process_payment'),  # 新增處理支付的路由
    path('order/payment/success/<int:order_id>/', views.payment_success, name='payment_success'),  # 新增支付成功的路由
    path('order/payment/cancel/<int:order_id>/', views.payment_cancel, name='payment_cancel'),  # 新增支付取消的路由
    path('order/payment/error/<int:order_id>/', views.payment_error, name='payment_error'),  # 新增支付失敗的路由
    path('api/carts/', views.CartListCreateAPIView.as_view(), name='api_carts'),
    path('api/cart-items/', views.CartItemListCreateAPIView.as_view(), name='api_cart_items'),
    path('api/orders/', views.OrderListCreateAPIView.as_view(), name='api_orders'),
    path('api/order-items/', views.OrderItemListCreateAPIView.as_view(), name='api_order_items'),
]