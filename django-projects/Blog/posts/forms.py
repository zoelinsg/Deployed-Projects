from django import forms
from .models import Post, Tag, Comment

# 文章表單
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '標題',
            'content': '內容',
            'category': '類別',
            'image': '圖片',
            'tags': '標籤',
        }

# 標籤表單
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': '標籤名稱',
        }

# 評論表單
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '新增評論'
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 1,  # 設定為 3 行高度
                'cols': 50,  # 設定寬度為 40 列
                'style': 'resize: none;',  # 禁用手動調整大小
                'placeholder': '輸入您的評論...',  # 添加提示文字
            }),
        }