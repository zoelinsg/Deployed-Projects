from django.db import models
from django.contrib.auth.models import User

# 訊息模型
class Message(models.Model):
    STATUS_CHOICES = [
        ('unread', '未讀'),
        ('read', '已讀'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")  # 發送者
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")  # 接收者
    content = models.TextField()  # 訊息內容
    timestamp = models.DateTimeField(auto_now_add=True)  # 發送時間
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')  # 訊息狀態
    archived = models.BooleanField(default=False)  # 是否封存

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} - {self.get_status_display()}"