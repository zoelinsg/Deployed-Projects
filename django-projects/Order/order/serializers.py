# OrderManagement/serializers.py

from rest_framework import serializers
from .models import Order, OrderItem
from menu.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    """
    訂單項目序列化器，用於將訂單中的每個項目序列化為 JSON 格式
    """
    menu_item = ProductSerializer(read_only=True)  # 嵌套序列化菜單項目

    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity', 'total_price']  # 定義需要序列化的欄位

class OrderSerializer(serializers.ModelSerializer):
    """
    訂單序列化器，用於將訂單模型序列化為 JSON 格式
    """
    items = OrderItemSerializer(many=True, read_only=True)  # 嵌套序列化訂單項目

    class Meta:
        model = Order
        fields = ['id', 'table', 'status', 'created_at', 'updated_at', 'items']  # 定義需要序列化的欄位