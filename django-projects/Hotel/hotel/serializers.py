from rest_framework import serializers
from .models import Booking

# 訂房序列化器
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'hotel', 'single_rooms', 'double_rooms', 'quad_rooms', 'six_rooms', 
            'check_in_date', 'check_out_date', 'guest_name', 'guest_email', 
            'phone', 'eco_plan', 'extra_bed', 'spa_voucher', 'hotel_facilities', 'total_price', 'deposit_paid', 'status'
        ]  # 序列化欄位