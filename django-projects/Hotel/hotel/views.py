from pyexpat.errors import messages
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import viewsets
from .models import Hotel, Booking
from .forms import BookingForm
from .serializers import BookingSerializer
import paypalrestsdk

# 配置 PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # Sandbox 或 live
    "client_id": settings.PAYPAL_CLIENT_ID,  # 從 settings.py 中讀取
    "client_secret": settings.PAYPAL_CLIENT_SECRET  # 從 settings.py 中讀取
})

# 首頁視圖
def home(request):
    return render(request, 'home.html')

# 關於我們視圖
def about(request):
    hotels = Hotel.objects.all()
    return render(request, 'about.html', {'hotels': hotels})

# 訂房視圖
def book_room(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save(commit=False)  # 暫存表單數據
                booking.save()  # 保存到資料庫
                return redirect('confirm_booking', booking_id=booking.id)  # 重定向至確認頁面
            except ValidationError as e:
                form.add_error(None, e.message)  # 顯示驗證錯誤
        else:
            messages.error(request, "表單提交無效，請檢查輸入數據。")
    else:
        form = BookingForm()
    return render(request, 'book_room.html', {'form': form})

# 確認訂單視圖
def confirm_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    deposit_amount = booking.total_price / 4
    return render(request, 'confirm_booking.html', {'booking': booking, 'deposit_amount': deposit_amount})

# 處理支付視圖
def process_payment(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    
    # 計算訂金為總金額的 1/4
    deposit_amount = booking.total_price / 4

    # 創建 PayPal 支付請求
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": f"{deposit_amount:.2f}",  # 訂金金額
                "currency": "USD"  # 使用的貨幣
            },
            "description": f"Deposit for booking {booking.id}"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/success",
            "cancel_url": "http://localhost:8000/payment/cancel"
        }
    })

    # 檢查支付是否創建成功
    if payment.create():
        # 尋找用戶支付鏈接
        for link in payment.links:
            if link.rel == "approval_url":
                # 將用戶重定向至 PayPal 支付頁面
                return redirect(link.href)
    else:
        # 如果支付創建失敗，回傳錯誤信息
        return render(request, 'payment_error.html', {"error": payment.error})

# 支付成功視圖
def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    # 根據支付 ID 獲取支付記錄
    payment = paypalrestsdk.Payment.find(payment_id)

    # 確認支付
    if payment.execute({"payer_id": payer_id}):
        # 更新訂單記錄
        booking_id = payment.transactions[0].description.split()[-1]
        booking = Booking.objects.get(id=booking_id)
        booking.deposit_paid = True
        booking.status = 'DEPOSIT_PAID'
        booking.save()

        # 發送確認郵件
        send_mail(
            '訂房確認',
            f'感謝您的訂房，{booking.guest_name}！您的訂單編號是 {booking.id}。',
            settings.DEFAULT_FROM_EMAIL,
            [booking.guest_email],
            fail_silently=False,
        )

        return render(request, 'payment_success.html', {"booking": booking})
    else:
        return render(request, 'payment_error.html', {"error": payment.error})

# 支付取消視圖
def payment_cancel(request):
    return render(request, 'payment_cancel.html')

# 查詢訂單視圖
def search_booking(request):
    if request.method == "POST":
        guest_name = request.POST.get('guest_name')
        check_in_date = request.POST.get('check_in_date')
        bookings = Booking.objects.filter(guest_name=guest_name, check_in_date=check_in_date)
        return render(request, 'search_results.html', {'bookings': bookings})
    return render(request, 'search_booking.html')

# 取消訂單視圖
def cancel_booking(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if booking.deposit_paid:
        booking.status = 'CANCELLED'
        booking.save()
        return render(request, 'cancel_success.html')
    else:
        return render(request, 'cancel_error.html')

# 訂房 API 視圖集
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer