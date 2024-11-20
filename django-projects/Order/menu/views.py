from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product, Cart
from .serializers import ProductSerializer, CartSerializer
from .forms import CartForm

# 顯示所有菜單項目
def menu_item_list(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})  # 使用 home.html 模板

# 顯示單個菜單項目的詳細資訊
def menu_item_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.product = product
            if not request.session.session_key:
                request.session.create()
            cart_item.session_id = request.session.session_key  # 設置 session_id
            cart_item.save()
            return redirect('menu_item_detail', pk=pk)
    else:
        form = CartForm()
    return render(request, 'menu_item_detail.html', {'product': product, 'form': form})  # 使用 menu_item_detail.html 模板

# 顯示購物車
def cart(request):
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key
    cart_items = Cart.objects.filter(session_id=session_id)
    cart_total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})  # 使用 cart.html 模板

# 刪除購物車項目
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    cart_item.delete()
    return redirect('cart')

# 修改購物車項目數量
def update_cart_item(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    if request.method == 'POST':
        form = CartForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('cart')
    else:
        form = CartForm(instance=cart_item)
    return render(request, 'update_cart_item.html', {'form': form, 'cart_item': cart_item})

# 搜尋餐點
def search_menu_items(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'menu_item_list.html', {'products': products, 'query': query})  # 使用 menu_item_list.html 模板

# 添加到購物車
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.product = product
            if not request.session.session_key:
                request.session.create()
            cart_item.session_id = request.session.session_key  # 設置 session_id
            cart_item.save()
            return redirect('cart')
    else:
        form = CartForm()
    return render(request, 'menu_item_detail.html', {'product': product, 'form': form})  # 使用 menu_item_detail.html 模板

# API 視圖集
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer