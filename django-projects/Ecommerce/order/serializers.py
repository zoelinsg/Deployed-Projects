from rest_framework import serializers
from .models import Product, Category, Tag, Cart, CartItem, Order, OrderItem

# 定義 Product 的序列化器，用於 API 接口
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product  # 指定序列化的模型為 Product
        fields = ['id', 'name', 'image', 'description', 'price', 'stock', 'is_sold_out', 'category', 'tags']  # 定義序列化的欄位

# 定義 Order 的序列化器，用於 API 接口
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order  # 指定序列化的模型為 Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'is_paid', 'address', 'phone']  # 定義序列化的欄位

# 定義 Cart 的序列化器，用於 API 接口
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart  # 指定序列化的模型為 Cart
        fields = ['id', 'user']  # 定義序列化的欄位

# 定義 CartItem 的序列化器，用於 API 接口
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem  # 指定序列化的模型為 CartItem
        fields = ['id', 'cart', 'product', 'quantity']  # 定義序列化的欄位

# 定義 OrderItem 的序列化器，用於 API 接口
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem  # 指定序列化的模型為 OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']  # 定義序列化的欄位