from django import forms
from .models import Activity

# 活動表單
class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'start_date', 'start_time', 'end_date', 'end_time', 'description', 'location', 'speaker']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'speaker': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '活動標題',
            'start_date': '開始日期',
            'start_time': '開始時間',
            'end_date': '結束日期',
            'end_time': '結束時間',
            'description': '活動描述',
            'location': '地點',
            'speaker': '演講者（可選）',
        }