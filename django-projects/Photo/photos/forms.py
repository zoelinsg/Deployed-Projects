from django import forms
from .models import Photo, Tag

class PhotoForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="使用 # 分隔標籤，例如：#台北 #夜景")

    class Meta:
        model = Photo
        fields = ['title', 'description', 'album', 'category', 'image', 'tags']  # 單張照片上傳