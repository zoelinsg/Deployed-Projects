# 檔案: books/views.py
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, BorrowHistory
from .forms import BookCreateForm, BookManageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 創建書籍的視圖（僅館員）
@login_required
def create_book(request):
    if request.user.profile.role != 'librarian':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('book_list')
    
    if request.method == 'POST':
        form = BookCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "書籍創建成功。")
            return redirect('book_list')  # 書籍創建成功後重定向到書籍列表頁面
    else:
        form = BookCreateForm()
    return render(request, 'library/book_form.html', {'form': form})

# 更新書籍的視圖（僅館員）
@login_required
def update_book(request, pk):
    if request.user.profile.role != 'librarian':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookManageForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "書籍更新成功。")
            return redirect('book_detail', pk=book.pk)  # 書籍更新成功後重定向到書籍詳情頁面
    else:
        form = BookManageForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form})

# 刪除書籍的視圖（僅館員）
@login_required
def delete_book(request, pk):
    if request.user.profile.role != 'librarian':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, "書籍刪除成功。")
        return redirect('book_list')
    return render(request, 'library/book_confirm_delete.html', {'book': book})

# 書籍列表視圖（所有用戶）
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

# 書籍詳情視圖（所有用戶）
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})

# 借書視圖（僅讀者）
@login_required
def borrow_book(request, pk):
    if request.user.profile.role != 'reader':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)
    if book.status == 'available':
        book.status = 'borrowed'
        book.borrowed_by = request.user
        book.borrowed_date = timezone.now()
        book.save()
        # 記錄借閱歷史
        BorrowHistory.objects.create(book=book, user=request.user, borrowed_date=book.borrowed_date)
        messages.success(request, "書籍借閱成功。")
    else:
        messages.error(request, "該書籍目前不可借閱。")
    return redirect('book_detail', pk=pk)

# 還書視圖（僅讀者）
@login_required
def return_book(request, pk):
    if request.user.profile.role != 'reader':
        messages.error(request, "您沒有權限執行此操作。")
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)
    if book.status == 'borrowed' and book.borrowed_by == request.user:
        book.status = 'available'
        book.borrowed_by = None
        book.borrowed_date = None
        book.due_date = None
        book.save()
        # 更新借閱歷史中的歸還日期
        try:
            borrow_history = BorrowHistory.objects.filter(book=book, user=request.user).latest('borrowed_date')
            borrow_history.returned_date = timezone.now()
            borrow_history.save()
        except BorrowHistory.DoesNotExist:
            messages.error(request, "找不到對應的借閱歷史記錄。")
            return redirect('book_detail', pk=pk)
        
        messages.success(request, "書籍歸還成功。")
    else:
        messages.error(request, "您無法歸還此書籍。")
    return redirect('book_detail', pk=pk)

# 讀者個人書房視圖（僅讀者）
@login_required
def reader_dashboard(request):
    if request.user.profile.role != 'reader':
        messages.error(request, "您沒有權限查看此頁面。")
        return redirect('book_list')
    
    borrow_histories = BorrowHistory.objects.filter(user=request.user)
    reserved_books = Book.objects.filter(borrowed_by=request.user, status='reserved')
    return render(request, 'library/reader_dashboard.html', {
        'borrow_histories': borrow_histories,
        'reserved_books': reserved_books,
    })

# 館員管理頁面視圖（僅館員）
@login_required
def librarian_dashboard(request):
    if request.user.profile.role != 'librarian':
        messages.error(request, "您沒有權限查看此頁面。")
        return redirect('book_list')
    
    borrow_histories = BorrowHistory.objects.all()
    reserved_books = Book.objects.filter(status='reserved')
    return render(request, 'library/librarian_dashboard.html', {
        'borrow_histories': borrow_histories,
        'reserved_books': reserved_books,
    })