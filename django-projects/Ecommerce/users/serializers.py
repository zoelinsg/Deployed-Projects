# 序列化器，處理UserProfile的序列化和反序列化
from rest_framework import serializers
from .models import UserProfile  # 匯入 UserProfile 模型

# 定義 UserProfile 的序列化器，用於 API 接口
class UserProfileSerializer(serializers.ModelSerializer):
    # Meta 類別定義序列化的模型及欄位
    class Meta:
        model = UserProfile  # 指定序列化的模型為 UserProfile
        fields = ['phone', 'country', 'birth_date', 'gender', 'bio']  # 定義序列化的欄位