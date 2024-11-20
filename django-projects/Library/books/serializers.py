# 檔案: books/serializers.py
from rest_framework import serializers
from .models import Book, BorrowHistory

# 定義 Book 的序列化器，用於 API 接口
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'cover', 'author', 'category', 'description', 'publication_date', 'isbn', 'status', 'borrowed_by', 'borrowed_date', 'due_date', 'cancelled_date']  # 定義序列化的欄位

# 定義 BorrowHistory 的序列化器，用於 API 接口
class BorrowHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowHistory
        fields = ['id', 'book', 'user', 'borrowed_date', 'returned_date']  # 定義序列化的欄位