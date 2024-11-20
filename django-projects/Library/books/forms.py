from django import forms
from .models import Book

# 書籍表單，用於創建書籍
class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'cover', 'author', 'category', 'description', 'publication_date', 'isbn']  # 定義表單顯示的欄位

    def __init__(self, *args, **kwargs):
        super(BookCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': '輸入書名'})
        self.fields['cover'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control', 'placeholder': '輸入作者'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': '輸入書籍描述'})
        self.fields['publication_date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        self.fields['isbn'].widget.attrs.update({'class': 'form-control', 'placeholder': '輸入ISBN'})

# 書籍表單，用於管理書籍
class BookManageForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'cover', 'author', 'category', 'description', 'publication_date', 'isbn', 'status', 'borrowed_by', 'borrowed_date']  # 定義表單顯示的欄位

    def __init__(self, *args, **kwargs):
        super(BookManageForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': '輸入書名'})
        self.fields['cover'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control', 'placeholder': '輸入作者'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': '輸入書籍描述'})
        self.fields['publication_date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        self.fields['isbn'].widget.attrs.update({'class': 'form-control', 'placeholder': '輸入ISBN'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['borrowed_by'].widget.attrs.update({'class': 'form-control'})
        self.fields['borrowed_date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})