# MenuManagement/serializers.py

from rest_framework import serializers
from .models import Product, Category, Tag, Cart

class CategorySerializer(serializers.ModelSerializer):
    """
    類別序列化器，將類別模型序列化為 JSON 格式
    """
    class Meta:
        model = Category
        fields = ['id', 'name']  # 定義需要序列化的欄位

class TagSerializer(serializers.ModelSerializer):
    """
    標籤序列化器，將標籤模型序列化為 JSON 格式
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']  # 定義需要序列化的欄位

class ProductSerializer(serializers.ModelSerializer):
    """
    菜單項目序列化器，將菜單項目模型序列化為 JSON 格式
    """
    category = CategorySerializer(read_only=True)  # 嵌套序列化類別
    tags = TagSerializer(many=True, read_only=True)  # 嵌套序列化標籤

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'available', 'category', 'tags', 'image']  # 定義需要序列化的欄位

class CartSerializer(serializers.ModelSerializer):
    """
    購物車序列化器，將購物車模型序列化為 JSON 格式
    """
    product = ProductSerializer(read_only=True)  # 嵌套序列化菜單項目

    class Meta:
        model = Cart
        fields = ['id', 'session_id', 'product', 'quantity', 'created_at', 'updated_at']  # 定義需要序列化的欄位