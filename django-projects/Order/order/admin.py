from django.contrib import admin
from .models import Order, OrderItem

# 註冊訂單模型到管理介面
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'table', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'table', 'created_at', 'updated_at')
    search_fields = ('order_number',)
    list_editable = ('status',)  # 允許在列表中編輯訂單狀態

# 註冊訂單項目模型到管理介面
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'total_price')
    list_filter = ('order', 'menu_item')
    search_fields = ('order__order_number', 'menu_item__name')