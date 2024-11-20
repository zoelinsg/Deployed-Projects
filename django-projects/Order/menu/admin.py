from django.contrib import admin
from .models import Category, Tag, Product, Cart

# 註冊模型到管理介面
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'category')
    list_filter = ('available', 'category', 'tags')
    search_fields = ('name', 'description')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'product', 'quantity', 'created_at', 'updated_at')
    list_filter = ('session_id', 'created_at', 'updated_at')
    search_fields = ('session_id',)