# 檔案: books/urls.py
from django.urls import path
from .views import (
    create_book, update_book, delete_book, book_list, book_detail,
    borrow_book, return_book, reader_dashboard, librarian_dashboard
)

urlpatterns = [
    path('', book_list, name='book_list'),  # 書籍列表
    path('book/<int:pk>/', book_detail, name='book_detail'),  # 書籍詳情
    path('book/create/', create_book, name='create_book'),  # 創建書籍
    path('book/<int:pk>/update/', update_book, name='update_book'),  # 更新書籍
    path('book/<int:pk>/delete/', delete_book, name='delete_book'),  # 刪除書籍
    path('book/<int:pk>/borrow/', borrow_book, name='borrow_book'),  # 借書
    path('book/<int:pk>/return/', return_book, name='return_book'),  # 還書
    path('reader_dashboard/', reader_dashboard, name='reader_dashboard'),  # 讀者個人書房
    path('librarian_dashboard/', librarian_dashboard, name='librarian_dashboard'),  # 館員管理頁面
]