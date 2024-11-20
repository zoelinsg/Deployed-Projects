from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# 活動模型
class Activity(models.Model):
    LOCATION_CHOICES = [
        ('3F多媒體室', '3F多媒體室'),
        ('4F多功能室', '4F多功能室'),
        ('5樓大演講廳', '5樓大演講廳'),
    ]
    
    title = models.CharField(max_length=255)  # 活動標題
    start_date = models.DateField()  # 開始日期
    start_time = models.TimeField()  # 開始時間
    end_date = models.DateField()  # 結束日期
    end_time = models.TimeField()  # 結束時間
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_activities')  # 創建者
    description = models.TextField()  # 活動描述
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)  # 地點
    participants = models.ManyToManyField(User, related_name='participated_activities')  # 參與者
    speaker = models.CharField(max_length=255, null=True, blank=True)  # 演講者（可選）

    def __str__(self):
        return self.title  # 返回活動標題作為模型的字串表示

    def clean(self):
        # 檢查是否有其他活動在同一時間同一地點
        overlapping_activities = Activity.objects.filter(
            location=self.location,
            start_date=self.start_date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)
        
        if overlapping_activities.exists():
            raise ValidationError('在同一時間同一地點已經有其他活動安排。')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)