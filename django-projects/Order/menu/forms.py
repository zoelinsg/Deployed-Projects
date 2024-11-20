from django import forms
from .models import Category, Tag, Product, Cart

# 建立類別表單類別
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': '類別名稱',
        }

# 建立標籤表單類別
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': '標籤名稱',
        }

# 建立菜單項目表單類別
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price', 'available', 'category', 'tags']
        labels = {
            'name': '菜名',
            'image': '圖片',
            'description': '描述',
            'price': '價格',
            'available': '是否可供應',
            'category': '所屬類別',
            'tags': '標籤',
        }

# 建立購物車表單類別
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
        labels = {
            'quantity': '數量',
        }