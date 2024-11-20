from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from menu.models import Cart

# 顯示所有訂單
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})  # 使用 order_list.html 模板

# 顯示單個訂單的詳細資訊
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order_detail.html', {'order': order})  # 使用 order_detail.html 模板

# 創建新的訂單
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            session_id = request.session.session_key
            cart_items = Cart.objects.filter(session_id=session_id)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item.product,
                    quantity=item.quantity,
                    total_price=item.total_price()
                )
            cart_items.delete()  # 清空購物車
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})  # 使用 create_order.html 模板

# 創建新的訂單項目
def create_order_item(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            return redirect('order_detail', pk=order_id)
    else:
        form = OrderItemForm()
    return render(request, 'create_order_item.html', {'form': form, 'order': order})  # 使用 create_order_item.html 模板