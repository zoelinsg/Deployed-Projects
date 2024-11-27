from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# 課程模型
class Course(models.Model):
    code = models.CharField(max_length=255, unique=True, editable=False)  # 課程代碼，自動生成，唯一
    name = models.CharField(max_length=255)  # 課程名稱
    category = models.ForeignKey('Category', on_delete=models.CASCADE)  # 課程類別
    description = models.TextField()  # 課程描述
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'profile__role': 'teacher'})  # 教師
    students = models.ManyToManyField(User, related_name='enrolled_courses', limit_choices_to={'profile__role': 'student'})  # 學生
    start_date = models.DateField()  # 開始日期
    end_date = models.DateField()  # 結束日期
    notes = models.TextField(blank=True)  # 備註
    created_at = models.DateTimeField(auto_now_add=True)  # 創建時間
    updated_at = models.DateTimeField(auto_now=True)  # 更新時間

    def __str__(self):
        return self.name  # 返回課程名稱作為模型的字串表示

    # 自動生成課程代碼
    def save(self, *args, **kwargs):
        if not self.code:
            current_year = datetime.now().year
            current_month = datetime.now().month
            last_course = Course.objects.filter(code__startswith=f'C{current_year}{current_month:02d}').order_by('code').last()
            if last_course:
                last_number = int(last_course.code[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.code = f'C{current_year}{current_month:02d}{new_number:04d}'
        super().save(*args, **kwargs)

# 課程類別模型
class Category(models.Model):
    name = models.CharField(max_length=255)  # 類別名稱
    description = models.TextField()  # 類別描述

    def __str__(self):
        return self.name  # 返回類別名稱作為模型的字串表示

# 教材模型
class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')  # 所屬課程
    file = models.FileField(upload_to='materials/')  # 教材文件
    description = models.TextField(blank=True)  # 教材描述
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 上傳時間

    def __str__(self):
        return f'{self.course.name} - {self.file.name}'  # 返回課程名稱和文件名稱作為模型的字串表示