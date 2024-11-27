from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics  # 導入 generics
from django.urls import reverse  # 導入 reverse
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import ProductForm, CartItemForm, OrderForm
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
from paypalrestsdk import Payment
import paypalrestsdk
import os
import pandas as pd
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.utils.timezone import make_aware
from datetime import datetime
from openpyxl import Workbook  # 確保已安裝 openpyxl

# 初始化 PayPal SDK 配置
paypalrestsdk.configure({
    "mode": os.getenv("PAYPAL_MODE", "sandbox").strip(),  # 環境設置為 sandbox 或 live
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),  # PayPal 客戶端 ID
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")  # PayPal 客戶端密鑰
})

# 管理產品
@login_required
def manage_products(request):
    if request.user.profile.role != 'boss':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('product_list')

    products = Product.objects.all()
    return render(request, 'products/manage_products.html', {'products': products})

# 新增產品
@login_required
def add_product(request):
    if request.user.profile.role != 'boss':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "產品已新增。")
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

# 編輯產品
@login_required
def edit_product(request, pk):
    if request.user.profile.role != 'boss':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('product_list')

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "產品已更新。")
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

# 刪除產品
@login_required
def delete_product(request, pk):
    if request.user.profile.role != 'boss':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('product_list')

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "產品已刪除。")
        return redirect('manage_products')
    return render(request, 'products/delete_product.html', {'product': product})

# 管理庫存
@login_required
def manage_stock(request):
    if request.user.profile.role != 'boss':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('product_list')

    products = Product.objects.all()
    if request.method == 'POST':
        for product in products:
            stock = request.POST.get(f'stock_{product.id}')
            if stock is not None:
                product.stock = int(stock)
                product.save()
        messages.success(request, "庫存已更新。")
        return redirect('manage_stock')

    return render(request, 'products/manage_stock.html', {'products': products})

# 顯示所有商品
def product_list(request):
    if request.user.is_authenticated and request.user.profile.role == 'boss':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('boss_dashboard')
    products = Product.objects.all()
    default_image_url = settings.MEDIA_URL + 'product_images/default.jpg'
    return render(request, 'products/product_list.html', {'products': products, 'default_image_url': default_image_url})

# 顯示單個產品的詳細資訊
def product_detail(request, pk):
    if request.user.is_authenticated and request.user.profile.role == 'boss':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('boss_dashboard')
    product = get_object_or_404(Product, pk=pk)
    default_image_url = settings.MEDIA_URL + 'product_images/default.jpg'
    return render(request, 'products/product_detail.html', {'product': product, 'default_image_url': default_image_url})

# 顯示分類中的產品
def product_category(request, category_name):
    if request.user.is_authenticated and request.user.profile.role == 'boss':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('boss_dashboard')
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'products/product_category.html', {'products': products, 'category': category})

# 搜尋產品
def product_search(request):
    if request.user.is_authenticated and request.user.profile.role == 'boss':
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('boss_dashboard')
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'products/product_search.html', {'products': products, 'query': query})

# 新增到購物車
@login_required
def add_to_cart(request, product_id):
    """
    將指定商品新增到購物車
    """
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.clean()  # 確保購買數量不超過庫存
    cart_item.save()
    messages.success(request, f"{product.name} 已加入購物車。")
    return redirect('product_detail', pk=product_id)

# 移除購物車中的商品
@login_required
def remove_from_cart(request, item_id):
    """
    從購物車中移除指定的商品
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "商品已從購物車中移除。")
    return redirect('view_cart')

# 修改購物車中的商品
@login_required
def update_cart_item(request, item_id):
    """
    修改購物車中的商品數量
    """
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            messages.success(request, "購物車商品已更新。")
            return redirect('view_cart')
    else:
        form = CartItemForm(instance=cart_item)
    return render(request, 'cart/update_cart_item.html', {'form': form, 'cart_item': cart_item})

# 顯示購物車內容
@login_required
def view_cart(request):
    """
    顯示當前用戶的購物車內容
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/view_cart.html', {'cart': cart})

# 下訂單
@login_required
def place_order(request):
    """
    用戶下訂單
    """
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.status = 'processing'  # 設置訂單狀態為處理中
            order.save()
            # 從購物車創建訂單項目
            for item in cart.items.all():
                if item.product.stock < item.quantity:
                    messages.error(request, f"商品 {item.product.name} 庫存不足，無法完成訂單。")
                    return redirect('view_cart')
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
                item.product.stock -= item.quantity  # 減少庫存
                item.product.save()
            cart.items.all().delete()  # 清空購物車
            messages.success(request, "訂單已成功下達，請進行支付。")
            return redirect('process_payment', order_id=order.pk)
    else:
        form = OrderForm()
    return render(request, 'orders/place_order.html', {'form': form, 'cart': cart})

# 處理支付
@login_required
def process_payment(request, order_id):
    """
    處理 PayPal 支付
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    total = sum(item.quantity * item.product.price for item in order.items.all())
    payment = Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('payment_success', args=[order.id])),
            "cancel_url": request.build_absolute_uri(reverse('payment_cancel', args=[order.id]))
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
            "amount": {"total": str(total), "currency": "USD"},
            "description": f"Order {order.id}"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)  # 重定向到 PayPal 支付頁面
    else:
        messages.error(request, "支付過程中出現錯誤，請稍後再試。")
        return redirect('payment_error', order_id=order.id)

# 處理支付成功
@login_required
def payment_success(request, order_id):
    """
    支付成功處理
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    total = sum(item.quantity * item.product.price for item in order.items.all())  # 計算訂單總金額
    order.status = 'processing'  # 將訂單狀態改為處理中
    order.is_paid = True
    order.save()
    messages.success(request, "支付成功，訂單正在準備中。")
    return render(request, 'payment/payment_success.html', {'order': order, 'total': total})

