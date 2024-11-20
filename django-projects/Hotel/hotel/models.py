from django.db import models
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.utils import timezone

# 飯店模型
class Hotel(models.Model):
    name = models.CharField(max_length=100)  # 飯店名稱
    address = models.CharField(max_length=200)  # 地址
    city = models.CharField(max_length=50)  # 城市
    country = CountryField()  # 國家
    phone = models.CharField(max_length=20)  # 電話
    email = models.EmailField(blank=True, null=True)  # 電子郵件
    website = models.URLField(blank=True, null=True)  # 網站

    def __str__(self):
        return self.name

# 房間模型
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)  # 所屬飯店
    ROOM_TYPES = [
        ('SINGLE', '單人房'),
        ('DOUBLE', '雙人房'),
        ('QUAD', '四人房'),
        ('SIX', '六人房'),
    ]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)  # 房型
    room_number = models.CharField(max_length=10)  # 房號
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)  # 每晚價格
    capacity = models.IntegerField()  # 容量
    has_tv = models.BooleanField(default=False)  # 是否有電視
    is_available = models.BooleanField(default=True)  # 是否可用

    def __str__(self):
        return f"{self.room_type} - {self.room_number} - {self.capacity} persons"

# 訂房模型
class Booking(models.Model):
    STATUS_CHOICES = [
        ('DEPOSIT_PAID', '已付訂金'),
        ('CANCELLED', '已取消'),
        ('COMPLETED', '已完成'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)  # 飯店
    single_rooms = models.IntegerField(default=0)  # 單人房數量
    double_rooms = models.IntegerField(default=0)  # 雙人房數量
    quad_rooms = models.IntegerField(default=0)  # 四人房數量
    six_rooms = models.IntegerField(default=0)  # 六人房數量
    check_in_date = models.DateField()  # 入住日期
    check_out_date = models.DateField()  # 退房日期
    guest_name = models.CharField(max_length=100)  # 客人姓名
    guest_email = models.EmailField()  # 客人電子郵件
    phone = models.CharField(max_length=20)  # 電話
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # 總價
    deposit_paid = models.BooleanField(default=False)  # 是否已支付訂金
    eco_plan = models.BooleanField(default=False)  # 環保方案
    extra_bed = models.IntegerField(default=0)  # 加床數量
    spa_voucher = models.BooleanField(default=False)  # SPA券
    hotel_facilities = models.BooleanField(default=False)  # 飯店設施
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DEPOSIT_PAID')  # 訂單狀態

    def __str__(self):
        return f"Booking for {self.guest_name} at {self.hotel.name}"

    def clean(self):
        # 檢查入住日期是否為過去的日期
        if self.check_in_date < timezone.now().date():
            raise ValidationError("入住日期不能是過去的日期")
        # 檢查退房日期是否早於或等於入住日期
        if self.check_out_date <= self.check_in_date:
            raise ValidationError("退房日期必須晚於入住日期")

    def save(self, *args, **kwargs):
        # 驗證數據
        self.clean()
        # 確認房間是否可用
        total_rooms_needed = self.single_rooms + self.double_rooms + self.quad_rooms + self.six_rooms
        available_rooms = Room.objects.filter(hotel=self.hotel, is_available=True).count()
        if total_rooms_needed > available_rooms:
            raise ValidationError("所選飯店在預定日期客滿，無法訂房")
        
        # 計算總價
        self.total_price = 0
        room_types = {
            'SINGLE': self.single_rooms,
            'DOUBLE': self.double_rooms,
            'QUAD': self.quad_rooms,
            'SIX': self.six_rooms,
        }
        for room_type, count in room_types.items():
            room = Room.objects.filter(hotel=self.hotel, room_type=room_type, is_available=True).first()
            if room:
                self.total_price += room.price_per_night * count * (self.check_out_date - self.check_in_date).days
        if self.eco_plan:
            self.total_price -= 200
        if self.extra_bed > 0:
            self.total_price += self.extra_bed * 300
        if self.spa_voucher:
            self.total_price += 500
        if self.hotel_facilities:
            self.total_price += 300

        # 保存記錄
        super().save(*args, **kwargs)