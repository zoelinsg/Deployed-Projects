from django import forms
from .models import Product, CartItem, Order

# 產品表單，用於管理介面或前端表單
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # 指定表單對應的模型為 Product
        fields = ['name', 'image', 'description', 'price', 'stock', 'category', 'tags']  # 定義表單包含的欄位
        labels = {
            'name': '產品名稱',
            'image': '圖片',
            'description': '描述',
            'price': '價格',
            'stock': '庫存量',
            'category': '所屬類別',
            'tags': '標籤',
        }  # 定義欄位的標籤
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),  # 自定義描述欄位的顯示樣式
        }

# 購物車項目表單，用於管理購物車中的產品數量
class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem  # 指定表單對應的模型為 CartItem
        fields = ['quantity']  # 定義表單包含的欄位
        labels = {
            'quantity': '數量',
        }  # 定義欄位的標籤

# 訂單表單，用於管理訂單資訊
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order  # 指定表單對應的模型為 Order
        fields = ['address', 'phone']  # 定義表單包含的欄位
        labels = {
            'address': '配送地址',
            'phone': '聯絡電話',
        }  # 定義欄位的標籤