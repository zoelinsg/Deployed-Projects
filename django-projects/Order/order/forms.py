from django import forms
from .models import Order, OrderItem

# 建立訂單表單類別
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table', 'status']
        labels = {
            'table': '餐桌',
            'status': '訂單狀態',
        }

# 建立訂單項目表單類別
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'menu_item', 'quantity']
        labels = {
            'order': '訂單',
            'menu_item': '菜單項目',
            'quantity': '數量',
        }