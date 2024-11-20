from django.urls import path
from .views import home, book_room, confirm_booking, process_payment, payment_success, payment_cancel, about, search_booking, cancel_booking, BookingViewSet
from rest_framework.routers import DefaultRouter

# 設置 DefaultRouter
router = DefaultRouter()
router.register(r'api/bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', home, name='home'),  # 首頁路由
    path('about/', about, name='about'),  # 關於我們路由
    path('book/', book_room, name='book_room'),  # 訂房路由
    path('confirm/<int:booking_id>/', confirm_booking, name='confirm_booking'),  # 確認訂單路由
    path('payment/<int:booking_id>/', process_payment, name='process_payment'),  # 處理支付路由
    path('payment/success/', payment_success, name='payment_success'),  # 支付成功路由
    path('payment/cancel/', payment_cancel, name='payment_cancel'),  # 支付取消路由
    path('search/', search_booking, name='search_booking'),  # 查詢訂單路由
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),  # 取消訂單路由
]

# 加入 API 路由
urlpatterns += router.urls