from django import forms
from .models import Product

# 產品表單，用於管理介面或前端表單
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price', 'stock', 'category', 'tags']
        labels = {
            'name': '產品名稱',
            'image': '圖片',
            'description': '描述',
            'price': '價格',
            'stock': '庫存量',
            'category': '所屬類別',
            'tags': '標籤',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }