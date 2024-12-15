from django.contrib import admin
from .models import Photo, Category, Album, Tag

# 註冊模型到管理後台
admin.site.register(Photo)  # 註冊相片模型
admin.site.register(Category)  # 註冊相片類別模型
admin.site.register(Album)  # 註冊相簿模型
admin.site.register(Tag)  # 註冊標籤模型