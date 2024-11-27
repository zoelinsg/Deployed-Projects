from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem

# 購物車序列化器
class CartSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cart
        fields = ['user', 'items']

# 購物車項目序列化器
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity']

# 訂單序列化器
class OrderSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Order
        fields = ['user', 'created_at', 'updated_at', 'status', 'is_paid', 'items']

# 訂單項目序列化器
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']