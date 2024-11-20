from django.contrib import admin
from .models import Message

# 註冊訊息模型
admin.site.register(Message)