from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record

# 使用者註冊表單，繼承自 Django 的 UserCreationForm
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))  # 自定義 Email 欄位，使用 Bootstrap 樣式和占位符
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))  # 自定義名字欄位
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))  # 自定義姓氏欄位

    class Meta:
        model = User  # 指定表單對應的模型為 User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')  # 指定表單包含的欄位

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

# 新增資料的表單，繼承自 Django 的 ModelForm
class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"First Name", "class":"form-control"}), label="")  # 自定義名字欄位
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Last Name", "class":"form-control"}), label="")  # 自定義姓氏欄位
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Email", "class":"form-control"}), label="")  # 自定義電子郵件欄位
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Phone", "class":"form-control"}), label="")  # 自定義電話號碼欄位
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Address", "class":"form-control"}), label="")  # 自定義地址欄位
    city = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"City", "class":"form-control"}), label="")  # 自定義城市欄位
    company = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Company", "class":"form-control"}), label="")  # 自定義公司欄位
    position = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Position", "class":"form-control"}), label="")  # 自定義職位欄位
    remark = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={"placeholder":"Remark", "class":"form-control"}), label="")  # 自定義備註欄位

    class Meta:
        model = Record  # 指定表單對應的模型為 Record
        exclude = ("created_at",)  # 排除不需要顯示的欄位