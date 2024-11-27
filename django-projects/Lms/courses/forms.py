from django import forms
from .models import Course, Category, Material

# 課程表單
class CourseForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}), label='開始日期')  # 使用 DateInput 作為日期選擇器
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control datepicker'}), label='結束日期')  # 使用 DateInput 作為日期選擇器
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), label='課程描述')  # 課程描述，限制為三行
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), label='備註', required=False)  # 備註，限制為三行

    class Meta:
        model = Course  # 指定表單對應的模型為 Course
        fields = ['name', 'category', 'description', 'teacher', 'start_date', 'end_date', 'notes']  # 移除 students 欄位

# 課程類別表單
class CategoryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), label='類別描述')  # 類別描述，限制為三行

    class Meta:
        model = Category  # 指定表單對應的模型為 Category
        fields = ['name', 'description']  # 定義表單包含的欄位

# 教材表單
class MaterialForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), label='教材描述', required=False)  # 教材描述，限制為三行

    class Meta:
        model = Material  # 指定表單對應的模型為 Material
        fields = ['course', 'file', 'description']  # 定義表單包含的欄位