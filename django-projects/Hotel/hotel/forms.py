from django import forms
from .models import Booking, Hotel

# 訂房表單
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'hotel', 'single_rooms', 'double_rooms', 'quad_rooms', 'six_rooms', 
            'check_in_date', 'check_out_date', 'guest_name', 'guest_email', 
            'phone', 'eco_plan', 'extra_bed', 'spa_voucher', 'hotel_facilities', 'status'
        ]  # 表單欄位
        labels = {
            'hotel': '飯店',
            'single_rooms': '單人房數量',
            'double_rooms': '雙人房數量',
            'quad_rooms': '四人房數量',
            'six_rooms': '六人房數量',
            'check_in_date': '入住日期',
            'check_out_date': '退房日期',
            'guest_name': '客人姓名',
            'guest_email': '客人電子郵件',
            'phone': '電話',
            'eco_plan': '環保方案',
            'extra_bed': '加床數量',
            'spa_voucher': 'SPA券',
            'hotel_facilities': '飯店設施',
            'status': '訂單狀態'
        }  # 欄位標籤
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }  # 使用日期選擇器