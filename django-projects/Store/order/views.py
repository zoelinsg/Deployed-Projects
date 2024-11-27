from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from .forms import OrderForm
from rest_framework import generics
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
from paypalrestsdk import Payment
import paypalrestsdk
import os
from django.urls import reverse

# 初始化 PayPal SDK
paypalrestsdk.configure({
    "mode": os.getenv("PAYPAL_MODE"),  # sandbox 或 live
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
})

# 加入購物車
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        if cart_item.quantity + 1 > product.stock:
            messages.error(request, f"{product.name} 的庫存不足")
            return redirect('product_detail', pk=product_id)
        cart_item.quantity += 1
    else:
        if cart_item.quantity > product.stock:
            messages.error(request, f"{product.name} 的庫存不足")
            return redirect('product_detail', pk=product_id)
    cart_item.save()
    messages.success(request, f"{product.name} 已加入購物車")
    return redirect('cart_detail')

# 修改購物車商品數量
@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if quantity > cart_item.product.stock:
            messages.error(request, f"{cart_item.product.name} 的庫存不足")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"{cart_item.product.name} 的數量已更新")
    return redirect('cart_detail')

# 刪除購物車商品
@login_required
def delete_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, f"{cart_item.product.name} 已從購物車中刪除")
    return redirect('cart_detail')

# 購物車頁面
@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    total = sum(item.quantity * item.product.price for item in cart.items.all())
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'total': total})

# 送出訂單
@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    total = sum(item.quantity * item.product.price for item in cart.items.all())
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.is_paid = False
            order.save()
            for item in cart.items.all():
                if item.quantity > item.product.stock:
                    messages.error(request, f"{item.product.name} 的庫存不足")
                    return redirect('cart_detail')
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
                item.product.stock -= item.quantity
                item.product.save()
            cart.items.all().delete()
            messages.success(request, "訂單已成功送出")
            return redirect('process_payment', order_id=order.id)  # 跳轉到支付頁面
    else:
        form = OrderForm()
    return render(request, 'order/create_order.html', {'form': form, 'cart': cart, 'total': total})

# 查看自己的訂單
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        order.total = sum(item.quantity * item.product.price for item in order.items.all())
    return render(request, 'order/order_list.html', {'orders': orders})

# 查看訂單詳情
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.total = sum(item.quantity * item.product.price for item in order.items.all())
    return render(request, 'order/order_detail.html', {'order': order})

# 確認訂單
@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'shipped':
        order.status = 'completed'
        order.save()
        messages.success(request, "訂單已確認完成")
    return redirect('order_list')

# 取消訂單
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'completed':
        order.status = 'cancelled'
        order.save()
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
        messages.success(request, "訂單已取消")
    return redirect('order_list')

# 處理支付
@login_required
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    total = sum(item.quantity * item.product.price for item in order.items.all())
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('payment_success', args=[order.id])),  # 支付成功後的返回 URL
            "cancel_url": request.build_absolute_uri(reverse('payment_cancel', args=[order.id]))  # 支付取消後的返回 URL
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": item.product.name,
                    "sku": str(item.product.id),
                    "price": str(item.product.price),
                    "currency": "USD",
                    "quantity": item.quantity
                } for item in order.items.all()]
            },
            "amount": {
                "total": str(total),
                "currency": "USD"
            },
            "description": f"Order {order.id}"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return redirect(approval_url)
    else:
        messages.error(request, "支付過程中出現錯誤，請稍後再試。")
        return redirect('payment_error', order_id=order.id)

# 支付成功
@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.status = 'shipped'  # 支付成功後將訂單狀態改為已出貨
    order.is_paid = True
    order.save()
    messages.success(request, "支付成功，訂單正在準備中")
    return render(request, 'payment/payment_success.html', {'order': order})

# 支付取消
@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    messages.error(request, "支付已取消")
    return render(request, 'payment/payment_cancel.html', {'order': order})

# 支付失敗
@login_required
def payment_error(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    error_message = "支付過程中出現錯誤，請稍後再試。"
    return render(request, 'payment/payment_error.html', {'order': order, 'error': error_message})

# 購物車 API 視圖
class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

# 訂單 API 視圖
class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer