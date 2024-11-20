from rest_framework import serializers
from .models import Message

# 訊息序列化器
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'