# 支付取消
@login_required
def payment_cancel(request, order_id):
    """
    支付取消處理
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    messages.error(request, "支付已取消。")
    return render(request, 'payment/payment_cancel.html', {'order': order})

# 支付失敗
@login_required
def payment_error(request, order_id):
    """
    支付錯誤處理
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'payment/payment_error.html', {'order': order, 'error': "支付過程中出現錯誤。"})

# 客人查看自己的訂單
@login_required
def order_list(request):
    """
    客人查看自己的訂單列表
    """
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        order.total = sum(item.quantity * item.product.price for item in order.items.all())
    return render(request, 'orders/order_list.html', {'orders': orders})

# 客人查看訂單詳情
@login_required
def order_detail(request, order_id):
    """
    客人查看自己的訂單詳情
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.total = sum(item.quantity * item.product.price for item in order.items.all())
    return render(request, 'orders/order_detail.html', {'order': order})

# 確認訂單
@login_required
def confirm_order(request, order_id):
    """
    客人確認訂單後，將訂單狀態改為已完成
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'shipped':
        order.status = 'completed'
        order.save()
        messages.success(request, "訂單已確認完成")
    return redirect('order_list')

# 取消訂單
@login_required
def cancel_order(request, order_id):
    """
    客人取消訂單時，將訂單中的商品庫存還原
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'completed':
        order.status = 'cancelled'
        order.save()
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
        messages.success(request, "訂單已取消")
    return redirect('order_list')

# 老闆查看所有訂單
@login_required
def order_list_boss(request):
    """
    老闆查看所有訂單
    """
    if request.user.profile.role != 'boss':  # 檢查用戶角色是否為老闆
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('home')
    orders = Order.objects.all()  # 獲取所有訂單
    for order in orders:
        order.total = sum(item.quantity * item.product.price for item in order.items.all())  # 計算訂單總額
    return render(request, 'orders/order_list_boss.html', {'orders': orders})  # 渲染訂單列表頁面

# 老闆查看訂單詳情
@login_required
def order_detail_boss(request, order_id):
    """
    老闆查看訂單詳情
    """
    if request.user.profile.role != 'boss':  # 檢查用戶角色是否為老闆
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('consumer_dashboard')
    order = get_object_or_404(Order, id=order_id)  # 獲取指定訂單
    order.total = sum(item.quantity * item.product.price for item in order.items.all())  # 計算訂單總額
    return render(request, 'orders/order_detail_boss.html', {'order': order})  # 渲染訂單詳情頁面

# 管理訂單
@login_required
def manage_orders(request):
    """
    老闆管理訂單
    """
    if request.user.profile.role != 'boss':  # 檢查用戶角色是否為老闆
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('home')
    orders = Order.objects.all()  # 獲取所有訂單
    return render(request, 'orders/manage_orders.html', {'orders': orders})  # 渲染管理訂單頁面

# 老闆更新訂單狀態
@login_required
def update_order_status(request, order_id):
    """
    老闆更新訂單狀態為已出貨
    """
    if request.user.profile.role != 'boss':  # 檢查用戶角色是否為老闆
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('home')
    order = get_object_or_404(Order, id=order_id)  # 獲取指定訂單
    if request.method == 'POST':
        order.status = 'shipped'
        order.save()
        messages.success(request, "訂單狀態已更新為已出貨。")
        return redirect('order_detail_boss', order_id=order.id)
    return render(request, 'orders/update_order_status.html', {'order': order})

# 老闆查看銷售報表
@login_required
def sales_report(request):
    """
    老闆查看銷售報表
    """
    if request.user.profile.role != 'boss':  # 檢查用戶角色是否為老闆
        messages.error(request, "您沒有權限訪問此頁面。")
        return redirect('home')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = make_aware(datetime.combine(parse_date(start_date), datetime.min.time()))
        end_date = make_aware(datetime.combine(parse_date(end_date), datetime.max.time()))
        orders = Order.objects.filter(created_at__range=[start_date, end_date], status='completed')
    else:
        orders = Order.objects.filter(status='completed')

    sales_data = []
    for order in orders:
        for item in order.items.all():
            sales_data.append({
                '產品名稱': item.product.name,
                '數量': item.quantity,
                '價格': item.product.price,
                '小計': item.quantity * item.product.price,
            })

    df = pd.DataFrame(sales_data)
    if not df.empty:
        total_sales = df['小計'].sum()
        product_sales = df.groupby('產品名稱').agg({'數量': 'sum', '小計': 'sum'}).reset_index()
    else:
        total_sales = 0
        product_sales = pd.DataFrame(columns=['產品名稱', '數量', '小計'])

    if 'download' in request.GET:
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'
        product_sales.to_excel(response, index=False)
        return response

    return render(request, 'orders/sales_report.html', {
        'product_sales': product_sales.to_dict('records'),
        'total_sales': total_sales,
        'start_date': start_date,
        'end_date': end_date,
    })

# 產品列表 API 視圖
@api_view(['GET'])
def api_product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# 產品詳情 API 視圖
@api_view(['GET'])
def api_product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

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

# 訂單項目 API 視圖
class OrderItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer