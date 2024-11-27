from django import forms
from .models import Order, OrderItem

# 訂單表單，用於管理介面或前端表單
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone']  # 只顯示配送地址和聯絡電話
        labels = {
            'address': '配送地址',
            'phone': '聯絡電話',
        }

# 訂單項目表單，用於管理介面或前端表單
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
        labels = {
            'product': '產品',
            'quantity': '數量',
            'price': '價格',
        }