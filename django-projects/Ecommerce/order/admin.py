from django.contrib import admin
from .models import Category, Tag, Product, Cart, CartItem, Order, OrderItem

# 註冊模型到管理介面
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 顯示欄位
    search_fields = ('name',)  # 搜尋欄位

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 顯示欄位
    search_fields = ('name',)  # 搜尋欄位

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_sold_out', 'category')  # 顯示欄位
    list_filter = ('is_sold_out', 'category', 'tags')  # 過濾器
    search_fields = ('name', 'description')  # 搜尋欄位
    autocomplete_fields = ('category', 'tags')  # 自動完成欄位

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)  # 顯示欄位
    search_fields = ('user__username',)  # 搜尋欄位

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')  # 顯示欄位
    search_fields = ('cart__user__username', 'product__name')  # 搜尋欄位

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'is_paid', 'created_at')  # 顯示欄位
    list_filter = ('status', 'is_paid')  # 過濾器
    search_fields = ('user__username', 'id')  # 搜尋欄位

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')  # 顯示欄位
    search_fields = ('order__id', 'product__name')  # 搜尋欄位