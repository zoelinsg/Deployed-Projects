from rest_framework import serializers
from .models import Account, Expense, Category

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'user', 'balance', 'created', 'updated']  # 序列化欄位

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'name', 'account', 'category', 'user', 'amount', 'is_income', 'date', 'notes', 'created', 'updated']  # 序列化欄位

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  # 序列化欄位