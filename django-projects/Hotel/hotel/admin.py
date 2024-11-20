from django.contrib import admin
from .models import Hotel, Room, Booking

# 註冊飯店模型
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'phone')  # 顯示欄位
    search_fields = ('name', 'city', 'country')  # 搜尋欄位

# 註冊房間模型
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'room_number', 'price_per_night', 'capacity', 'is_available')  # 顯示欄位
    list_filter = ('hotel', 'room_type', 'is_available')  # 篩選欄位
    search_fields = ('room_number',)  # 搜尋欄位

# 註冊訂房模型
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'single_rooms', 'double_rooms', 'quad_rooms', 'six_rooms', 'check_in_date', 'check_out_date', 'guest_name', 'total_price', 'deposit_paid', 'status')  # 顯示欄位
    list_filter = ('hotel', 'check_in_date', 'check_out_date', 'deposit_paid', 'status')  # 篩選欄位
    search_fields = ('guest_name', 'guest_email', 'phone')  # 搜尋欄位